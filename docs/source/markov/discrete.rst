Discrete Time Analysis
=======================
In a Discrete Time Markov Chain, the set :math:`T` is made up of
discrete time intervals (ex: period 1, 2, 3, etc.).
This works well for systems where events occur in steps or specified
intervals of time.  These could be
months, years, weeks, days, hours, or other time interval choices.

In Markov Chains, we only care about the states at the end of
each of the time intervals.

Usage Example
-------------
Consider a store that has a lit-up sign for displaying the name of the
store to potential customers driving by.  Assume that the sign has
1,000 of these special bulbs to make the sign brighter.  Your boss may
notice the bulbs burning out more than they expected, and wants to know
if this was just by chance or if this behavior is expected in the long term
future.  They also would like an analysis on the expected cost of replacing these
light bulbs.

The code below will return a dictionary with the results of this analysis.

.. code-block:: python

   >>> from ormm.markov import markov_analysis, print_markov
   >>> import numpy as np
   >>>
   >>> # Probability of bulb failing based on age of bulb in months
   >>> prob = [0.5, 0.1, 0.1, 0.1, 0.2]
   >>> cdf = np.cumsum(prob)
   >>> cond_prob = [p / (1 - cdf[ind - 1])
   >>>              if ind > 0 else p for ind, p in enumerate(prob)]
   >>> cond_prob[-1] = 1  # roundoff error overriding
   >>>
   >>> # Create state space and transition probability arrays
   >>> state_space = [0, 1, 2, 3, 4]
   >>> num_states = len(state_space)
   >>> num_bulbs = 1_000
   >>> transition_matrix = np.zeros(shape=(num_states, num_states))
   >>> transition_matrix[:, 0] = cond_prob
   >>> for row in range(num_states - 1):
   ...     transition_matrix[row, row + 1] = 1 - transition_matrix[row, 0]
   >>> transition_matrix
   array([[0.5       , 0.5       , 0.        , 0.        , 0.        ],
          [0.2       , 0.        , 0.8       , 0.        , 0.        ],
          [0.25      , 0.        , 0.        , 0.75      , 0.        ],
          [0.33333333, 0.        , 0.        , 0.        , 0.66666667],
          [1.        , 0.        , 0.        , 0.        , 0.        ]])
   >>>
   >>> # Create cost parameters
   >>> inspect_cost = 0.10
   >>> replace_cost = 2
   >>> inspect_vector = [inspect_cost] * num_states
   >>> inspect_vector
   [0.1, 0.1, 0.1, 0.1, 0.1]
   >>> replace_matrix = np.array([[replace_cost] * num_states]
   ...                           + ([[0] * num_states] * (num_states - 1))).T
   >>> replace_matrix
   array([[2, 0, 0, 0, 0],
          [2, 0, 0, 0, 0],
          [2, 0, 0, 0, 0],
          [2, 0, 0, 0, 0],
          [2, 0, 0, 0, 0]])
   >>>
   >>> # Run Markov Analysis
   >>> analysis = markov_analysis(transition_matrix, state_space,
   ...                            trans_kwargs={"ts_length": 12,
   ...                                          "init": [1, 0, 0, 0, 0]},
   ...                            cost_kwargs={"state": inspect_vector,
   ...                                         "transition": replace_matrix,
   ...                                         "num": num_bulbs}
   >>> print_markov(analysis)
   CDFs:
   [[0.5        1.         1.         1.         1.        ]
    [0.2        0.2        1.         1.         1.        ]
    [0.25       0.25       0.25       1.         1.        ]
    [0.33333333 0.33333333 0.33333333 0.33333333 1.        ]
    [1.         1.         1.         1.         1.        ]]

   Steady State Probs:
   [0.41666667 0.20833333 0.16666667 0.125      0.08333333]

   Transient Probabilities (length 12)
   Initial Conditions:
   [1, 0, 0, 0, 0]
   Output:
   [[1.         0.         0.         0.         0.        ]
    [0.5        0.5        0.         0.         0.        ]
    [0.35       0.25       0.4        0.         0.        ]
    [0.325      0.175      0.2        0.3        0.        ]
    [0.3475     0.1625     0.14       0.15       0.2       ]
    [0.49125    0.17375    0.13       0.105      0.1       ]
    [0.447875   0.245625   0.139      0.0975     0.07      ]
    [0.4103125  0.2239375  0.1965     0.10425    0.065     ]
    [0.39881875 0.20515625 0.17915    0.147375   0.0695    ]
    [0.40385313 0.19940938 0.164125   0.1343625  0.09825   ]
    [0.42587719 0.20192656 0.1595275  0.12309375 0.089575  ]
    [0.42381203 0.21293859 0.16154125 0.11964563 0.0820625 ]
    [0.41682342 0.21190602 0.17035088 0.12115594 0.07976375]]

   Cost kwargs:
   {'state': [0.1, 0.1, 0.1, 0.1, 0.1], 'transition': array([[2, 0, 0, 0, 0],
          [2, 0, 0, 0, 0],
          [2, 0, 0, 0, 0],
          [2, 0, 0, 0, 0],
          [2, 0, 0, 0, 0]]), 'num': 1000}
   Expected Steady State Cost:
   $0.93
   Expected Total Steady State Cost: $933.33
   Expected Transient Cost:
   [1.1        0.8        0.75       0.795      1.0825     0.99575
    0.920625   0.8976375  0.90770625 0.95175438 0.94762406 0.93364684
    0.92705939]
   Expected Total Transient Cost: $12,009.30
