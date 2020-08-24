Markov Analysis
===============
This subpackage provides methods for performing analyis on
discrete-state Markovian processes.
A Markov process is a stochastic process that holds the Markovian Property,
both of which are described in the definitions below.

1. Stochastic Process:  A collection of random variables :math:`\{X_t\}`,
   where :math:`t` is a time index that takes values from a given set
   :math:`T` ([Jensen-Bard]_, P. 413).
2. Markovian Property:  Given that the current state is known, the conditional
   probability of the next state is independent of the states prior to the
   current state ([Jensen-Bard]_, P. 413).

There are discrete and continuous time Markov processes.  Discrete time ones
are commonly called Markov Chains.

These processes can be represented by labels for the possible states (or
a state space :math:`S`) and a transition matrix :math:`P`.  The transition
matrix details the probabilities of moving from one state to another - thus,
it must be of size :math:`m \times m`, where :math:`m` is the number of states
in the state space :math:`S`.

There are many ways to analyze a Markovian system, including simulation,
transient probabilities, steady state probabilities, and cost analysis.
The :py:obj:`markov_analyis` method can be passed dictionaries of key word
arguments to add these details to the returned analysis.

.. toctree::
   :maxdepth: 2

   discrete.rst

.. [Jensen-Bard] Jensen, P. A., & Bard, J. F. (2002). Operations Research Models
   and Methods. Wiley.