import io
import sys

import pyomo.environ as pyo
from ormm.mathprog import resource_allocation, \
    print_sol, sensitivity_analysis

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
    sensitivity_analysis(instance)

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

def test_sensitivity_analysis():
    instance, results = create_cm_with_data(
        COMPLEX_DATA, mult_res = True, max_activity = False)
    # Redirect output to StringIO object
    captured_output = io.StringIO()
    sys.stdout = captured_output
    sensitivity_analysis(instance)
    sys.stdout = sys.__stdout__  # reset stdout
    test_string = (
    "dual : Direction=Suffix.IMPORT, Datatype=Suffix.FLOAT\n"
    "    Key                   : Value\n    ResourceConstraint[A]"
    " :  4.81950601646612\n    ResourceConstraint[B] :"
    "  5.20160439096475\n    ResourceConstraint[C] :"
    "  8.96347899514461\n    ResourceConstraint[D] :"
    " 0.363099007810851\n\nResourceConstraint[A]\nSlack:"
    " -0.0\n{Member of ResourceConstraint} : Size=4,"
    " Index=Resources, Active=True\n    Key : Lower : Body      "
    "                                                           "
    "             : Upper : Active\n"
    "      A :  -Inf : 1.2*NumActivity[Q] + 1.3*NumActivity[W] "
    "+ 0.7*NumActivity[E] + 0.5*NumActivity[T] : 160.0 :   True\n"
    "\nResourceConstraint[B]\nSlack: 0.0\n{Member of "
    "ResourceConstraint} : Size=4, Index=Resources, Active=True\n"
    "    Key : Lower : Body                                      "
    "                                                        "
    " : Upper : Active\n"
    "      B :  -Inf : 0.7*NumActivity[Q] + 2.2*NumActivity[W] "
    "+ 1.6*NumActivity[E] + 0.5*NumActivity[R] + NumActivity[T] :"
    " 200.0 :   True\n\nResourceConstraint[C]\nSlack: -0.0\n"
    "{Member of ResourceConstraint} : Size=4, Index=Resources,"
    " Active=True\n    Key : Lower : Body                      "
    "                                                          "
    "               : "
    "Upper : Active\n      C :  -Inf : 0.9*NumActivity[Q] + "
    "0.7*NumActivity[W] + 1.3*NumActivity[E] + NumActivity[R] + "
    "0.8*NumActivity[T] : 120.0 :   True\n\nResourceConstraint[D]\n"
    "Slack: 0.0\n{Member of ResourceConstraint} : Size=4, "
    "Index=Resources, Active=True\n    Key : Lower : Body        "
    "                                                            "
    "                               : Upper : Active\n      D "
    ":  -Inf : 1.4*NumActivity[Q]"
    " + 2.8*NumActivity[W] + 0.5*NumActivity[E] + 1.2*"
    "NumActivity[R] + 0.6*NumActivity[T] : 280.0 :   True\n\n"
    )
    assert captured_output.getvalue() == test_string

if __name__ == "__main__":
    test_sensitivity_analysis()