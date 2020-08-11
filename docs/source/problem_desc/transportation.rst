Transportation Problem
===========================
The Transportation Problem minimizes the shipping costs
while satisfying the demand at each destination.
The decision variables are how many units at each source node will be
shipped to each destination node.
Each source node has a supply, which is the upper limit on how many
units can be shipped from that node.
Each destination node has a demand, which is the required amount
at each destination node.

The main constraints ensure that all supply is used from the source nodes,
and that all demand is met at the destination nodes.
This type of problem arises often, with notable examples being supply chain
management and online order shipments.

Definitions
-----------

Sets
""""
- :py:obj:`Sources` - A set of nodes where the units are shipped from

   - :py:obj:`i in Sources` or :math:`i \in I`

- :py:obj:`Destinations` - A set of nodes where the units are shipped to

   - :py:obj:`j in Destinations` or :math:`j \in J`

Parameters
""""""""""
- :py:obj:`Supply` - measure of number of units available at :py:obj:`Source i`

   - :py:obj:`Supply[i] for i in Sources` or :math:`S_i \enspace \forall i \in I`

- :py:obj:`Demand` - measure of number of units available at :py:obj:`Source i`

   - :py:obj:`Demand[j] for j in Destinations` or :math:`D_j \enspace \forall j \in J`

- :py:obj:`ShippingCost` - measure of the cost of holding one extra unit
  from one period to the next

   - :py:obj:`ShippingCost[i, j] for i in Sources for j in Destinations`
     or :math:`C_{i,j} \enspace \forall i \in I\text{, }j \in J`

Decision Variables
""""""""""""""""""
- :py:obj:`Flow` - number of units to ship from :py:obj`Source i` to
  :py:obj`Destination j`

   - :py:obj:`Flow[i, j] for i in Sources for j in Destinations`
     or :math:`X_{i,j} \enspace \forall i \in I\text{, }j \in J`

- :py:obj:`InvLevel` - number of units left in inventory
  at the end of :py:obj:`Period p`

   - :py:obj:`InvLevel[p] for p in Periods` or
     :math:`Y_{p} \enspace \forall p \in P`

Objective
---------
**Minimize** shipping costs from sources to destinations.

.. math::

   \text{Min}  \sum_{i \in I} \sum_{j \in J} C_{i,j}X_{i,j}

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