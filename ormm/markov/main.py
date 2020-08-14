from quantecon import MarkovChain


def markov_analysis(P, state_values=None,
                    sim_kwargs={"ts_length": 25, "init": None}):
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
        of the markov process.  These include ts_length (length of each
        simulation) and init (Initial state values).
    """
    markov = MarkovChain(P, state_values)
    print(f"Cdfs: {markov.cdfs}")
    steady_state = markov.stationary_distributions
    print(f"Steady State Probs: {steady_state}")
    print(f"Simulation of length {sim_kwargs['ts_length']}:")
    print(markov.simulate(**sim_kwargs))
