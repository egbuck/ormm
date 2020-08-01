"""
Module contains factory methods & other functions for Mixed Integer Linear Programs (MILP).
"""
import pyomo.environ as pyo

def resource_allocation(*args, **kwargs):
    """
    Factory method for Pyomo Abstract/Concrete Model for the Resource Allocation Problem.

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
    >>> model = resource_allocation()
    >>> instance = model.create_instance("my_params.dat") # AMPL data file
    >>> opt = pyo.SolverFactory("glpk")
    >>> results = opt.solve(instance)
    """
    def _get_bounds(model, p):
        """Upper Bounds for the Decision Vars based on Maximum Demand."""
        return (0, model.MaxActivity[p])

    def _obj_expression(model):
        """Objective Expression: Maximizing Value"""
        return pyo.summation(model.Values, model.NumActivity)

    def _resource_constraint_rule(model, m):
        """Constraints for Scarce Resources"""
        return sum(model.ResourceNeeds[m, p] * model.NumActivity[p] for p in model.Activities) <= model.MaxResource[m]
    ## Create the abstract model for Resource Allocation Problem
    model = pyo.AbstractModel()
    # Define sets/params/vars
    model.Activities = pyo.Set()
    model.Resources = pyo.Set()
    model.Values = pyo.Param(model.Activities)
    model.ResourceNeeds = pyo.Param(model.Resources, model.Activities)
    model.MaxResource = pyo.Param(model.Resources)
    model.MaxActivity = pyo.Param(model.Activities)
    model.NumActivity = pyo.Var(model.Activities, within = pyo.NonNegativeIntegers, bounds = _get_bounds)
    # Define objective & resource constraints
    model.OBJ = pyo.Objective(rule = _obj_expression, sense = pyo.maximize)
    model.ResourceConstraint = pyo.Constraint(model.Resources, rule = _resource_constraint_rule)
    # check if returning concrete or abstract model
    if args or kwargs:
        return model.create_instance(*args, **kwargs)
    else:
        return model


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