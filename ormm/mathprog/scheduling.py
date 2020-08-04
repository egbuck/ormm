"""
"""

import pyomo.environ as pyo


def scheduling(prob_class="employee", **kwargs):
    """
    Calls factory methods for different scheduling problems.

    Parameters
    ----------
    prob_class : str
        Choice of "rental", "employee", & "job shop"
        to return different scheduling models.

    Raises
    ------
    TypeError
        Raised if invalid argument value is given for `prob_class`.
    """
    if prob_class == "rental":
        return _rental(**kwargs)
    elif prob_class == "employee":
        return _employee(**kwargs)
    elif prob_class == "job shop":
        return _job_shop(**kwargs)
    else:
        raise TypeError((
            "Invalid argument value {prob_class}: "
            "must be 'rental', 'employee', or 'job shop'.\n"))


def _rental(**kwargs):
    """
    Factory method for the Rental scheduling problem.

    Parameters
    ----------
    **kwargs : optional
        if any given, returns pyomo concrete model instead, with these passed
        into pyomo's `create_instance`.
    """
    def _obj_expression(model):
        """Objective Expression: Minimizing Number of Workers"""
        my_expr = 0
        for (period, plan) in model.PlanToPeriod:
            my_expr += model.PlanCosts[plan] * model.NumRent[(period, plan)]
        return my_expr

    def _period_reqs_constraint_rule(model, p):
        """Constraints for having enough workers per period"""
        first_member = model.Periods.first()
        last_member = model.Periods.last()
        next_member = model.Periods.next(p, step=1)
        index = model.Periods.ord(p)  # 1 based!!
        set_member = model.Periods[index]  # ?
        print((first_member, last_member, next_member, index, set_member))
        if p == min(model.Periods):
            return (model.PeriodReqs[p],
                    model.NumWorkers[p] + model.NumWorkers[max(model.Periods)],
                    None)
        else:
            return (model.PeriodReqs[p],
                    model.NumWorkers[p] + model.NumWorkers[p - 1], None)

    # Create the abstract model & dual suffix
    model = pyo.AbstractModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    # Define sets/params that are always used
    model.Periods = pyo.Set(ordered=True)
    model.Plans = pyo.Set()
    model.PlanToPeriod = pyo.Set(dimen=2)
    model.PeriodReqs = pyo.Param(model.Periods)
    model.PlanCosts = pyo.Param(model.Plans)
    model.PlanLengths = pyo.Param(model.Plans)
    # Define decision variables
    model.NumRent = pyo.Var(
        model.PlanToPeriod,
        within=pyo.NonNegativeIntegers)
    # Define objective & constraints
    model.OBJ = pyo.Objective(rule=_obj_expression, sense=pyo.minimize)
    model.PeriodReqsConstraint = pyo.Constraint(
        model.Periods,
        rule=_period_reqs_constraint_rule)
    # Check if returning concrete or abstract model
    if kwargs:
        return model.create_instance(**kwargs)
    else:
        return model


def _employee(**kwargs):
    """
    Factory method for the Employee scheduling problem.

    Parameters
    ----------
    **kwargs : optional
        if any given, returns pyomo concrete model instead, with these passed
        into pyomo's `create_instance`.

    Notes
    -----
    Simple model: minimize # of workers employed to meet shift requirements
    """
    def _obj_expression(model):
        """Objective Expression: Minimizing Number of Workers"""
        return pyo.summation(model.NumWorkers)

    def _period_reqs_constraint_rule(model, p):
        """Constraints for having enough workers per period"""
        if p == min(model.Periods):
            return (model.PeriodReqs[p],
                    model.NumWorkers[p] + model.NumWorkers[max(model.Periods)],
                    None)
        else:
            return (model.PeriodReqs[p],
                    model.NumWorkers[p] + model.NumWorkers[p - 1], None)

    # Create the abstract model & dual suffix
    model = pyo.AbstractModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    # Define sets/params that are always used
    model.Periods = pyo.Set()
    model.ShiftLength = pyo.Param()  # num periods a worker works in a row
    model.PeriodReqs = pyo.Param(model.Periods)
    # Define decision variables
    model.NumWorkers = pyo.Var(
        model.Periods,
        within=pyo.NonNegativeIntegers)
    # Define objective & constraints
    model.OBJ = pyo.Objective(rule=_obj_expression, sense=pyo.minimize)
    model.PeriodReqsConstraint = pyo.Constraint(
        model.Periods,
        rule=_period_reqs_constraint_rule)
    # Check if returning concrete or abstract model
    if kwargs:
        return model.create_instance(**kwargs)
    else:
        return model


def _job_shop(**kwargs):
    """
    Factory method for the Job Shop scheduling problem.

    Parameters
    ----------
    **kwargs : optional
        if any given, returns pyomo concrete model instead, with these passed
        into pyomo's `create_instance`.
    """
    pass
