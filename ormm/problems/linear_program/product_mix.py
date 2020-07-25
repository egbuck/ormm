import pyomo.environ as pyo
# import pandas / numpy


class ProductMix(object):

    def __init__(self, dat_file):
        """dat file holds param values for our abstract model"""
        self.model = self.create_abstract_model()
        self.instance = self.model.create_instance(dat_file)

    def create_abstract_model(self):
        """Create the abstract model"""
        model = pyo.AbstractModel()
        model.products = pyo.Set()
        model.machines = pyo.Set()
        model.profits = pyo.Param(model.products)
        model.process_times = pyo.Param(model.machines, model.products)
        model.max_times = pyo.Param(model.machines)
        model.max_demand = pyo.Param(model.products)
        model.produce = pyo.Var(model.products, domain = pyo.NonNegativeIntegers, ub = model.max_demand)

        model.OBJ = pyo.Objective(rule = self._obj_expression)
        model.AxbConstraint = pyo.Constraint(model.machines, rule = self._ax_constraint_rule)
        return model

    def _obj_expression(self, model):
        return pyo.summation(model.profits, model.product)

    def _ax_constraint_rule(self, model, m):
        return sum(model.process_times[m, p] * model.produce[p] for p in model.products) >= model.max_times[m]

    def solve(self, opt = pyo.SolverFactory("glpk")):
        """Solve the ProductMix Model Instance"""
        opt.solve(self.instance)