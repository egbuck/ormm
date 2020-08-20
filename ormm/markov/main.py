from quantecon import MarkovChain
import numpy as np


def markov_analysis(P, state_values=None, sim_kwargs=None,
                    trans_kwargs=None, cost_kwargs=None):
    """
    Perform Markov Analysis of costs, steady state, & transient probabilities.

    Parameters
    ----------
    P : array-like
        The transition matrix.  Must be of shape n x n.
    state_values : array-like
        Array_like of length n containing the values associated with the
        states, which must be homogeneous in type. If None, the values
        default to integers 0 through n-1.
    sim_kwargs : dict
        Dictionary of key word arguments to be passed to the simulation
        of the markov process.  If None, then no simulation will be performed.
        These include ts_length (length of each
        simulation) and init (Initial state values).
    trans_kwargs : dict
        Dictionary of options for the transient probability analysis (tsa).
        If None is passed instead of dict, no tsa will be done.
        ts_length is the number of time periods to analyze, while init is
        the initial state probability vector.
    cost_kwargs : dict
        Dictionary of cost parameters for cost analysis.  If None, then
        no cost analysis will be performed.  These include state (vector of
        costs of being in each state), transition (matrix of costs of
        transitioning from one state to another), and num (number of
        these processes - total cost multiplied by this, default 1).

    Returns
    -------
    analysis : dict
        Dictionary with results of markov analysis

    Raises
    ------
    ValueError
        If sim_kwargs, trans_kwargs, or cost_kwargs is given, but their
        required arguments are not passed.  These are

        - sim_kwargs: `ts_length` is required, the length of the sim.
        - trans_kwargs: `ts_length` is required, the number of periods
          to analyze
        - cost_kwargs: `state` and `transition` are required, which are the
          costs of being in any state and the costs of transitioning from one
          state to another.
    """
    analysis = {}
    markov = MarkovChain(P, state_values)
    analysis["cdfs"] = markov.cdfs
    steady_state = markov.stationary_distributions[0]
    analysis["steady_state"] = {"output": steady_state}
    if sim_kwargs:
        if "ts_length" not in sim_kwargs:
            raise ValueError(("Required argument `ts_length` in sim_kwargs! "
                              "None was given."))
        if "init" not in sim_kwargs:
            sim_kwargs["init"] = None
        analysis["sim"] = {"kwargs": sim_kwargs,
                           "output": markov.simulate(**sim_kwargs)}
    if trans_kwargs:
        if "ts_length" not in trans_kwargs:
            raise ValueError(("Required argument `ts_length` in trans_kwargs! "
                              "None was given."))
        if "init" not in trans_kwargs:
            trans_kwargs["init"] = None
        trans_probs = _transient_probs(P, state_values, **trans_kwargs)
        analysis["transient"] = {"kwargs": trans_kwargs,
                                 "output": trans_probs}
    if cost_kwargs:
        if "state" not in cost_kwargs:
            raise ValueError(("Required argument `state` in trans_kwargs! "
                              "None was given."))
        if "transition" not in cost_kwargs:
            raise ValueError(("Required argument `transition` in trans_kwargs!"
                              " None was given."))
        if "num" not in cost_kwargs:
            cost_kwargs["num"] = 1
        # Cost of steady state
        cost_vector, cost_total = _cost_analysis(P, steady_state,
                                                 **cost_kwargs)
        # Cost of transient analysis
        analysis["steady_state"]["cost"] = \
            {"kwargs": cost_kwargs,
             "total": cost_total, "vector": cost_vector}
        if trans_kwargs:
            cost_vector, cost_total = _cost_analysis(P, trans_probs,
                                                     **cost_kwargs)
            analysis["transient"]["cost"] = {"kwargs": cost_kwargs,
                                             "total": cost_total,
                                             "vector": cost_vector}
    return analysis


def _cost_analysis(P, probs, state, transition, num):
    """
    Cost analysis for markov process

    probs could be transient or steady state
    """
    # Get cost vector - element wise mult, sum across cols
    cost_vector = state + np.sum(transition * P, 1)

    # Calculate expected costs
    exp_cost = np.matmul(probs, cost_vector)
    total_cost = np.sum(exp_cost) * num
    return exp_cost, total_cost


def _transient_probs(P, state_values, ts_length, init=None):
    """
    Calculate transient probabilities

    q(n): probability dist at time n
        q(n) = q(n-1) * P
    """
    if init is None:
        init = [np.random.choice(state_values, size=P.shape[0])]
    q = np.array([init])
    # q_n = q_(n-1) * P
    for _ in range(1, ts_length + 1):
        q = np.vstack((q, np.matmul(q[-1], P)))
    return q


def print_markov(analysis):
    """
    Print analysis from markov analysis

    Parameters
    ----------
    analysis : dict
        dictionary returned from markov_analysis() containing
        cdfs, steady state probs, etc.
    """
    print("CDFs:")
    print(analysis["cdfs"])
    print()
    print("Steady State Probs:")
    print(analysis["steady_state"]['output'])
    print()
    if "sim" in analysis:
        print(("Simulation of length "
               f"{analysis['sim']['kwargs']['ts_length']}"))
        print("Initial Conditions:")
        print(analysis["sim"]["kwargs"]["init"])
        print("Output:")
        print(analysis["sim"]["output"])
        print()
    if "transient" in analysis:
        print(("Transient Probabilities (length "
              f"{analysis['transient']['kwargs']['ts_length']})"))
        print("Initial Conditions:")
        print(analysis["transient"]["kwargs"]["init"])
        print("Output:")
        print(analysis["transient"]["output"])
        print()
    if "cost" in analysis['steady_state']:
        print("Cost kwargs:")
        print(analysis['steady_state']['cost']['kwargs'])
        print("Expected Steady State Cost:")
        print(analysis['steady_state']['cost']['vector'])
        print(("Expected Total Steady State Cost: $"
              f"{analysis['steady_state']['cost']['total']:,.2f}"))
    if "transient" in analysis:
        if "cost" in analysis['transient']:
            print("Expected Transient Cost:")
            print(analysis["transient"]['cost']['vector'])
            print(("Expected Total Transient Cost: $"
                  f"{analysis['transient']['cost']['total']:,.2f}"))
