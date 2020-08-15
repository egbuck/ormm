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
    """
    markov = MarkovChain(P, state_values)
    print(f"Cdfs: {markov.cdfs}")
    steady_state = markov.stationary_distributions
    print(f"Steady State Probs: {steady_state}")
    if sim_kwargs:
        print(f"Simulation of length {sim_kwargs['ts_length']}:")
        print(markov.simulate(**sim_kwargs))
    if trans_kwargs:
        trans_probs = _transient_probs(P, **trans_kwargs)
        print("Transient Probabilities:")
        print(trans_probs)
    if cost_kwargs:
        if "num" not in cost_kwargs:
            cost_kwargs["num"] = 1
        # Cost of steady state
        cost = _cost_analysis(steady_state, **cost_kwargs)
        print(f"Expected Total Steady State Cost: ${cost:,.2f}")
        # Cost of transient analysis
        if trans_kwargs:
            cost = _cost_analysis(trans_probs, **cost_kwargs)
            print(f"Expected Total Transient Cost: ${cost:,.2f}")


def _cost_analysis(P, probs, state, transition, num):
    """
    Cost analysis for markov process

    probs could be transient or steady state
    """
    # Get cost vector
    cost_vector = [state + transition * P[x, 0]
                   for x in range(transition.shape[0])]

    # Calculate expected transient costs - don't include month 0
    exp_trans_cost = np.delete(np.matmul(probs, cost_vector), 0)
    total_trans_cost = sum(exp_trans_cost) * num
    return total_trans_cost


def _transient_probs(P, ts_length, init):
    """
    Calculate transient probabilities

    q(n): probability dist at time n
        q(n) = q(n-1) * P
    """
    q = np.array(init)
    # q_n = q_(n-1) * P
    for _ in range(1, ts_length + 1):
        q = np.vstack((q, np.matmul(q[-1], P)))
    return q
