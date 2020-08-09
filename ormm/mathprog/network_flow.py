import pyomo.environ as pyo


def transportation(linear=False, **kwargs):
    """
    Factory method for the transportation problem class

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
        return pyo.summation(model.Cost, model.Blend)

    def _property_constraint_rule(model, p):
        """Constraints for Scarce Resources"""
        return (model.MinProperty[p], sum(
            model.IngredientProperties[i, p]
            * model.Blend[i]
            for i in model.Ingredients
            ), model.MaxProperty[p])

    def _conservation_constraint_rule(model):
        return pyo.summation(model.Blend) == 1

    # Create the abstract model & dual suffix
    model = pyo.AbstractModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    # Define sets/params that are always used
    model.Sources = pyo.Set()
    model.Destinations = pyo.Set()
    model.Supply = pyo.Param(model.Sources)
    model.Demand = pyo.Param(model.Destinations)
    model.ShippingCosts = pyo.Param(model.Ingredients, model.Properties)
    # Define decision variables
    model.Flow = pyo.Var(
        model.Sources,
        model.Destinations,
        within=pyo.NonNegativeReals if linear else pyo.NonNegativeIntegers,
        bounds=(0, None))
    # Define objective & constraints
    model.OBJ = pyo.Objective(rule=_obj_expression, sense=pyo.minimize)
    model.PropertyConstraint = pyo.Constraint(
        model.Properties,
        rule=_property_constraint_rule)
    model.ConservationConstraint = pyo.Constraint(
        rule=_conservation_constraint_rule)
    # Check if returning concrete or abstract model
    if kwargs:
        return model.create_instance(**kwargs)
    else:
        return model
