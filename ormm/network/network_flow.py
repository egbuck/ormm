"""
Eventually may move transportation_model to method in Graph class
To do this, would:
  * When call transportation, arguments for:
    - These are the supply nodes
    - These are their supply max's
    - These are demand nodes
    - These are demand requirements (mins)
    - Then maybe option for adding that info to graph object?

Other ideas to add:
  * Implement print() method on Graph object (__repr__)
  * Graph() should be able to read in data file (.dat)
    used for transportation problem
    - either when transportation_problem is called, or
      in separate method to permanently add attributes
  * Graph() needs add_arcs overhaul
    - reading in different attributes
    - different input types to handle:
      1. Dictionaries
      2. Lists
      3. Numpy arrays
      4. Pandas DF
      5. Data file (.dat)?
"""

from collections import defaultdict
from collections.abc import Sequence

import numpy as np
import pandas as pd
import pyomo.environ as pyo


def transportation_model(**kwargs):
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
    def __init__(self, arcs=defaultdict(list), costs={}, nodes=set()):
        """
        Parameters
        ----------
        arcs
            Dictionary of possible paths from one node
            e.g. {'A': ['B', 'C', 'D', 'E'], ...}
        costs
            The cost of traveling from one node to another
            e.g. {('A', 'B'): 2, ('A', 'C'): 5, ...}
        nodes
            A set of all unique nodes in the graph
            e.g. {"A", "B", "C", ...}
        """
        self.arcs = arcs
        self.costs = costs
        self.nodes = nodes

    def __repr__(self):
        """String representation that could recreate object"""
        return (f"Graph({self.arcs!r}, {self.costs!r}, {self.nodes!r})")

    def __str__(self):
        """String representation for user reading object

        NOT IMPLEMENTED - currently just calls __repr__"""
        return repr(self)

    def add_arcs(self, arc_data):
        """
        Parameters
        ----------
        arc_data
            Iterable of Iterables that contain arc information,
            such as from_node ("From"), to_node ("To"),
            cost ("Cost), and
            optionally direction ("Direction") -
            whether the arc is one-directional
            ("one") or bi-directional ("two")
            e.g. [["A", "B", 7, "one"],
                  ["B", "C", 3, "one"],
                  ["C", "A", 8, "two"]]

        Raises
        ------
        TypeError
            If `arcs` is not a dict, list, DataFrame, tuple, or array
        ValueError
            If `arcs` does not have enough arguments (columns) to support
            the requirements (from_node, to_node, cost)
        """
        if isinstance(arc_data, (Sequence, np.ndarray)):
            for arc in arc_data:
                self._add_arc(*arc)
        elif isinstance(arc_data, (pd.DataFrame, dict)):
            if isinstance(arc_data, dict):
                arc_data = pd.DataFrame(arc_data)
            # Create possible keywords
            from_choices = pd.Series(["From", "FromNode", "From_Node",
                                      "From_node", "From Node"])
            to_choices = pd.Series(["To", "ToNode", "To_Node", "To_node",
                                    "To Node"])
            cost_choices = pd.Series(["Cost", "ShippingCost", "Shipping_Cost",
                                      "Shipping_cost", "Shipping Cost"])
            # Add lowercase & uppercase options to choices
            from_choices = from_choices.append(
                from_choices.str.lower(), ignore_index=True).append(
                    from_choices.str.upper(), ignore_index=True)
            to_choices = to_choices.append(
                to_choices.str.lower(), ignore_index=True).append(
                    to_choices.str.upper(), ignore_index=True)
            cost_choices = cost_choices.append(
                cost_choices.str.lower(), ignore_index=True).append(
                    cost_choices.str.upper(), ignore_index=True)
            # Get lists of matches in column names
            from_matches = [col for col in arc_data.columns
                            if col in set(from_choices)]
            to_matches = [col for col in arc_data.columns
                          if col in set(to_choices)]
            cost_matches = [col for col in arc_data.columns
                            if col in set(cost_choices)]
            if from_matches and to_matches and cost_matches:
                direction_choices = pd.Series(["Direction", "direction"])
                direction_matches = [col for col in arc_data.columns
                                     if col in set(direction_choices)]
                if direction_matches:
                    key_cols = {"From": from_matches[0],
                                "To": to_matches[0],
                                "Cost": cost_matches[0],
                                "Direction": direction_matches[0]}
                    for _, row in arc_data.iterrows():
                        self._add_arc(row[key_cols["From"]],
                                      row[key_cols["To"]],
                                      row[key_cols["Cost"]],
                                      row[key_cols["Direction"]])
                else:
                    key_cols = {"From": from_matches[0],
                                "To": to_matches[0],
                                "Cost": cost_matches[0]}
                    for _, row in arc_data.iterrows():
                        self._add_arc(row[key_cols["From"]],
                                      row[key_cols["To"]],
                                      row[key_cols["Cost"]])
            else:
                num_cols = arc_data.shape[1]
                if num_cols == 3:
                    for _, row in arc_data.iterrows():
                        self._add_arc(row[0], row[1], row[2])
                elif num_cols >= 4:
                    for _, row in arc_data.iterrows():
                        self._add_arc(row[0], row[1], row[2], row[3])
                else:
                    raise ValueError("Not enough columns in `arcs` to support"
                                     " required arguments (`From`, `To`,"
                                     " `Cost`)")
        else:
            raise TypeError("Argument 'arcs' must be an iterable of"
                            " iterables!")

    def _add_arc(self, from_node, to_node, cost, direction="two"):
        # Check if to_node in from_node's list in self.arcs dict
        if from_node not in self.arcs or to_node not in self.arcs[from_node]:
            self.arcs[from_node].append(to_node)

        # Add new cost, or overwrite old cost
        self.costs[(from_node, to_node)] = cost

        # Do same thing as above in reverse if bidirectional arc
        if direction == "two":
            if to_node not in self.arcs and (
                    from_node not in self.arcs[to_node]):
                self.arcs[to_node].append(from_node)
            self.costs[(to_node, from_node)] = cost

        # Add from_node and to_node to nodes set if don't exist
        self.nodes.update([from_node, to_node])

    def shortest_path(self, source):
        """
        Solve the shortest path tree problem with Dijkstra's Algorithm.
        This requires nonnegative costs/arc lengths to get an optimal solution.

        Parameters
        ----------
        source
            The source node to use for minimizing the distance to all
            other nodes

        Returns
        -------
        dictionary
            Contains minimum costs and best paths
            to achieve those minimum costs

        Raises
        ------
        ValueError
            If self.costs contains any negative costs (arc lengths)
        """
        if min(self.costs.values()) < 0:
            raise ValueError("Non-negative costs (arc lengths) required"
                             " for Dijkstra's Algorithm for"
                             " shortest path tree problem!")
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
        return {"Costs": min_costs, "Paths": best_paths}
