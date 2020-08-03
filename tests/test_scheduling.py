from ormm.mathprog import scheduling
import pyomo.environ as pyo


def solve_instance(instance):
    opt = pyo.SolverFactory("glpk")
    results = opt.solve(instance)
    return instance, results


def test_employee_simple():
    instance = scheduling(filename="ormm/mathprog/example_data/employee.dat")
    instance, results = solve_instance(instance)
    assert instance.OBJ() == 295
    for v in instance.component_objects(pyo.Var, active=True):
        assert {index: v[index].value
                for index in v} == {1: 55, 2: 115, 3: 85, 4: 0, 5: 25, 6: 15}
