import io
import sys

from quantecon.markov import MarkovChain
import scipy.stats
import numpy as np
from ormm.markov import markov_analysis, print_markov


def test_income_audit():
    """A simple example of markov chain"""
    # Define MarkovChain object - P is transition matrix
    P = [[0.6, 0.4], [0.5, 0.5]]
    state_values = [0, 1]
    analysis = markov_analysis(P, state_values,
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
    analysis = markov_analysis(P=transition_matrix, state_values=states)
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


def light_bulb_replace():
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
    print(inspect_cost)
    print(replace_cost)
    print(transition_matrix)
    print(test_cost_vector)

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
    num_replaced = int(sum(test_q[1:, 0]) * num_bulbs)
    print("Transient Probabilities:")
    print(test_q)
    print("test cost vector")
    print(test_cost_vector)
    print("exp trans cost vector?")
    print(exp_trans_cost)
    print(f"Expected Total Transient Cost: ${test_trans_cost:,.2f}")
    print(f"Expected # of Replacements: {num_replaced:,d}")

    # Steady state probabilities
    # for discrete-time markov chains, as long as each state can be
    #  reached from every other state, the transient probabilities
    #  will approach equilibrium.
    markov_obj = MarkovChain(P=transition_matrix, state_values=state_space)
    test_steady_state = markov_obj.stationary_distributions
    print(f"Stationary probs: {test_steady_state[0]}")

    analysis = markov_analysis(transition_matrix, state_space,
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
    # Assert that numpy arrays are the same (except sim & stdy state output)
    assert all([np.allclose(analysis[k], test[k])
                for k in analysis if k not in ['transient', 'steady_state']])
    # Assert cost totals are the same
    assert all([analysis[k]['cost']['total'] ==
               test[k]['cost']['total']
               for k in ['transient', 'steady_state']])
    # assert transient kwargs values are the same
    assert all([test["transient"]["kwargs"][k] ==
               analysis["transient"]["kwargs"][k]
               for k in analysis["transient"]["kwargs"]])
    # Assert that transient output numpy arrays are the same
    assert np.allclose(analysis["transient"]["output"],
                       test["transient"]["output"])
    # Assert that steady state output numpy arrays are the same
    assert np.allclose(analysis["steady_state"]["output"],
                       test["steady_state"]["output"])
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
    print("---------------------------")
    print_markov(analysis)


if __name__ == "__main__":
    light_bulb_replace()
