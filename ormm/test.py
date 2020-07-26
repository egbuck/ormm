import pyomo.environ as pyo
from problems.linear_program.product_mix import ProductMix

def main():
    data_path = "problems/linear_program/example_data/product_mix.dat"
    mod = ProductMix(data_path)
    #mod.solve()


if __name__ == "__main__":
    main()