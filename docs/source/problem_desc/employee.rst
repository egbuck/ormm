Employee Scheduling Problem
===========================
The Employee Scheduling Problem minimizes the number of workers hired
while satisfying the minimum number of workers required for each period.
These constraints are commonly called the `covering constraints` in
other scheduling problems.
ORMM's current implementation of this problem class has limitations.
It assumes that the worker works in "Shifts" that are in a row.
For example, if the periods were days, and `ShiftLength` was set to 5,
then it assumes that when a worker starts working on a Monday, then
they will work Monday through Friday, and will be off on the weekend.
This is because the decision variables in this implementation are
interpreted as the number of workers that start their shift on `Period p`.
This simplifies the model, and allows it to be an effective MILP.
This type of problem occurs in management decisions where workers' schedules
may not be constant, such as nurse scheduling or hourly staff.

Definitions
-----------

Sets
""""
- :py:obj:`Periods` - Set of periods where workers are needed

   - :py:obj:`p in Periods` or :math:`p \in P`

Parameters
""""""""""
- :py:obj:`PeriodReqs` - measure of number of workers needed for :py:obj:`Period p`

   - :py:obj:`PeriodReqs[p] for p in Periods` or :math:`R_p \enspace \forall p \in P`

- :py:obj:`ShiftLength` - measure of how many periods in a row a worker will work

   - :py:obj:`ShiftLength` or :math:`L`

Decision Variables
""""""""""""""""""
- :py:obj:`NumWorkers` - number of workers that work a shift starting
  on :py:obj:`Period p`

   - :py:obj:`NumWorkers[p] for p in Periods` or
     :math:`X_p \enspace \forall p \in P`

Objective
---------
**Minimize** total number of workers (in the model, hired, etc.).

.. math::

   \text{Min} \sum_{p \in P} X_p

Constraints
-----------
- The number of workers that are working for each period must be greater than
  or equal to the minimum required - :py:obj:`PeriodReqs[p]`.  Obtaining the
  number of workers that are present in each period requires using both the
  decision variables (what day a worker starts their shift) as well as the
  :py:obj:`ShiftLength` parameter.  For example, if the :py:obj:`ShiftLength`
  is 2, and there are 10 workers that start Monday, 15 workers that start Tuesday,
  and 25 workers that start Wednesday, 40 workers would be present on Wednesday.
  If we are at the first period given by the data, the model has to go back to the
  last period given as well - in our example, this would be saying the number of
  workers present on Sunday (the beginning of the week) is the number of workers
  that start on Sunday plus the number of workers that start on Saturday
  (the end of the week).  In mathematical terms, this can be represented by

.. math::

   \sum_{p - (L - 1)}^p X_p \leq R_p \quad \forall p \in P

where :math:`P` is a cyclically ordered set (or a cycle) and the start
of the sum goes back :math:`L - 1` terms in that set.

- The decision variables must be greater than or equal to zero and integer.

.. math::

    X_p \geq 0\text{, int} \enspace \forall p \in P

API Reference
-------------
See the corresponding section in the :ref:`api_reference` to learn more
about how to use the API for this problem class.