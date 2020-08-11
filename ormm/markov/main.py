def markov(state="discrete", time="discrete"):
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
    """
    pass
