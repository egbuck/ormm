Continuous Time Analysis
========================
In a Continuous Time Markov Chain, the set :math:`T` is made up of
a continuous time interval.
The Markovian property is only satisfied with a continuous time interval
if all activity durations are exponentially distributed, such as an
:math:`M/M/s` queuing system.

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

   >>> from ormm.markov import analyze_ctmc
   >>> import numpy as np
   >>>
   >>> # Defining Parameters
   >>> arrival_rate = 2  # per minute
   >>> service_rate = 2.5  # per minute
   >>> states = [0, 1, 2, 3, 4, 5]
   >>> num_states = len(states)
   >>> rate_matrix = []
   >>> for row in states:
   >>>     this_row = [arrival_rate if col == row + 1 else 0 for col in states]
   >>>     if row >= 1:
   >>>         this_row[row - 1] = service_rate
   >>>     rate_matrix.append(this_row)
   >>> rate_matrix = np.array(rate_matrix)
   >>> d = 0.05  # small time interval, a parameter
   >>> t = 1  # want to approx. transient probs at this time, a parameter
   >>> n = int(t / d)  # number of steps - determines accuracy of approx.
   >>> q_init = [1, 0, 0, 0, 0, 0]
   >>>
   >>> # Run Analysis
   >>> analysis = analyze_ctmc(states=states, rate_matrix=rate_matrix,
   >>>                         t=t, d=d, init=q_init)
   >>> analysis
   {'transition_rates': array([2. , 4.5, 4.5, 4.5, 4.5, 2.5]),
    'P': array([[0.9  , 0.1  , 0.   , 0.   , 0.   , 0.   ],
                [0.125, 0.775, 0.1  , 0.   , 0.   , 0.   ],
                [0.   , 0.125, 0.775, 0.1  , 0.   , 0.   ],
                [0.   , 0.   , 0.125, 0.775, 0.1  , 0.   ],
                [0.   , 0.   , 0.   , 0.125, 0.775, 0.1  ],
                [0.   , 0.   , 0.   , 0.   , 0.125, 0.875]]),
    'init': [1, 0, 0, 0, 0, 0],
    'transient': array([0.43253628, 0.29099199, 0.16203962, 0.0745227,
                        0.02883399, 0.01107543]),
    'generator_matrix': array([[ 1. ,  2. ,  0. ,  0. ,  0. ,  0. ],
                               [ 1. , -4.5,  2. ,  0. ,  0. ,  0. ],
                               [ 1. ,  2.5, -4.5,  2. ,  0. ,  0. ],
                               [ 1. ,  0. ,  2.5, -4.5,  2. ,  0. ],
                               [ 1. ,  0. ,  0. ,  2.5, -4.5,  2. ],
                               [ 1. ,  0. ,  0. ,  0. ,  2.5, -2.5]]),
    'steady_state': array([0.2710556 , 0.21684448, 0.17347558, 0.13878047,
                           0.11102437, 0.0888195 ])}
