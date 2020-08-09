import pyomo.environ as pyo

from ormm.mathprog import transportation
from tests.methods import solve_instance

MATHPROG_DATA = "ormm/mathprog/example_data/"
TRANSPORTATION_DATA = MATHPROG_DATA + "transportation.dat"


def test_transportation():
    model = transportation()
    instance1 = model.create_instance(TRANSPORTATION_DATA)
    instance2 = transportation(filename=TRANSPORTATION_DATA)
    for inst in [instance1, instance2]:
        instance, results = solve_instance(inst)
        assert instance.OBJ() == 475
        for v in instance.component_objects(pyo.Var, active=True):
            assert {index: v[index].value
                    for index in v} == {
                        ('S1', 'D1'): 0.0, ('S1', 'D2'): 5.0,
                        ('S1', 'D3'): 5.0, ('S1', 'D4'): 5.0,
                        ('S1', 'D5'): 0.0, ('S2', 'D1'): 0.0,
                        ('S2', 'D2'): 5.0, ('S2', 'D3'): 0.0,
                        ('S2', 'D4'): 0.0, ('S2', 'D5'): 10.0,
                        ('S3', 'D1'): 5.0, ('S3', 'D2'): 0.0,
                        ('S3', 'D3'): 10.0, ('S3', 'D4'): 0.0,
                        ('S3', 'D5'): 0.0}


if __name__ == "__main__":
    test_transportation()
