"""
"""

import pyomo.environ as pyo


def scheduling(prob_class="employee", linear=False, **kwargs):
    """
    Calls factory methods for different scheduling problems.

    The `prob_class` parameter allows the user to choose from different
    types of problem classes, which in turn have different model structures.

    The valid choices are:

    - :py:obj:`employee` (default):  A simple employee scheduling problem to
      minimize the number of workers employed to meet period requirements.
      Currently assumes that a worker works their periods in a row
      (determined by `ShiftLenth` parameter).

    - :py:obj:`rental`:  A type of scheduling problem where there are different
      plans (with different durations & costs), and the goal is to minimize the
      total cost of the plans purchased while meeting the period requirements
      (covering constraints).

    More details on these model classes can be found in the Notes section here,
    as well as the corresponding section of the :ref:`problem_desc`.

    Parameters
    ----------
    prob_class : :py:obj:`str`, optional
        Choice of "employee", "rental", or "agg_planning"
        to return different scheduling models.
    linear : :py:obj:`bool`, optional
        Determines whether decision variables will be
        Reals (True) or Integer (False).
    **kwargs
        Passed into Pyomo Abstract Model's `create_instance`
        to return Pyomo Concrete Model instead.

    Raises
    ------
    TypeError
        Raised if invalid argument value is given for `prob_class`.

    Notes
    -----
    The employee model minimizes workers hired with covering constraints:

    .. math::

       \\text{Min}  \\sum_{p \\in P} X_p

       \\text{s.t.} \\sum_{p - (L - 1)}^p X_p \\geq R_p
           \\quad \\forall p \\in P

       X_p \\geq 0\\text{, int} \\quad \\forall p \\in P

    The rental model minimizes cost of plans purchased
    with covering constraints:

    .. math::

       \\text{Min}  \\sum_{a \\in A} C_a
           \\sum_{p \\in P \\, \\mid \\, (p,a) \\in J} X_{(p,a)}

       \\text{s.t.} \\sum_{j \\in J \\, \\mid \\, f} X_j \\geq R_p
           \\quad \\forall p \\in P

       X_j \\geq 0\\text{, int} \\quad \\forall j \\in J

    The aggregate planning model minimizes production & holding costs
    while meeting demand over a number of periods:

    .. math::

       \\text{Min}  \\sum_{p \\in P} C_pX_p &+ H_pY_p

       \\text{s.t.} \\enspace Y_{p-1} + X_p - Y_p &= D_p
       &\\forall p \\in P

       Y_p &\\leq M_p &\\forall p \\in P

       Y_{\\min(p)-1} &= I_F

       Y_{\\max(p)} &= I_L

       X_p, \\, Y_p &\\geq 0\\text{, int} &\\forall p \\in P
    """
    if prob_class.lower() == "rental":
        return _rental(**kwargs)
    elif prob_class.lower() == "employee":
        return _employee(**kwargs)
    elif prob_class.lower() == "agg_planning":
        return _aggregate_planning(**kwargs)
    else:
        raise TypeError((
            "Invalid argument value {prob_class}: "
            "must be 'rental', 'employee', or 'job shop'.\n"))


def _rental(linear=False, **kwargs):
    """
    Factory method for the Rental scheduling problem.

    Parameters
    ----------
    linear : :py:obj:`bool`, optional
        Determines whether decision variables will be
        Reals (True) or Integer (False).
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
        num_periods = len(model.Periods)
        my_sum = 0
        sum_terms = []
        for (period, plan) in model.PlanToPeriod:
            # Get index of current period
            ind = model.Periods.ord(p)
            # Get effective periods based on PlanLength
            periods_in_plan = [
                model.Periods[(
                    (ind - 1 - pl) % num_periods) + 1]
                for pl in range(model.PlanLengths[plan])]
            periods_in_plan = [per for per in periods_in_plan
                               if (per, plan) in model.PlanToPeriod]
            # Sum up how many rented in effective periods
            # new_terms makes sure that not adding same term again
            new_terms = [(p_in_plan, plan)
                         for p_in_plan in periods_in_plan
                         if (p_in_plan, plan) not in sum_terms]
            my_sum += sum([model.NumRent[term] for term in new_terms])
            sum_terms.extend(new_terms)
        return my_sum >= model.PeriodReqs[p]

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
        within=pyo.NonNegativeReals if linear else pyo.NonNegativeIntegers)
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


def _employee(linear=False, **kwargs):
    """
    Factory method for the Employee scheduling problem.

    Parameters
    ----------
    linear : :py:obj:`bool`, optional
        Determines whether decision variables will be
        Reals (True) or Integer (False).
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
        # Get index of current period
        ind = model.Periods.ord(p)
        num_periods = len(model.Periods)
        # Get effective periods based on ShiftLength - loops back
        effective_periods = [
            model.Periods[((ind - 1 - shift) % num_periods) + 1]
            for shift in range(model.ShiftLength.value)]
        # Sum up how many workers are working this period
        my_sum = sum([model.NumWorkers[period]
                      for period in effective_periods])
        return my_sum >= model.PeriodReqs[p]

    # Create the abstract model & dual suffix
    model = pyo.AbstractModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    # Define sets/params that are always used
    model.Periods = pyo.Set(ordered=True)
    model.ShiftLength = pyo.Param()  # num periods a worker works in a row
    model.PeriodReqs = pyo.Param(model.Periods)
    # Define decision variables
    model.NumWorkers = pyo.Var(
        model.Periods,
        within=pyo.NonNegativeReals if linear else pyo.NonNegativeIntegers)
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


def _aggregate_planning(linear=False, **kwargs):
    """
    Factory method returning Pyomo Abstract/Concrete Model
    for the Aggregate Planning Problem

    Parameters
    ----------
    **kwargs
        Passed into Pyomo Abstract Model's `create_instance`
        to return Pyomo Concrete Model instead.

    Notes
    -----
    """
    def _obj_expression(model):
        """Objective Expression: """
        return (pyo.summation(model.Cost, model.Produce)
                + model.HoldingCost * pyo.summation(model.InvLevel))

    def _conserve_flow_constraint_rule(model, p):
        """Constraints for """
        ind = model.Periods.ord(p)
        if ind == 1:
            return (model.InitialInv + model.Produce[p]
                    - model.InvLevel[p] == model.Demand[p])
        else:
            last_p = model.Periods[ind - 1]
            return (model.InvLevel[last_p] + model.Produce[p]
                    - model.InvLevel[p] == model.Demand[p])

    def _max_storage_constraint_rule(model, p):
        return (0, model.InvLevel[p], model.MaxStorage)

    def _final_inv_constraint_rule(model):
        last_period = model.Periods[-1]
        return model.InvLevel[last_period] == model.FinalInv

    # Create the abstract model & dual suffix
    model = pyo.AbstractModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    # Define sets/params that are always used
    model.Periods = pyo.Set(ordered=True)
    model.Cost = pyo.Param(model.Periods)
    model.Demand = pyo.Param(model.Periods)
    model.HoldingCost = pyo.Param()
    model.MaxStorage = pyo.Param(within=pyo.Any, default=None)
    model.InitialInv = pyo.Param(default=0)
    model.FinalInv = pyo.Param(default=0)
    # Define decision variables
    model.Produce = pyo.Var(
        model.Periods,
        within=pyo.NonNegativeReals if linear else pyo.NonNegativeIntegers)
    model.InvLevel = pyo.Var(
        model.Periods,
        within=pyo.NonNegativeReals if linear else pyo.NonNegativeIntegers)
    # Define objective & constraints
    model.OBJ = pyo.Objective(rule=_obj_expression, sense=pyo.minimize)
    model.ConserveFlowConstraint = pyo.Constraint(
        model.Periods,
        rule=_conserve_flow_constraint_rule)
    model.MaxStorageConstraint = pyo.Constraint(
        model.Periods,
        rule=_max_storage_constraint_rule)
    model.FinalInvConstraint = pyo.Constraint(
        rule=_final_inv_constraint_rule)
    # Check if returning concrete or abstract model
    if kwargs:
        return model.create_instance(**kwargs)
    else:
        return model
