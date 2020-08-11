def markov(activities, events, random_vars={}, transition_function=None,
           state="discrete", time="discrete"):
    """
    type of stochastic process that is memoryless
        time: stochastic process has sequence of events that occur over time
        state: attributes of a system at some point in time
            ex: # of people in a system
            v component vector s={s_1,s_2,...,s_v} to describe the state
            ATM example: s={k} where k is # of people in system
            X_i: possible value of vector s at time i
                a random variable
            Set of all possible states: S, the state space

    A system has activities, which have some duration.
        An activity culminates in an event.
        Ex: `a` for arrival activicy/event
            `d` for service activity and its completion
    Duration of each activity is a random variable
        distribution may or may not be known
        this is probabilistic element of the stochastic process
        Ex: time for service t_d
            time for arrivals t_a
        can be described by cumulative distribution functions if known
            ex: F_d(t) = Pr{t_d \\leq t}

    Set of possible activities/events can depend on the state of the system
        Y(s) - set of possible activities/events for state s
        this is referenced as the calendar

    transition: describes the movement from the current state to the next state
        state-transition network: describes the components of the stoch. model
        complex situations, may use a transition function instead
            if more than one component, this is multidimensional

    Formal Definitions
    ------------------
    - A stochastic process is a collection of random variables {X_t},
      where t is a time index that takes values from a given set T.

    - Markovian Property: Given that the current state is known,
      the conditional probability of the next state is independent of the
      states prior to the current state.  A system that has this property
      is said to be memoryless because the future realization depends only
      on the current state and in no way on the past.
     -------------Discrete markov defs-------------------
    - Let S = {0, 1, ...} be the state space for a discrete-time Markov chain
      and let p_{i,j} be the probability of going from stae i to state j in
      one transition.  Then the state-transition matrix for the markov chain
      is P = (p_{ij}), where
      :math:`\\sum_{j \\in S} p_{ij} = 1 \\forall i \\in S
             \\text{ and } 0 \\leq p_{ij} \\leq 1 \\forall i,j \\in S`

    - A discrete-time Markov Chain (or Markov chain, for short) is a
      stochastic process with the following characteristics:
      1. A discrete state space
      2. Markovian property
      3. The one-step transition probabilities p_{ij}, from time n to
         time n+1 remain constant over time (termed stationary trainsition
         probabilities).
    """
    X = (e for e in events)
    if random_vars == {}:
        random_vars = {a: ((0.75, 0), (0.15, 0.6), (None, 1))
                       for a in activities}
    if transition_function is None:
        transition_function = default_transition
    return X, random_vars


def markov_discrete_time(
        activities, events, random_vars,
        transition_matrix, state="discrete"):
    """
    Discrete time version of markov chain
    """
    # n \in N is used for discrete time
    N = [0, 1, 2, 3, 4, 5]
    X = {n: 0 for n in N}
    random_vars = {a: ((0.75, 0), (0.15, 0.6), (None, 1))
                   for a in activities}
    transition_matrix = [[0.6, 0.3, 0.1],
                         [0.8, 0.2, 0.0],
                         [1.0, 0.0, 0.0]]
    return X, random_vars, transition_matrix


def default_transition(s, x):
    if x == 'a':
        return s + 1
    elif x == 'd':
        return s - 1
    else:
        raise ValueError
