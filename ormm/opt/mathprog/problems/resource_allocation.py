import pyomo.environ as pyo

class ResourceAllocation(pyo.AbstractModel):
    """Pyomo Abstract Model for the Resource Allocation Problem

    :return: A pyomo abstract model with definitions for the Resource Allocation Problem

    See Also
    --------
    Formulation: Documentation with definitions & details of the abstract model.

    Examples
    --------
    Creating abstract model, an instance from data params, & solving instance.

    >>> model = ResourceAllocation()
    >>> instance = model.create_instance(my_params.dat) # AMPL data file
    >>> opt = pyo.SolverFactory("glpk")
    >>> opt.solve(instance)
    """

    def __init__(self):
        """Constructor method - calls create_abstract_model
        """
        super().__init__()
        self.create_abstract_model()

    def create_abstract_model(self):
        """Create the abstract model for Resource Allocation Problem
        """
        self.Products = pyo.Set()
        self.Machines = pyo.Set()
        self.Profits = pyo.Param(self.Products)
        self.ProcessTimes = pyo.Param(self.Machines, self.Products)
        self.MaxTimes = pyo.Param(self.Machines)
        self.MaxDemand = pyo.Param(self.Products)
        self.Produce = pyo.Var(self.Products, within = pyo.NonNegativeIntegers, bounds = self._get_bounds)

        self.OBJ = pyo.Objective(rule = self._obj_expression, sense = pyo.maximize)
        self.ResourceConstraint = pyo.Constraint(self.Machines, rule = self._resource_constraint_rule)

    def _get_bounds(self, model, p):
        """Upper Bounds for the Decision Vars based on Maximum Demand
        """
        return (0, self.MaxDemand[p])

    def _obj_expression(self, model):
        """Objective Expression: Maximizing Profit
        """
        return pyo.summation(self.Profits, self.Produce)

    def _resource_constraint_rule(self, model, m):
        """Constraints for Scarce Resources"""
        return sum(self.ProcessTimes[m, p] * self.Produce[p] for p in self.Products) <= self.MaxTimes[m]

def print_sol(instance):
    """Print the solution to the solved `instance`
    :param instance: A solved pyomo.environ.ConcreteModel
    """
    print(f"Objective Value: ${instance.OBJ():,}")
    for v in instance.component_objects(pyo.Var, active=True):
        print ("Variable component: ",v)
        for index in v:
            print ("   ", index, v[index].value)