Rental Problem
===========================
The Rental Problem minimizes the cost of the plans purchased
while satisfying the number of units needed per period (the covering constraints).
The structure of this problem is very similar to the employee problem,
except for the addition of these plans, or options.
These plans can have different effective number of periods, and different costs
as a result.  Note that the "plan length" would be pseudo-equivalent to the :py:obj:`ShiftLength`
in the employee problem.  Additionally, these plans may be restricted to only having
certain start periods - for example, there may be a weekend plan that can only start
on Saturday (and is effective Saturday and Sunday).
This requires connecting the plans to the periods which they can start in, which is
done through the :py:obj:`PlanToPeriod` parameter.
This type of problem can arise when renting cars or other types of equipment.

Definitions
-----------

Sets
""""
- :py:obj:`Periods` - An ordered set of periods when the units are needed

   - :py:obj:`p in Periods` or :math:`p \in P`

- :py:obj:`Plans` - Set of plans that are available to rent units

   - :py:obj:`a in Plans` or :math:`a \in A`

- :py:obj:`PlanToPeriod` - A set that describes which periods a plan can start in.
  This set is 2 dimensions, consisting of tuples :math:`(p,a)`. Note that not all
  combinations of :math:`(p,a)` for :math:`p \in P`, :math:`a \in A` may exist
  in this set.

   - :py:obj:`(period, plan) in PlanToPeriod` or :math:`(p,a) \in J` or :math:`j \in J`

Parameters
""""""""""
- :py:obj:`PeriodReqs` - measure of number of units needed for :py:obj:`Period p`

   - :py:obj:`PeriodReqs[p] for p in Periods` or :math:`R_p \enspace \forall p \in P`

- :py:obj:`PlanCosts` - measure of the cost of reunting one unit under :py:obj:`Plan a`

   - :py:obj:`PeriodReqs[a] for p in Periods` or :math:`C_a \enspace \forall a \in A`

- :py:obj:`PlanLengths` - measure of how many periods in a row a :py:obj:`Plan a`
  is effective for

   - :py:obj:`PlanLengths[a] for a in Plans` or :math:`L_a \enspace \forall a \in A`

Decision Variables
""""""""""""""""""
- :py:obj:`NumRent` - number of units that are rented starting 
  on :py:obj:`Period p` and under :py:obj:`Plan a`

   - :py:obj:`NumWorkers[(p,a)] for p in Periods for a in Plans` or
     :math:`X_{(p,a)} \enspace \forall (p,a) \in J` or
     :math:`X_{j} \enspace \forall j \in J`

Objective
---------
**Minimize** cost of the purchased plans.  Note that we have to make sure that
the combination of :py:obj:`Period p` and :py:obj:`Plan a` exists in 
:py:obj:`PlanToPeriod`, or :math:`(p,a) \in J`.

.. math::

   \text{Min}  \sum_{a \in A} C_a
      \sum_{p \in P \, \mid \, (p,a) \in J} X_{(p,a)}

Constraints
-----------
- The covering constraints require that there are enough units available
  in each :py:obj:`Period p`.  To obtain the number of units available
  in each period, we need to use the decision variables :py:obj:`NumRent[(p,a)]`
  in combination with the plan lengths :py:obj:`PlanLengths[p]`.
  The number of units available in each period would be the sum of all of
  the :py:obj:`NumRent[(p,a)]` that are `effective` during the covering contraint's
  :py:obj:`Period p`.  In other words, we have to look through all of the plans, and
  see which periods they can start in, and determine whether or not that combination symbol 
  will be effective in the constraint's :py:obj:`Period p` based on the :py:obj:`PlanLengths[p]`.
  This `effective` condition will be represented by the math symbol :math:`f`.  
  In mathematical terms, these constraints can be represented by

.. math::

   \sum_{j \in J \, \mid \, f} X_j \geq R_p
      \quad \forall p \in P

where :math:`P` is a cyclically ordered set (or a cycle).

- The decision variables must be greater than or equal to zero and integer.

.. math::

    X_j \geq 0\text{, int} \enspace \forall j \in J

API Reference
-------------
See the corresponding section in the :ref:`api_reference` to learn more
about how to use the API for this problem class.