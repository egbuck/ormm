import io
import sys

from quantecon.markov import MarkovChain
import scipy.stats
import numpy as np
import pytest

from ormm.markov import analyze_dtmc, print_markov, analyze_ctmc


def test_income_audit():
    """A simple example of markov chain"""
    # Define MarkovChain object - P is transition matrix
    P = [[0.6, 0.4], [0.5, 0.5]]
    state_values = [0, 1]
    analysis = analyze_dtmc(P, state_values,
                            sim_kwargs={"ts_length": 25,
                                        "random_state": 42})
    analysis["steady_state"]['output'] = \
        analysis["steady_state"]['output'].round(3)
    test = {
        'cdfs': np.array([[0.6, 1.],
                          [0.5, 1.]]),
        'steady_state': {'output': np.array([[0.556, 0.444]])},
        'sim': {'kwargs': {'ts_length': 25, 'init': None, "random_state": 42},
                'output': np.array([0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1,
                                    0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0])}}
    # Assert that numpy arrays are the same (except sim & stdy state output)
    assert all([np.allclose(analysis[k], test[k])
                for k in analysis if k not in ['sim', 'steady_state']])
    # assert sim kwargs values are the same
    assert all([test["sim"]["kwargs"][k] == analysis["sim"]["kwargs"][k]
                for k in analysis["sim"]["kwargs"]])
    # Assert that sim output numpy arrays are the same (fixed random state)
    assert np.allclose(analysis["sim"]["output"], test["sim"]["output"])
    # Assert that steady state output numpy arrays are the same
    assert np.allclose(analysis["steady_state"]["output"],
                       test["steady_state"]["output"])
    # Assert that both have the same keys
    assert test.keys() == analysis.keys()
    assert test['sim'].keys() == analysis["sim"].keys()
    assert test['sim']["kwargs"].keys() == analysis["sim"]["kwargs"].keys()

    # Assert print_markov works correctly with sim kwarg
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_markov(analysis)
    sys.stdout = sys.__stdout__  # reset stdout
    test_str = ("CDFs:\n"
                "[[0.6 1. ]\n"
                " [0.5 1. ]]\n\n"
                "Steady State Probs:\n"
                "[0.556 0.444]\n\n"
                "Simulation of length 25\n"
                "Initial Conditions:\n"
                "None\n"
                "Output:\n"
                "[0 1 0 1 1 0 0 0 0 0 1 0 1 1 0 1 1 1 0 0 0 0 0 1 0]\n\n")
    assert captured_output.getvalue() == test_str

    # Assert ValueErrors are raised
    with pytest.raises(ValueError):
        analysis = analyze_dtmc(P, state_values, sim_kwargs={"no_ts_len": 0})
    with pytest.raises(ValueError):
        analysis = analyze_dtmc(P, state_values, trans_kwargs={"no_ts_len": 0})
    with pytest.raises(ValueError):
        analysis = analyze_dtmc(P, state_values, cost_kwargs={"no_ts_len": 0})
    with pytest.raises(ValueError):
        analysis = analyze_dtmc(P, state_values,
                                cost_kwargs={"no_transition": 0})
    with pytest.raises(ValueError):
        analysis = analyze_dtmc(P, state_values,
                                cost_kwargs={"no_state": 0, "transition": 0})


def test_computer_repair():
    """
    One worker requires 2 days to repair a machine, and there are 2 of them.
    They fail as independent events: 0.2 to fail, 0.8 to not fail within
        the day.
    We use the binomial distribution to model the event of 0, 1, or 2 failures.
    There are 5 possible states, which we will define as (s_1, s_2):
        s_1 = num days first machine been in shop
        s_2 = num days second has been in shop
        s_1 = 0 if machine not failed, 1 if in first day of repair, 2 if second
        The 5 possible states: (0,0), (1,0), (2,0), (1,1), (2,1)
    """
    # Failure of computers is binomial
    #   p = 0.2 and n = 2
    pmf = scipy.stats.binom.pmf(k=[0, 1, 2], n=2, p=0.2)
    p_0, p_1, p_2 = pmf[0], pmf[1], pmf[2]
    # Define trainsition matrix
    transition_matrix = [[p_0, p_1, 0.0, p_2, 0.0],
                         [0.0, 0.0, 0.8, 0.0, 0.2],
                         [0.8, 0.2, 0.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0, 1.0],
                         [0.0, 1.0, 0.0, 0.0, 0.0]]
    states = [(0, 0), (1, 0), (2, 0), (1, 1), (2, 1)]
    analysis = analyze_dtmc(P=transition_matrix, states=states)
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_markov(analysis)
    sys.stdout = sys.__stdout__  # reset stdout
    test_str = ("CDFs:\n"
                "[[0.64 0.96 0.96 1.   1.  ]\n"
                " [0.   0.   0.8  0.8  1.  ]\n"
                " [0.8  1.   1.   1.   1.  ]\n"
                " [0.   0.   0.   0.   1.  ]\n"
                " [0.   1.   1.   1.   1.  ]]\n\n"
                "Steady State Probs:\n"
                "[0.45351474 0.25510204 0.20408163 0.01814059"
                " 0.069161  ]\n\n")
    assert captured_output.getvalue() == test_str


def test_light_bulb_replacement():
    """
    How many of the bulbs on average will have to be replaced each month?
        How much the budget for the repairs should be?
    Time of fauliure is uncertain
        variety of maintenance optioins
    failed bulbs are replaced monthly - use this for time intervals for dist
    """
    # Define state space, the age of the bulb
    state_space = [0, 1, 2, 3, 4]  # new, 1 month, 2 month, etc.
    num_states = len(state_space)
    num_bulbs = 1_000
    # probability of bulb failing based on age of bulb in months
    prob = [0.5, 0.1, 0.1, 0.1, 0.2]
    cdf = np.cumsum(prob)
    cond_prob = [p / (1 - cdf[ind - 1])
                 if ind > 0 else p for ind, p in enumerate(prob)]
    cond_prob[-1] = 1  # roundoff error overriding
    transition_matrix = np.zeros(shape=(num_states, num_states))
    transition_matrix[:, 0] = cond_prob
    for row in range(num_states - 1):
        transition_matrix[row, row + 1] = 1 - transition_matrix[row, 0]

    # Costs of inspecting & replacing light bulbs
    inspect_cost = 0.10
    replace_cost = 2
    test_cost_vector = [inspect_cost + replace_cost * transition_matrix[x, 0]
                        for x in range(num_states)]
    inspect_vector = [inspect_cost] * num_states
    replace_matrix = np.array([[replace_cost] * num_states]
                              + ([[0] * num_states] * (num_states - 1))).T

    # Transient probabilities
    #  all bulbs start at age 0 (new sign)
    #  estimate how many bulbs will be replaced during each of first 12 months?
    # q(n): probability dist for age of bulb at time n
    test_q = np.array([[1, 0, 0, 0, 0]])  # row 0 is q(0), row 1 is q(1), etc.
    # q_n = q_(n-1) * P
    for _ in range(1, 13):  # for the 12 months
        test_q = np.vstack((test_q, np.matmul(test_q[-1], transition_matrix)))
    # Calculate expected transient costs - don't include month 0
    exp_trans_cost = np.delete(np.matmul(test_q, test_cost_vector), 0)
    test_trans_cost = sum(exp_trans_cost) * num_bulbs
    print("test trans cost: ", test_trans_cost)
    num_replaced = int(sum(test_q[1:, 0]) * num_bulbs)
    print("Num Replaced: ", num_replaced)

    # Steady state probabilities
    # for discrete-time markov chains, as long as each state can be
    #  reached from every other state, the transient probabilities
    #  will approach equilibrium.
    markov_obj = MarkovChain(P=transition_matrix, state_values=state_space)
    test_steady_state = markov_obj.stationary_distributions
    print('steady state: ', test_steady_state)

    analysis = analyze_dtmc(transition_matrix, state_space,
                            trans_kwargs={"ts_length": 12,
                                          "init": [1, 0, 0, 0, 0]},
                            cost_kwargs={"state": inspect_vector,
                                         "transition": replace_matrix,
                                         "num": num_bulbs})
    test = {
        'cdfs': np.array(
            [[0.5, 1., 1., 1., 1.],
             [0.2, 0.2, 1., 1., 1.],
             [0.25, 0.25, 0.25, 1., 1.],
             [0.33333333, 0.33333333, 0.33333333, 0.33333333, 1.],
             [1., 1., 1., 1., 1.]]),
        'steady_state': {
            'cost': {'kwargs': {'num': 1000,
                                'state': [0.1, 0.1, 0.1, 0.1, 0.1],
                                'transition': np.array([[2, 0, 0, 0, 0],
                                                        [2, 0, 0, 0, 0],
                                                        [2, 0, 0, 0, 0],
                                                        [2, 0, 0, 0, 0],
                                                        [2, 0, 0, 0, 0]])},
                     'total': 933.3333333333333,
                     'vector': 0.9333333333333332},
            'output': np.array(
                [0.41666667, 0.20833333, 0.16666667, 0.125, 0.08333333])},
        'transient': {
            'cost': {'kwargs': {'num': 1000,
                                'state': [0.1, 0.1, 0.1, 0.1, 0.1],
                                'transition': np.array([[2, 0, 0, 0, 0],
                                                        [2, 0, 0, 0, 0],
                                                        [2, 0, 0, 0, 0],
                                                        [2, 0, 0, 0, 0],
                                                        [2, 0, 0, 0, 0]])},
                     'total': 12009.303421875004,
                     'vector': np.array([1.1, 0.8, 0.75, 0.795, 1.0825,
                                         0.99575, 0.920625, 0.8976375,
                                         0.90770625, 0.95175438,
                                         0.94762406, 0.93364684,
                                         0.92705939])},
            'kwargs': {'init': [1, 0, 0, 0, 0], 'ts_length': 12},
            'output': np.array(
                [[1., 0., 0., 0., 0.],
                 [0.5, 0.5, 0., 0., 0.],
                 [0.35, 0.25, 0.4, 0., 0.],
                 [0.325, 0.175, 0.2, 0.3, 0.],
                 [0.3475, 0.1625, 0.14, 0.15, 0.2],
                 [0.49125, 0.17375, 0.13, 0.105, 0.1],
                 [0.447875, 0.245625, 0.139, 0.0975, 0.07],
                 [0.4103125, 0.2239375, 0.1965, 0.10425, 0.065],
                 [0.39881875, 0.20515625, 0.17915, 0.147375, 0.0695],
                 [0.40385313, 0.19940938, 0.164125, 0.1343625, 0.09825],
                 [0.42587719, 0.20192656, 0.1595275, 0.12309375, 0.089575],
                 [0.42381203, 0.21293859, 0.16154125, 0.11964563, 0.0820625],
                 [0.41682342, 0.21190602, 0.17035088, 0.12115594, 0.07976375]]
                )}}
    # Assert two dictionaries have equal values
    assert all(is_analysis_equal(analysis, test))
    # Assert that both have the same keys
    assert test.keys() == analysis.keys()
    assert test['steady_state'].keys() == analysis["steady_state"].keys()
    assert test['steady_state']['cost'].keys() == \
        analysis['steady_state']['cost'].keys()
    assert test['steady_state']['cost']['kwargs'].keys() == \
        analysis['steady_state']['cost']['kwargs'].keys()

    assert test['transient'].keys() == analysis["transient"].keys()
    assert test['transient']["kwargs"].keys() == \
        analysis["transient"]["kwargs"].keys()
    assert test['transient']['cost'].keys() == \
        analysis['transient']['cost'].keys()
    assert test['transient']['cost']['kwargs'].keys() == \
        analysis['transient']['cost']['kwargs'].keys()

    # Test print_markov
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_markov(analysis)
    sys.stdout = sys.__stdout__  # reset stdout
    test_str = ("CDFs:\n"
                "[[0.5        1.         1.         1.         1.        ]\n"
                " [0.2        0.2        1.         1.         1.        ]\n"
                " [0.25       0.25       0.25       1.         1.        ]\n"
                " [0.33333333 0.33333333 0.33333333 0.33333333 1.        ]\n"
                " [1.         1.         1.         1.         1.        ]]\n"
                "\nSteady State Probs:\n"
                "[0.41666667 0.20833333 0.16666667 0.125      0.08333333]\n\n"
                "Transient Probabilities (length 12)\n"
                "Initial Conditions:\n"
                "[1, 0, 0, 0, 0]\n"
                "Output:\n"
                "[[1.         0.         0.         0.         0.        ]\n"
                " [0.5        0.5        0.         0.         0.        ]\n"
                " [0.35       0.25       0.4        0.         0.        ]\n"
                " [0.325      0.175      0.2        0.3        0.        ]\n"
                " [0.3475     0.1625     0.14       0.15       0.2       ]\n"
                " [0.49125    0.17375    0.13       0.105      0.1       ]\n"
                " [0.447875   0.245625   0.139      0.0975     0.07      ]\n"
                " [0.4103125  0.2239375  0.1965     0.10425    0.065     ]\n"
                " [0.39881875 0.20515625 0.17915    0.147375   0.0695    ]\n"
                " [0.40385313 0.19940938 0.164125   0.1343625  0.09825   ]\n"
                " [0.42587719 0.20192656 0.1595275  0.12309375 0.089575  ]\n"
                " [0.42381203 0.21293859 0.16154125 0.11964563 0.0820625 ]\n"
                " [0.41682342 0.21190602 0.17035088 0.12115594 0.07976375]]\n"
                "\nCost kwargs:\n"
                "{'state': [0.1, 0.1, 0.1, 0.1, 0.1], 'transition': "
                "array([[2, 0, 0, 0, 0],\n"
                "       [2, 0, 0, 0, 0],\n"
                "       [2, 0, 0, 0, 0],\n"
                "       [2, 0, 0, 0, 0],\n"
                "       [2, 0, 0, 0, 0]]), 'num': 1000}\n"
                "Expected Steady State Cost:\n"
                "$0.93\n"
                "Expected Total Steady State Cost: $933.33\n"
                "Expected Transient Cost:\n"
                "[1.1        0.8        0.75       0.795      1.0825"
                "     0.99575\n"
                " 0.920625   0.8976375  0.90770625 0.95175438 0.94762406"
                " 0.93364684\n"
                " 0.92705939]\n"
                "Expected Total Transient Cost: $12,009.30\n")
    assert captured_output.getvalue() == test_str


def is_analysis_equal(analysis, test):
    is_equal = []
    for k in analysis:
        if type(analysis[k]) is dict:
            is_equal.extend(is_analysis_equal(analysis[k], test[k]))
        elif type(analysis[k]) in [np.float64, float, int]:
            is_equal.append(round(analysis[k], 5) == round(test[k], 5))
        elif type(analysis[k]) is str:
            is_equal.append(analysis[k] == test[k])
        elif type(analysis[k]) is np.ndarray:
            is_equal.append(np.allclose(analysis[k], test[k]))
        elif type(analysis[k]) is list:
            is_equal.append(all(a == b for a, b in zip(analysis[k], test[k])))
    return is_equal


def test_atm_example():
    arrival_rate = 2  # per minute
    service_rate = 2.5  # per minute
    states = [0, 1, 2, 3, 4, 5]
    num_states = len(states)
    rate_matrix = []
    for row in states:
        this_row = [arrival_rate if col == row + 1 else 0 for col in states]
        if row >= 1:
            this_row[row - 1] = service_rate
        rate_matrix.append(this_row)
    rate_matrix = np.array(rate_matrix)

    # transient solutions
    # have to use numerical approcaches, no closed form in general
    # QuantEcon only has finite state discrete time MarkovChain
    # DTMC approximation (not embedded here)
    d = 0.05  # small time interval, a parameter
    t = 1  # want to approx. transient probs at this time, a parameter
    n = int(t / d)  # number of steps - determines accuracy of approx.
    # alpha_i is sum of transition rates out of state i
    alpha = rate_matrix.sum(axis=1)  # sum across cols
    # P is state-transition matrix determined from rate matrix & d
    P = [[1 - d*alpha[col] if row == col else d * rate_matrix[row, col]
          for col in states] for row in states]
    P = np.array(P)
    # prob that system in state i at time t: q_i(t)
    # q(t) = [q_0(t), q_1(t), ..., q_(m-1)(t)]
    # Note sum(q_t) == 1
    # Initial probability vector:
    q_init = [1, 0, 0, 0, 0, 0]
    # transient sol. approx. at time t = n*d with DTMC
    #   by solving following equation:
    # eq = q(n*d) == q(0)P^(n)
    # or q(n*d + d) == q(n*d)P
    q_step = np.matmul(q_init, np.linalg.matrix_power(P, n))

    # My analysis
    analysis = analyze_ctmc(states=states, rate_matrix=rate_matrix,
                            t=t, d=d, init=q_init)
    assert (analysis['transient'] == q_step).all()

    # Steady State probabilities
    # limit of q(t) as t goes to infinity
    # generator matrix
    gen_matrix = [[-alpha[row] if row == col else rate_matrix[row, col]
                   for col in states] for row in states]
    gen_matrix = np.array(gen_matrix)
    # augmented generator matrix - replace first col with 1s
    gen_matrix[:, 0] = np.ones(num_states)
    # Solve linear equations for steady state probs
    unit_vector = np.zeros(num_states)
    unit_vector[0] = 1
    steady_state = np.matmul(unit_vector.T, np.linalg.inv(gen_matrix))
    assert (analysis['steady_state'] == steady_state).all()

    no_d_analysis = analyze_ctmc(states=states, rate_matrix=rate_matrix,
                                 t=t, n=n, init=q_init)
    assert all(is_analysis_equal(analysis, no_d_analysis))
    no_t_analysis = analyze_ctmc(states=states, rate_matrix=rate_matrix,
                                 n=n, d=d, init=q_init)
    assert all(is_analysis_equal(analysis, no_t_analysis))

    with pytest.raises(ValueError):
        analyze_ctmc(states=states, rate_matrix=rate_matrix, t=t, init=q_init)
    with pytest.raises(ValueError):
        analyze_ctmc(states=states, rate_matrix=rate_matrix, d=d, init=q_init)
    with pytest.raises(ValueError):
        analyze_ctmc(states=states, rate_matrix=rate_matrix, n=n, init=q_init)
    with pytest.raises(ValueError):
        analyze_ctmc(states=states, rate_matrix=rate_matrix, t=3, d=1,
                     n=5, init=q_init)

    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_markov(analysis, mtype="ctmc")
    sys.stdout = sys.__stdout__  # reset stdout
    test_str = ("Transition Rates:\n"
                "[2.  4.5 4.5 4.5 4.5 2.5]\n"
                "P:\n"
                "[[0.9   0.1   0.    0.    0.    0.   ]\n"
                " [0.125 0.775 0.1   0.    0.    0.   ]\n"
                " [0.    0.125 0.775 0.1   0.    0.   ]\n"
                " [0.    0.    0.125 0.775 0.1   0.   ]\n"
                " [0.    0.    0.    0.125 0.775 0.1  ]\n"
                " [0.    0.    0.    0.    0.125 0.875]]\n"
                "Steady State:\n"
                "[0.2710556  0.21684448 0.17347558 0.13878047 0.11102437"
                " 0.0888195 ]\n"
                "Initial States:\n"
                "[1, 0, 0, 0, 0, 0]\n"
                "Transient Probabilities:\n"
                "[0.43253628 0.29099199 0.16203962 0.0745227  0.02883399"
                " 0.01107543]\n"
                "Generator Matrix:\n"
                "[[ 1.   2.   0.   0.   0.   0. ]\n"
                " [ 1.  -4.5  2.   0.   0.   0. ]\n"
                " [ 1.   2.5 -4.5  2.   0.   0. ]\n"
                " [ 1.   0.   2.5 -4.5  2.   0. ]\n"
                " [ 1.   0.   0.   2.5 -4.5  2. ]\n"
                " [ 1.   0.   0.   0.   2.5 -2.5]]\n")
    assert captured_output.getvalue() == test_str
