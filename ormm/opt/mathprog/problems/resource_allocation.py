"""
===================
Problem Description
===================

---------
Objective
---------

Maximize total profit of selling products produced.

-----------
Constraints
-----------

- A Product p cannot be sold more than its Max Demand
- To sell 1 unit of a product, it must undergo all processing for each machine.  In other words, `sum(ProcessTimes[m,p] for m in Machines)` must happen per product produced. This is implied by the problem parameters and the next constraint.
- The amount of processing time for a machine m must not exceed `MaxTimes[m]`, or `sum(ProcessTimes[m,p] * Produce[p] for p in Products) <= MaxTimes[m]` for all m in machines.

-----------
Definitions
-----------

Sets:
- `Products`: Set of products that are available to produce ⟶ `p in Products`
- `Machines`: Set of machines that are used to produce products ⟶ `m in Machines`

Parameters:
- `Profits`: amount of profit made from producing one unit of Product p ⟶ `Profits[p] for p in Products`
- `ProcessTimes`: amount of time it takes to process Product p on Machine m ⟶ `ProcessTimes[m, p] for m in Machines for p in Products`
- `MaxTimes`: maximum amount of time available to use each Machine m ⟶ `MaxTimes[m] for m in Machines`
- `MaxDemand`: maximum amount of demand for Product p ⟶ `MaxDemand[p] for p in Products`

Decision Variables:
- `Produce`: number of units to produce of Product p ⟶ `Produce[p] for p in Products`
"""

import pyomo.environ as pyo

class ResourceAllocation(pyo.AbstractModel):

    def __init__(self):
        """dat file holds param values for our abstract model"""
        super().__init__()
        self.create_abstract_model()

    def create_abstract_model(self):
        """Create the abstract model for Resource Allocation"""
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
        """Upper Bounds for the Decision Vars based on Maximum Demand"""
        return (0, self.MaxDemand[p])

    def _obj_expression(self, model):
        """Objective Expression: Maximizing Profit"""
        return pyo.summation(self.Profits, self.Produce)

    def _resource_constraint_rule(self, model, m):
        """Constraints for Scarce Resources"""
        return sum(self.ProcessTimes[m, p] * self.Produce[p] for p in self.Products) <= self.MaxTimes[m]

def print_sol(instance, results):
    print(f"Objective Value: ${instance.OBJ():,}")
    for v in instance.component_objects(pyo.Var, active=True):
        print ("Variable component: ",v)
        for index in v:
            print ("   ", index, v[index].value)