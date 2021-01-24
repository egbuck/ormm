import pyomo.environ as pyo
from collections import defaultdict


def transportation(**kwargs):
    """
    Factory method for the balanced transportation problem.

    By balanced, we mean that this implementation currently requires the data
    to have the same number of source nodes as destination nodes. Your data
    can be easily changed to meet this requirement; see the notes section.

    This network flow problem has a set of source nodes and
    destination nodes, with shipping costs between each of them.
    There are demands at the destinations, and supply limits at the
    sources.  The objective is to minimize the shipping costs while
    meeting the demands.

    Parameters
    ----------
    **kwargs
        Passed into Pyomo Abstract Model's `create_instance`
        to return Pyomo Concrete Model instead.

    Returns
    -------
    pyomo.environ.AbstractModel or pyomo.environ.ConcreteModel
        Abstract Model with the sets, parameters, decision variables,
        objective, and constraints for the transportation problem.
        Returns a Concrete Model instead if any kwargs passed.

    Notes
    -----
    This is a bipartite network with m supply nodes and n destination nodes.
    If not possible to ship from i to j, a large cost M should be passed.

    Assumes the feasibility property holds (total supply equals total demand) -
    then becomes balanced TP. You can modify data so this requirement is
    satisfied.

    Let :math:`\\delta` be the excess amount (positive).  Add  a dummy source
    to the data with index m + 1 if demand > supply.

    :math:`s_{m+1} = \\delta\\text{ ; }c_{m+1,j}=0 \\quad \\forall j \\in J`

    Add a dummy demand to the data with index n + 1 if supply > demand.

    :math:`d_{n+1} = \\delta\\text{ ; }c_{i,n+1}=0 \\quad \\forall i \\in I`

    .. math::

        \\text{Min} \\sum_{i \\in I}\\sum_{j \\in J}C_{i,j}X_{i,j}

        \\text{s.t. } \\sum_{j \\in J} X_{i,j} = S_i \\quad \\forall i \\in I

        \\sum_{i \\in I} X_{i,j} = D_j \\quad \\forall j \\in J

        X_{i,j} \\geq 0\\text{, int} \\quad \\forall i \\in I\\text{, }j \\in J
    """
    def _obj_expression(model):
        """Objective Expression: Minimizing Shipping Costs"""
        return pyo.summation(model.ShippingCosts, model.Flows)

    def _supply_constraint_rule(model, i):
        """Constraints for flows from supply"""
        return sum(model.Flows[i, j]
                   for j in model.Destinations) == model.Supply[i]

    def _demand_constraint_rule(model, j):
        """Constraints for flows from demands"""
        return sum(model.Flows[i, j]
                   for i in model.Supply) == model.Demand[j]

    # Create the abstract model & dual suffix
    model = pyo.AbstractModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    # Define sets/params that are always used
    model.Sources = pyo.Set()
    model.Destinations = pyo.Set()
    model.Supply = pyo.Param(model.Sources)
    model.Demand = pyo.Param(model.Destinations)
    model.ShippingCosts = pyo.Param(model.Sources, model.Destinations)
    # Define decision variables
    model.Flows = pyo.Var(
        model.Sources,
        model.Destinations,
        within=pyo.NonNegativeReals,
        bounds=(0, None))
    # Define objective & constraints
    model.OBJ = pyo.Objective(rule=_obj_expression, sense=pyo.minimize)
    model.SupplyConstraint = pyo.Constraint(
        model.Sources,
        rule=_supply_constraint_rule)
    model.DemandConstraint = pyo.Constraint(
        model.Destinations,
        rule=_demand_constraint_rule)
    # Check if returning concrete or abstract model
    if kwargs:
        return model.create_instance(**kwargs)
    else:
        return model


class Graph():
    def __init__(self):
        """
        Attributes
        ----------
        self.edges
            dictionary of connected nodes
            e.g. {'A': ['B', 'C', 'D', 'E'], ...}
        self.costs
            The cost of traveling from one node to another
            e.g. {('A', 'B'): 2, ('A', 'C'): 5, ...}
        """
        self.edges = defaultdict(list)
        self.cost = {}

    def add_edges(self, edges):
        """
        Parameters
        ----------
        edges
            Iterable of Iterables that contain edge information,
            such as from_node, to_node, cost, and
            optionally whether the edge is one-directional
            ("one") or bi-directional ("two")
        """
        for edge in edges:
            self._add_edge(*edge)

    def _add_edge(self, from_node, to_node, cost, direction="two"):
        self.edges[from_node].append(to_node)
        if direction == "two":
            self.edges[to_node].append(from_node)

        self.costs[(from_node, to_node)] = cost
        self.costs[(to_node, from_node)] = cost

    def shortest_path():
        """
        Solve the shortest path tree problem with Dijkstra's Algorithm.
        """
        pass
