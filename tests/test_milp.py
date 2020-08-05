import io
import sys

import pyomo.environ as pyo
import pandas as pd

from ormm.mathprog import resource_allocation, \
    print_sol, sensitivity_analysis, blending
from tests.methods import solve_instance

MATHPROG_DATA = "ormm/mathprog/example_data/"
SIMPLE_RES_DATA = MATHPROG_DATA + "resource_allocation.dat"
COMPLEX_RES_DATA = MATHPROG_DATA + "mult_resource_allocation.dat"
BLENDING_DATA = MATHPROG_DATA + "blending.dat"


def create_instance_results(model, data_path):
    instance = model.create_instance(data_path)
    opt = pyo.SolverFactory("glpk")
    results = opt.solve(instance)
    return instance, results


def create_blending(data_path, **kwargs):
    mod = blending(**kwargs)
    return create_instance_results(mod, data_path)


def test_simple_resource_allocation_with_data():
    model = resource_allocation()
    instance1 = model.create_instance(SIMPLE_RES_DATA)
    instance2 = resource_allocation(filename=SIMPLE_RES_DATA)
    for inst in [instance1, instance2]:
        instance, results = solve_instance(inst)
        # Check all variable values
        for v in instance.component_objects(pyo.Var, active=True):
            if v.name == "NumActivity":
                assert {index: v[index].value
                        for index in v} == {"Q": 31.25, "W": 75}
        assert instance.OBJ() == 7343.75


def test_complex_resource_allocation_with_data():
    instance = resource_allocation(
        filename=COMPLEX_RES_DATA, mult_res=True, max_activity=False)
    instance, results = solve_instance(instance)
    # Check all variable values
    for v in instance.component_objects(pyo.Var, active=True):
        if v.name == "NumActivity":
            assert {
                index: round(v[index].value, 2) for index in v} == {
                "Q": 123.08, "W": 0, "E": 0, "R": 0, "T": 46.15, "Y": 0}
    assert round(instance.OBJ(), 0) == 2692


def test_blending():
    model = blending()
    instance1 = model.create_instance(BLENDING_DATA)
    instance2 = blending(filename=BLENDING_DATA)
    for inst in [instance1, instance2]:
        instance, results = solve_instance(inst)
        for v in instance.component_objects(pyo.Var, active=True):
            if v.name == "Blend":
                assert {
                    index: round(v[index].value, 2) for index in v} == {
                    "Banana": 0.02, "Milk": 0.76, "Yogurt": 0.22}
        assert round(instance.OBJ(), 2) == 37.61


def test_print_sol_with_data():
    instance = resource_allocation(filename=SIMPLE_RES_DATA)
    instance, results = solve_instance(instance)
    # Redirect output to StringIO object
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_sol(instance, money_obj=True)
    sys.stdout = sys.__stdout__  # reset stdout
    test_string = (
        "Objective Value: $7,343.75\n"
        "Variable component:  NumActivity\n"
        "    Q 31.25\n"
        "    W 75.0\n"
    )
    assert captured_output.getvalue() == test_string


def test_sensitivity_analysis():
    instance = resource_allocation(
        filename=COMPLEX_RES_DATA, mult_res=True, max_activity=False)
    instance, results = solve_instance(instance)
    sens_analysis_df = sensitivity_analysis(instance)
    test_df = pd.DataFrame({
        "Dual Value": [9.29, 0.00, 5.22, 0.00],
        "Lower": [None, None, None, None],
        "Upper": [200.0, 280.0, 160.0, 320.0],
        "Slack": [0, 113.85, 0, 107.69],
        "Active": [True, False, True, False]
        }, index=[
            "ResourceConstraint[A]",
            "ResourceConstraint[B]",
            "ResourceConstraint[C]",
            "ResourceConstraint[D]"])
    sens_analysis_df["Dual Value"] = \
        sens_analysis_df["Dual Value"].round(decimals=2)
    sens_analysis_df["Slack"] = \
        sens_analysis_df["Slack"].round(decimals=2)
    assert sens_analysis_df.equals(test_df)
