import io
import sys

import pyomo.environ as pyo
from ormm.mathprog import resource_allocation, print_sol

SIMPLE_DATA = "../ormm/mathprog/example_data/resource_allocation.dat"
COMPLEX_DATA = "../ormm/mathprog/example_data/mult_resource_allocation.dat"

def create_cm_with_data(data_path, **kwargs):
    """Use exmaple data & return results and solved instance"""
    mod = resource_allocation(**kwargs)
    instance = mod.create_instance(data_path)
    opt = pyo.SolverFactory("glpk")
    results = opt.solve(instance)
    return instance, results

def test_simple_resource_allocation_with_data():
    instance, results = create_cm_with_data(SIMPLE_DATA)
    # Check all variable values
    for v in instance.component_objects(pyo.Var, active=True):
        if v.name == "NumActivity":
            assert {index: v[index].value
                for index in v} == {"P": 100, "Q": 30}
    assert instance.OBJ() == 6300

def test_complex_resource_allocation_with_data():
    instance, results = create_cm_with_data(
        COMPLEX_DATA, mult_res = True, max_activity = False)
    # Check all variable values
    for v in instance.component_objects(pyo.Var, active=True):
        if v.name == "NumActivity":
            assert {
                index: round(v[index].value, 2) for index in v} == {
                "Q": 58.96, "W": 62.63, "E": 0, "R": 10.58, "T":15.64}
    assert round(instance.OBJ(), 0) == 2989

def test_print_sol_with_data():
    instance, results = create_cm_with_data(SIMPLE_DATA)
    # Redirect output to StringIO object
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_sol(instance)
    sys.stdout = sys.__stdout__  # reset stdout
    test_string = (
        "Objective Value: $6,300.0\n"
        "Variable component:  NumActivity\n"
        "    P 100.0\n"
        "    Q 30.0\n"
    )
    assert captured_output.getvalue() == test_string