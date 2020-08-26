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

>>> from ormm.markov import markov_analysis, print_markov
>>> import pyomo.environ as pyo
>>> import numpy as np
>>>
>>> # Create state space and transition probability arrays
>>> state_space = [0, 1, 2, 3, 4]
>>> num_states = len(state_space)
>>> num_bulbs = 1_000
>>> transition_matrix = np.zeros(shape=(num_states, num_states))
>>> transition_matrix[:, 0] = cond_prob
>>> for row in range(num_states - 1):
>>>     transition_matrix[row, row + 1] = 1 - transition_matrix[row, 0]
>>> transition_matrix
[[]]
>>> # Create cost parameters
>>> inspect_cost = 0.10
>>> replace_cost = 2
>>> inspect_vector = [inspect_cost] * num_states
>>> inspect_vector
[]
>>> replace_matrix = np.array([[replace_cost] * num_states]
...                           + ([[0] * num_states] * (num_states - 1))).T
>>> replace_matrix
[[]]
>>> # Run Markov Analysis
>>> analysis = markov_analysis(transition_matrix, state_space,
...                            trans_kwargs={"ts_length": 12,
...                                          "init": [1, 0, 0, 0, 0]},
...                            cost_kwargs={"state": inspect_vector,
...                                         "transition": replace_matrix,
...                                         "num": num_bulbs}
>>> print_markov(analysis)
