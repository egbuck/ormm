# Problem Description

# Definitions
Sets:
* `Products`: Set of products that are available to produce ⟶ `p in Products`
* `Machines`: Set of machines that are used to produce products ⟶ `m in Machines`

Parameters:
* `Profits`: amount of profit made from producing one unit of Product p ⟶ `Profits[p] for p in Products`
* `ProcessTimes`: amount of time it takes to process Product p on Machine m ⟶ `ProcessTimes[m, p] for m in Machines for p in Products`
* `MaxTimes`: maximum amount of time available to use each Machine m ⟶ `MaxTimes[m] for m in Machines`
* `MaxDemand`: maximum amount of demand for Product p ⟶ `MaxDemand[p] for p in Products`

Decision Variables:
* `Produce`: number of units to produce of Product p ⟶ `Produce[p] for p in Products`
