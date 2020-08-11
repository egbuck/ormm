import time
import random

import pyomo.environ as pyo

from ormm.mathprog import transportation
from tests.methods import solve_instance

MATHPROG_DATA = "ormm/mathprog/example_data/"
TRANSPORTATION_DATA = MATHPROG_DATA + "transportation.dat"


def test_transportation():
    model = transportation()
    instance1 = model.create_instance(TRANSPORTATION_DATA)
    instance2 = transportation(filename=TRANSPORTATION_DATA)
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


def bad_huge_transportation():
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
    model = transportation()
    inst = model.create_instance(data={None: my_data})
    # Start timer and solve
    start_time = time.time()
    instance, results = solve_instance(inst)
    end_time = time.time()
    # Print termination status and solving time
    print(results.solver.termination_condition)
    print(end_time - start_time)


if __name__ == "__main__":
    bad_huge_transportation()
