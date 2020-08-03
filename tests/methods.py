import pyomo.environ as pyo


def solve_instance(instance):
    opt = pyo.SolverFactory("glpk")
    results = opt.solve(instance)
    return instance, results
