History
=======

0.0.1 (2020–07-30)
------------------
* First release on PyPI.
* ResourceAllocation class under ormm.opt.mathprog.problems
* print_sol function under there as well
* tests implemented for both of these
* Documentation available at https://ormm.readthedocs.io/en/stable/

0.0.2 (2020-08-02)
------------------
* ResourceAllocation class has been changed to a factory method, resource_allocation

   * This has many more options now, allowing for integer or linear decision variables,
     multiple amounts of a type of resource, and the option of having an upper bound
     on the decision variables or not.  Note that this last option may be removed
     in the future due to a simpler option of the user using None in their data params.

* sensitivity_analysis function added, which will return a pandas dataframe
* Blending problem class has been added, under the factory method blending

  * This also has the option of making the decision variables linear or integer

* The structure has changed to be simpler - all of these methods/functions are
  now in the milp module (Mixed Integer Linear Programming), and can be
  imported by `from ormm.mathprog import *`.
* tests implemented, and documentation available
  `here <https://ormm.readthedocs.io/en/stable/>`_