Aggregate Planning Problem
===========================
The Aggregate Planning Problem minimizes the production and holding costs
while satisfying the demand of units for each period.
The decisions to be made in this problem are how many units to produce in
each period.  Units that aren't sold (aka are over the demand) in one period
can be held into the next, but with some holding cost per unit.
While the holding cost is a single parameter, production costs per unit
can vary from period to period.

This main constraints are the `conservation of flow` constraints, or that the leftover
inventory plus the production minus the extra inventory equals the demand
for every period. 
This type of problem can arise in manufacturing or in sales industries.

Definitions
-----------

Sets
""""
- :py:obj:`Periods` - An ordered set of periods when the units are needed

   - :py:obj:`p in Periods` or :math:`p \in P`

Parameters
""""""""""
- :py:obj:`Demand` - measure of number of units needed for :py:obj:`Period p`

   - :py:obj:`Demand[p] for p in Periods` or :math:`D_p \enspace \forall p \in P`

- :py:obj:`Cost` - measure of cost of producing one unit within :py:obj:`Period p`

   - :py:obj:`Cost[p] for p in Periods` or :math:`C_p \enspace \forall p \in P`

- :py:obj:`HoldingCost` - measure of the cost of holding one extra unit
  from one period to the next

   - :py:obj:`HoldingCost` or :math:`H`

- :py:obj:`MaxStorage` - maximum number of units that can be held over
  from one period to the next

   - :py:obj:`MaxStorage` or :math:`M`

- :py:obj:`InitialInv` - initial number of units in inventory, before the
  first period begins

   - :py:obj:`InitialInv` or :math:`I_F`

- :py:obj:`FinalInv` - desired number of units in inventory to end up with, 
  after the last period ends

   - :py:obj:`FinalInv` or :math:`I_L`

Decision Variables
""""""""""""""""""
- :py:obj:`Produce` - number of units to produce
  in :py:obj:`Period p`

   - :py:obj:`Produce[p] for p in Periods` or
     :math:`X_{p} \enspace \forall p \in P`

- :py:obj:`InvLevel` - number of units left in inventory
  at the end of :py:obj:`Period p`

   - :py:obj:`InvLevel[p] for p in Periods` or
     :math:`Y_{p} \enspace \forall p \in P`

Objective
---------
**Minimize** production cost and holding costs.

.. math::

   \text{Min}  \sum_{p \in P} C_pX_p + HY_p

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