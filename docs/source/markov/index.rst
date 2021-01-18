Markov Analysis
===============
This subpackage provides methods for performing analyis on
discrete-state Markovian processes.  While some refer to a discrete
time Markov process as a Markov Chain, in this package a Markov Chain refers to
a discrete state Markov process.
This is so that we can refer to them as continuous time or
discrete time Markov Chains, since this package currently only
considers discrete states.

A Markov process is a stochastic process that holds the Markovian Property,
both of which are described in the definitions below.

1. Stochastic Process:  A collection of random variables :math:`\{X_t\}`,
   where :math:`t` is a time index that takes values from a given set
   :math:`T` ([1]_, P. 413).
2. Markovian Property:  Given that the current state is known, the conditional
   probability of the next state is independent of the states prior to the
   current state ([1]_, P. 413).

These processes can be represented by labels for the possible states (or
a state space :math:`S`) and a transition matrix :math:`P`.  The transition
matrix details the probabilities of moving from one state to another - thus,
it must be of size :math:`m \times m`, where :math:`m` is the number of states
in the state space :math:`S`.

There are many ways to analyze a Markovian system, including simulation,
transient probabilities, steady state probabilities, and cost analysis.
The :py:obj:`analyze_dtmc` and :py:obj:`analyze_ctmc` methods can be passed
dictionaries of key word arguments to add these details to the returned analysis.

The set :math:`T` of periods needs to be finite for simulations or
transient probability analyis, but steady state probabilities assess
the distribution of the states in the long term.  Note that steady state
probabilities are the eigenvectors of the transition matrix :math:`P`
corresponding to the eigenvalue 1.

.. toctree::
   :maxdepth: 2

   discrete.rst

.. [1] Jensen, P. A., & Bard, J. F. (2002). Operations Research Models
   and Methods. Wiley.