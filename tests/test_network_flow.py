import time
import random

import pyomo.environ as pyo
import pandas as pd

from ormm.network import transportation_model, Graph
from tests.methods import solve_instance

NETWORK_DATA = "ormm/network/example_data/"
TRANSPORTATION_DATA = NETWORK_DATA + "transportation.dat"
SIMPLE_ARCS = [["A", "B", 7, "one"],
               ["B", "C", 3, "one"],
               ["A", "D", 5, "one"],
               ["D", "E", 5, "one"],
               ["E", "F", 5, "one"],
               ["F", "C", 10, "two"]]
SIMPLE_ARCS_NO_DIRECTION = [arc[:-1] for arc in SIMPLE_ARCS]


def test_transportation_model():
    model = transportation_model()
    instance1 = model.create_instance(TRANSPORTATION_DATA)
    instance2 = transportation_model(filename=TRANSPORTATION_DATA)
    for inst in [instance1, instance2]:
        instance, results = solve_instance(inst)
        assert instance.OBJ() == 475
        for v in instance.component_objects(pyo.Var, active=True):
            assert {index: v[index].value
                    for index in v} == {
                        ('S1', 'D1'): 0.0, ('S1', 'D2'): 5.0,
                        ('S1', 'D3'): 5.0, ('S1', 'D4'): 5.0,
                        ('S1', 'D5'): 0.0, ('S2', 'D1'): 0.0,
                        ('S2', 'D2'): 5.0, ('S2', 'D3'): 0.0,
                        ('S2', 'D4'): 0.0, ('S2', 'D5'): 10.0,
                        ('S3', 'D1'): 5.0, ('S3', 'D2'): 0.0,
                        ('S3', 'D3'): 10.0, ('S3', 'D4'): 0.0,
                        ('S3', 'D5'): 0.0}


def huge_transportation_model():
    # Define large random datasets
    num_nodes = 1_000
    upper_lim = 100
    source_nodes = {None: [f"S{x}" for x in range(num_nodes)]}
    dest_nodes = {None: [f"D{x}" for x in range(num_nodes)]}
    supply = {s: 5 for s in source_nodes[None]}
    demand = {d: 5 for d in dest_nodes[None]}
    ship_costs = {(s, d): random.randint(0, upper_lim)
                  for s in source_nodes[None] for d in dest_nodes[None]}
    my_data = {"Sources": source_nodes,
               "Destinations": dest_nodes,
               "Supply": supply,
               "Demand": demand,
               "ShippingCosts": ship_costs}
    # Define model, load data in it
    model = transportation_model()
    inst = model.create_instance(data={None: my_data})
    # Start timer and solve
    start_time = time.time()
    instance, results = solve_instance(inst)
    end_time = time.time()
    # Print termination status and solving time
    print(results.solver.termination_condition)
    print(end_time - start_time)


def test_graph_repr():
    graph = Graph()
    graph.add_arcs(SIMPLE_ARCS)
    test_str = ("Graph(defaultdict(<class 'list'>, {'A': ['B', 'D'], "
                "'B': ['C'], 'D': ['E'], 'E': ['F'], 'F': ['C'], "
                "'C': ['F']}), {('A', 'B'): 7, ('B', 'C'): 3, "
                "('A', 'D'): 5, ('D', 'E'): 5, ('E', 'F'): 5, "
                "('F', 'C'): 10, ('C', 'F'): 10}, "
                "['A', 'B', 'C', 'D', 'E', 'F'])")
    graph_repr = repr(graph)
    # Need to reorder set of nodes at end
    set_start_index = graph_repr.rfind("{")
    graph_repr_ordered = graph_repr[:set_start_index] + \
        str(sorted(eval(graph_repr[set_start_index:-1]))) + ")"
    assert graph_repr_ordered == test_str


def test_add_arcs_input_types():
    list_tuple = [tuple(arc) for arc in SIMPLE_ARCS]
    tuple_tuple = tuple(tuple(arc) for arc in SIMPLE_ARCS)
    df_no_cols_direction = pd.DataFrame(SIMPLE_ARCS)
    df_cols_direction = pd.DataFrame(
        SIMPLE_ARCS, columns=["From", "To", "Cost", "Direction"])
    df_no_cols_no_direction = pd.DataFrame(SIMPLE_ARCS_NO_DIRECTION)
    df_cols_no_direction = pd.DataFrame(
        SIMPLE_ARCS_NO_DIRECTION, columns=["From", "To", "Cost"])
    dict_arcs = {"From": [arc[0] for arc in SIMPLE_ARCS],
                 "To": [arc[1] for arc in SIMPLE_ARCS],
                 "Cost": [arc[2] for arc in SIMPLE_ARCS],
                 "Direction": [arc[3] for arc in SIMPLE_ARCS]}
    input_types = [list_tuple, tuple_tuple,
                   df_no_cols_direction, df_cols_direction,
                   df_no_cols_no_direction, df_cols_no_direction, dict_arcs]
    for input_type in input_types:
        graph = Graph()
        graph.add_arcs(input_type)
        analysis = graph.shortest_path("A")
        costs, paths = analysis["Costs"], analysis["Paths"]
        test_costs = {'A': 0, 'D': 5, 'B': 7, 'E': 10, 'C': 10, 'F': 15}
        test_paths = {'A': ('A',), 'D': ('A', 'D'), 'B': ('A', 'B'),
                      'E': ('A', 'D', 'E'), 'C': ('A', 'B', 'C'),
                      'F': ('A', 'D', 'E', 'F')}
        assert costs == test_costs
        assert paths == test_paths


def test_shortest_path_simple():
    graph = Graph()
    graph.add_arcs(SIMPLE_ARCS)
    analysis = graph.shortest_path("A")
    costs, paths = analysis["Costs"], analysis["Paths"]
    test_costs = {'A': 0, 'D': 5, 'B': 7, 'E': 10, 'C': 10, 'F': 15}
    test_paths = {'A': ('A',), 'D': ('A', 'D'), 'B': ('A', 'B'),
                  'E': ('A', 'D', 'E'), 'C': ('A', 'B', 'C'),
                  'F': ('A', 'D', 'E', 'F')}
    assert costs == test_costs
    assert paths == test_paths


if __name__ == "__main__":
    # huge_transportation_model()
    test_add_arcs_input_types()
