.. include:: ../roles.rst

.. _api_reference:

API Library Reference
=====================

The current models are implemented under :py:mod:`ormm.mathprog`, :py:mod:`ormm.network`, and
:py:mod:`ormm.markov`.  MathProg contains
factory methods to implement problem classes and other useful functions for
solution analysis.  Markov contains functions to perform markov analysis on
discrete state and time processes, as well as printing those results nicely.  Network contains
models and methods for the transportation problem and the shortest path tree problem.

ORMM MathProg
-------------
.. currentmodule:: ormm.mathprog

.. autosummary::

   blending
   resource_allocation
   scheduling
   print_sol
   sensitivity_analysis

.. autofunction:: blending

.. autofunction:: resource_allocation

.. autofunction:: scheduling

.. autofunction:: print_sol

.. autofunction:: sensitivity_analysis

ORMM Markov
-----------
.. currentmodule:: ormm.markov

.. autosummary::

   analyze_dtmc
   analyze_ctmc
   print_markov

.. autofunction:: analyze_dtmc

.. autofunction:: analyze_ctmc

.. autofunction:: print_markov

ORMM Network
------------
.. currentmodule:: ormm.network

.. autosummary::

   transportation_model
   Graph

.. autofunction:: transportation_model

.. autoclass:: Graph