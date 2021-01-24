import pyomo.environ as pyo
import pandas as pd
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
        self.arcs
            Dictionary of possible paths from one node
            e.g. {'A': ['B', 'C', 'D', 'E'], ...}
        self.costs
            The cost of traveling from one node to another
            e.g. {('A', 'B'): 2, ('A', 'C'): 5, ...}
        self.nodes
            A set of all unique nodes in the graph
            e.g. {"A", "B", "C", ...}
        """
        self.arcs = defaultdict(list)
        self.costs = {}
        self.nodes = set()

    def add_arcs(self, arcs):
        """
        Parameters
        ----------
        edges
            Iterable of Iterables that contain arc information,
            such as from_node, to_node, cost, and
            optionally whether the arc is one-directional
            ("one") or bi-directional ("two")
        """
        for arc in arcs:
            self._add_arc(*arc)

    def _add_arc(self, from_node, to_node, cost, direction="two"):
        self.arcs[from_node].append(to_node)
        self.costs[(from_node, to_node)] = cost

        if direction == "two":
            self.arcs[to_node].append(from_node)
            self.costs[(to_node, from_node)] = cost

        self.nodes.update([from_node, to_node])

    def shortest_path(self, source):
        """
        Solve the shortest path tree problem with Dijkstra's Algorithm.
        This requires nonnegative arc lengths to get an optimal solution.

        Parameters
        ----------
        source
            The source node to use for minimizing the distance to all
            other nodes
        """
        solved_nodes = {source}
        min_costs = {source: 0}
        best_paths = {source: (source,)}
        while solved_nodes != self.nodes:
            # Find best arc that passes from solved node to unsolved
            # Filter self.arcs to include only arcs from solved nodes
            valid_arcs = {node: self.arcs[node]
                          for node in solved_nodes if self.arcs[node]}
            # Change valid_arcs from dict of lists to list of tuples
            #  And take out arcs that go to solved_nodes
            arc_tuples = [(key, *dest) for key, value in valid_arcs.items()
                          for dest in value]
            arc_tuples = [(start, end) for (start, end) in arc_tuples
                          if end not in solved_nodes]
            # Retrieve costs for arc_tuples
            costs = {node: self.costs[node] for node in arc_tuples}
            total_costs = {(from_node, to_node):
                           min_costs[from_node] + costs[(from_node, to_node)]
                           for (from_node, to_node) in arc_tuples}
            best_add = min(total_costs, key=total_costs.get)
            best_cost = total_costs[best_add]
            new_solved_node = best_add[1]
            solved_nodes.add(new_solved_node)
            min_costs[new_solved_node] = best_cost
            best_paths[new_solved_node] = \
                best_paths[best_add[0]] + (new_solved_node,)
        return min_costs, best_paths

    def init_df(self):
        """
        """
        pass

    def add_arcs_df(self, arcs):
        """
        """
        pass

    def shortest_path_df(self, source):
        solution = pd.DataFrame(data=[[source, 0, source]],
                                columns=["Destination", "Cost", "Path"])
        while solution["Destination"] != self.states:
            # Find best arc that passes from solved node to unsolved
            # Filter self.arcs to include only solved nodes
            valid_arcs = {key: self.arcs[key]
                          for key in solution["Destination"]}
            # Change valid_arcs from dict of lists to list of tuples
            arc_tuples = [(key, *dest) for key, value in valid_arcs.items()
                          for dest in value]
            # Retrieve costs for arc_tuples
            costs = {key: self.costs[key] for key in arc_tuples}
            print(costs)
