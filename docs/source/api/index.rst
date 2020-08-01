.. include:: ../roles.rst

.. _api_reference:

API Library Reference
=====================

The current models are implemented under :py:mod:`ormm.mathprog`, which only contains
the :py:func:`print_sol` method and the :py:func:`resource_allocation` factory method for now.

.. currentmodule:: ormm.mathprog

.. autosummary::

   resource_allocation
   print_sol
   sensitivity_analysis


API Component Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: resource_allocation

.. autofunction:: print_sol

.. autofunction:: sensitivity_analysis