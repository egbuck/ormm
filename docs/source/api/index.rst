.. include:: ../roles.rst

.. _api_reference:

API Library Reference
=====================

The current models are implemented under :py:mod:`ormm.mathprog` and
:py:mod:`ormm.markov`.  MathProg contains
factory methods to implement problem classes and other useful functions for
solution analysis.  Markov contains functions to perform markov analysis on
discrete state and time processes, as well as printing those results nicely.

ORMM MathProg
-------------
.. currentmodule:: ormm.mathprog

.. autosummary::

   blending
   resource_allocation
   scheduling
   print_sol
   sensitivity_analysis
   transportation

.. autofunction:: blending

.. autofunction:: resource_allocation

.. autofunction:: scheduling

.. autofunction:: transportation

.. autofunction:: print_sol

.. autofunction:: sensitivity_analysis

ORMM Markov
-----------
.. currentmodule:: ormm.markov

.. autosummary::

   analyze_dtmc
   print_markov

.. autofunction:: analyze_dtmc

.. autofunction:: print_markov
