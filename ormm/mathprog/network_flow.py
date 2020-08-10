import pyomo.environ as pyo


def transportation(**kwargs):
    """
    Factory method for the transportation problem class

    This is a bipartite network with m supply nodes, n destination nodes
    If not possible to ship from i to j, a large cost M should be passed

    Assumes the feasibility property holds
        (total supply equals total demand)
        then becomes balanced TP
    Will be modified so req satisfied
        let \\delta be the excess
        add dummy source with index m + 1 if demand > supply
            s_{m+1} = \\delta ; c_{m+1,j}=0 for all j
        add dummy demand with index n + 1 if supply > demand
            d_{n+1} = \\delta ; c_{i,n+1}=0 for all i
    d.v.: x_{i,j} - flow from source i to destination j
    """
    def _obj_expression(model):
        """Objective Expression: Maximizing Value"""
        return pyo.summation(model.ShippingCosts, model.Flows)

    def _supply_constraint_rule(model, i):
        """Constraints for Scarce Resources"""
        return sum(model.Flows[i, j]
                   for j in model.Destinations) == model.Supply[i]

    def _demand_constraint_rule(model, j):
        return sum(model.Flows[i, j]
                   for i in model.Supply) == model.Demand[j]

    # Create the abstract model & dual suffix
    model = pyo.AbstractModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    # Define sets/params that are always used
    model.Sources = pyo.Set()
    model.Destinations = pyo.Set()
    model.Supply = pyo.Param(model.Sources)
    model.Demand = pyo.Param(model.Destinations)
    model.ShippingCosts = pyo.Param(model.Sources, model.Destinations)
    # Define decision variables
    model.Flows = pyo.Var(
        model.Sources,
        model.Destinations,
        within=pyo.NonNegativeReals,
        bounds=(0, None))
    # Define objective & constraints
    model.OBJ = pyo.Objective(rule=_obj_expression, sense=pyo.minimize)
    model.SupplyConstraint = pyo.Constraint(
        model.Sources,
        rule=_supply_constraint_rule)
    model.DemandConstraint = pyo.Constraint(
        model.Destinations,
        rule=_demand_constraint_rule)
    # Check if returning concrete or abstract model
    if kwargs:
        return model.create_instance(**kwargs)
    else:
        return model
