import pyomo.environ as pyo
from problems.linear_program.product_mix import ProductMix, print_sol

def main():
    data_path = "problems/linear_program/example_data/product_mix.dat"
    mod = ProductMix()
    instance = mod.create_instance(data_path)
    opt = pyo.SolverFactory("glpk")
    results = opt.solve(instance)
    print_sol(instance, results)


if __name__ == "__main__":
    main()