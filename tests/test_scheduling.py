import pyomo.environ as pyo

from ormm.mathprog import scheduling
from tests.methods import solve_instance

DATA_PATH = "ormm/mathprog/example_data/"
EMPLOYEE_DATA = DATA_PATH + "employee.dat"
RENTAL_DATA = DATA_PATH + "rental.dat"


def test_employee_simple():
    model = scheduling()
    instance1 = model.create_instance(EMPLOYEE_DATA)
    instance2 = scheduling(filename=EMPLOYEE_DATA)
    for inst in [instance1, instance2]:
        instance, results = solve_instance(inst)
        assert instance.OBJ() == 295
        for v in instance.component_objects(pyo.Var, active=True):
            assert {index: v[index].value for index in v} == {
                1: 55, 2: 115, 3: 85, 4: 0, 5: 25, 6: 15}


def test_rental_simple():
    model = scheduling(prob_class="rental")
    instance1 = model.create_instance(RENTAL_DATA)
    instance1.pprint()
    instance2 = scheduling(prob_class="rental", filename=RENTAL_DATA)
    # for inst in [instance1, instance2]:
    #     instance, results = solve_instance(inst)
    #     assert instance.OBJ() == 295
    #     for v in instance.component_objects(pyo.Var, active=True):
    #         print({index: v[index].value for index in v})
    #         assert {index: v[index].value for index in v} == {
    #             ("Sat", "DailyWeekend"): 0.0,
    #             ("Sun", "DailyWeekend"): 0.0,
    #             ("Mon", "DailyWeekDay"): 5.0,
    #             ("Tue", "DailyWeekDay"): 0.0,
    #             ("Wed", "DailyWeekDay"): 9.0,
    #             ("Thu", "DailyWeekDay"): 0.0,
    #             ("Fri", "DailyWeekDay"): 4.0,
    #             ("Mon", "ThreeWeekDay"): 0.0,
    #             ("Tue", "ThreeWeekDay"): 0.0,
    #             ("Wed", "ThreeWeekDay"): 2.0,
    #             ("Sat", "Weekend"): 0.0,
    #             ("Mon", "AllWeekDay"): 0.0,
    #             ("Sat", "AllWeek"): 5.0
    #         }


if __name__ == "__main__":
    test_rental_simple()
