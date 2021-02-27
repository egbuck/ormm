Shortest Path Tree Problem
==========================
The Shortest Path Problem minimizes the weighted distance from one source
node to one destination node.  This module's implementation is actually the
Shortest Path Tree Problem, which solves the Shortest Path Problem for every
possible destination node from a single source node.

Dijkstra's algorithm finds an optimal solution to the shortest path tree problem
as long as all of the weighted distances (costs of traveling an arc) are
nonnegative.

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

- :py:obj:`Demand` - measure of number of units required at :py:obj:`Destination j`

   - :py:obj:`Demand[j] for j in Destinations` or :math:`D_j \enspace \forall j \in J`

- :py:obj:`ShippingCost` - measure of the cost of shipping one unit from
  :py:obj:`Source i` to :py:obj:`Destination j`

   - :py:obj:`ShippingCost[i, j] for i in Sources for j in Destinations`
     or :math:`C_{i,j} \enspace \forall i \in I\text{, }j \in J`

Decision Variables
""""""""""""""""""
- :py:obj:`Flow` - number of units to ship from :py:obj:`Source i` to
  :py:obj`:Destination j`

   - :py:obj:`Flow[i, j] for i in Sources for j in Destinations`
     or :math:`X_{i,j} \enspace \forall i \in I\text{, }j \in J`

Objective
---------
**Minimize** shipping costs from sources to destinations.

.. math::

   \text{Min}  \sum_{i \in I} \sum_{j \in J} C_{i,j}X_{i,j}

Constraints
-----------
- The total supply must be equal to the total demand.  Currently, this constraint
  must be met by the user changing their data.  See the Notes section of the API
  docs for more details.

- All of the supply at each node must be shipped to the destination nodes.

.. math::

   \sum_{j \in J}X_{i,j} = S_i \quad \forall i \in I

- All of the demand at each node must be met by the source nodes.

.. math::

   \sum_{i \in I}X_{i,j} = D_j \quad \forall j \in J

- The decision variables must be greater than or equal to zero and integer.

.. math::

    X_{i,j} \geq 0\text{, int} \enspace \forall i \in I\text{, }j \in J

API Reference
-------------
See the corresponding section in the :ref:`api_reference` to learn more
about how to use the API for this problem class.