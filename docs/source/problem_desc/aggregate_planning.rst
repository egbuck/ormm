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

   - :py:obj:`HoldingCost` or :math:`h`

- :py:obj:`MaxStorage` - maximum number of units that can be held over
  from one period to the next

   - :py:obj:`MaxStorage` or :math:`m`

- :py:obj:`InitialInv` - initial number of units in inventory, before the
  first period begins

   - :py:obj:`InitialInv` or :math:`I_I`

- :py:obj:`FinalInv` - desired number of units in inventory to end up with, 
  after the last period ends

   - :py:obj:`FinalInv` or :math:`I_F`

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

   \text{Min}  \sum_{p \in P} C_pX_p + hY_p

Constraints
-----------
- The conservation of flow constraints enforce the relationships between the
  production, inventory levels, and the demand for each period.  
  In mathematical terms, these constraints can be represented by

.. math::

   Y_{p-1} + X_p - Y_{p} = D_p
      \quad \forall p \in P

where :math:`Y_{p-1}` is defined to be :math:`I_I` when :math:`p` is the first period.

- The amount stored at the end of each period cannot be more than the maximum
  amount allowed, :math:`m`.

.. math::

   Y_p \leq m \quad \forall p \in P

- We define constraints to enforce the definition of :math:`Y_{p-1}` when :math:`p`
  is the first period, as well as the last period's inventory level to be :math:`I_F`.

.. math::

   Y_{\min(P)-1} &= I_I

   Y_{\max(P)} &= I_F

- The decision variables must be greater than or equal to zero and integer.

.. math::

    X_p, \, Y_p \geq 0\text{, int} \enspace \forall p \in P

API Reference
-------------
See the corresponding section in the :ref:`api_reference` to learn more
about how to use the API for this problem class.