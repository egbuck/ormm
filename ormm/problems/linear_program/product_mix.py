import pyomo.environ as pyo
# import pandas / numpy


class ProductMix(object):

    def __init__(self, dat_file):
        """dat file holds param values for our abstract model"""
        self.model = self.create_abstract_model()
        self.model.pprint()
        self.instance = self.model.create_instance(dat_file)

    def create_abstract_model(self):
        """Create the abstract model"""
        model = pyo.AbstractModel()
        model.Products = pyo.Set()
        model.Machines = pyo.Set()
        model.Profits = pyo.Param(model.Products)
        model.ProcessTimes = pyo.Param(model.Machines, model.Products)
        model.MaxTimes = pyo.Param(model.Machines)
        model.MaxDemand = pyo.Param(model.Products)
        model.Produce = pyo.Var(model.Products, within = pyo.NonNegativeIntegers, bounds = self._get_bounds)

        model.OBJ = pyo.Objective(rule = self._obj_expression)
        model.AxbConstraint = pyo.Constraint(model.Machines, rule = self._ax_constraint_rule)
        return model

    def _get_bounds(self, model, p):
        return (0, model.MaxDemand[p])

    def _obj_expression(self, model):
        return pyo.summation(model.Profits, model.Produce)

    def _ax_constraint_rule(self, model, m):
        return sum(model.ProcessTimes[m, p] * model.Produce[p] for p in model.Products) >= model.MaxTimes[m]

    def solve(self, opt = pyo.SolverFactory("glpk")):
        """Solve the ProductMix Model Instance"""
        opt.solve(self.instance)