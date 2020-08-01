"""
Module contains classes & functions for Mixed Integer Linear Programs (MILP).
"""
import pyomo.environ as pyo

class ResourceAllocation(pyo.AbstractModel):
    """
    Subclass of Pyomo Abstract Model for the Resource Allocation Problem.

    Parameters
    ----------
    *args : optional
        Passed into Pyomo Abstract Model's `create_instance`
        to return Pyomo Concrete Model instead.
    **kwargs : optional
        Passed into Pyomo Abstract Model's `create_instance`
        to return Pyomo Concrete Model instead.

    Notes
    -----
    The Resource Allocation Problem optimizes using scarce resources for valued activities.

    .. math::

       \\text{Max}  \sum_{a \in A} V_aX_a

       \\text{s.t.} \sum_{a \in A} N_{r,a}X_a \leq M_r \quad \\forall r \in R

       0 \leq X_a \leq M_a \quad \\forall a \in A

    Examples
    --------
    Creating abstract model, an instance from data params, & solving instance.

    >>> import pyomo.environ as pyo
    >>> model = ResourceAllocation()
    >>> instance = model.create_instance("my_params.dat") # AMPL data file
    >>> opt = pyo.SolverFactory("glpk")
    >>> results = opt.solve(instance)
    """
    def __init__(self, *args, **kwargs):
        """Constructor method - calls _create_abstract_model"""
        super().__init__()
        self._create_abstract_model()
        if args or kwargs:
            self._return_concrete_model(*args, **kwargs)

    def _create_abstract_model(self):
        """Create the abstract model for Resource Allocation Problem."""
        self.Activities = pyo.Set()
        self.Resources = pyo.Set()
        self.Values = pyo.Param(self.Activities)
        self.ResourceNeeds = pyo.Param(self.Resources, self.Activities)
        self.MaxResource = pyo.Param(self.Resources)
        self.MaxActivity = pyo.Param(self.Activities)
        self.NumActivity = pyo.Var(self.Activities, within = pyo.NonNegativeIntegers, bounds = self._get_bounds)

        self.OBJ = pyo.Objective(rule = self._obj_expression, sense = pyo.maximize)
        self.ResourceConstraint = pyo.Constraint(self.Resources, rule = self._resource_constraint_rule)

    def _return_concrete_model(self, *args, **kwargs):
        """Return Pyomo Concrete Model, given data."""
        return self.create_instance(*args, **kwargs)

    def _get_bounds(self, model, p):
        """Upper Bounds for the Decision Vars based on Maximum Demand."""
        return (0, self.MaxActivity[p])

    def _obj_expression(self, model):
        """Objective Expression: Maximizing Value"""
        return pyo.summation(self.Values, self.NumActivity)

    def _resource_constraint_rule(self, model, m):
        """Constraints for Scarce Resources"""
        return sum(self.ResourceNeeds[m, p] * self.NumActivity[p] for p in self.Activities) <= self.MaxResource[m]

def print_sol(instance):
    """Print the solution to the solved `instance`.

    Parameters
    ----------
    instance : :py:class:`pyomo.environ.ConcreteModel`
        A solved model to retrieve objective & variable values.
    """
    print(f"Objective Value: ${instance.OBJ():,}")
    for v in instance.component_objects(pyo.Var, active=True):
        print ("Variable component: ",v)
        for index in v:
            print ("   ", index, v[index].value)