import pyomo.environ as pyo
import pytest

from ormm.mathprog import scheduling
from tests.methods import solve_instance

DATA_PATH = "ormm/mathprog/example_data/"
EMPLOYEE_DATA = DATA_PATH + "employee.dat"
RENTAL_DATA = DATA_PATH + "rental.dat"
AGG_PLANNING_DATA = DATA_PATH + "aggregate_planning.dat"


def test_scheduling_error():
    with pytest.raises(TypeError):
        scheduling("not a scheduling prob class")


def test_employee_simple():
    model = scheduling()
    instance1 = model.create_instance(EMPLOYEE_DATA)
    instance2 = scheduling(filename=EMPLOYEE_DATA)
    for inst in [instance1, instance2]:
        instance, results = solve_instance(inst)
        assert instance.OBJ() == 215
        for v in instance.component_objects(pyo.Var, active=True):
            assert {index: v[index].value for index in v} == {
                1: 0, 2: 65, 3: 70, 4: 30, 5: 0, 6:  45, 7: 5}


def test_rental_simple():
    model = scheduling(prob_class="rental")
    instance1 = model.create_instance(RENTAL_DATA)
    instance2 = scheduling(prob_class="rental", filename=RENTAL_DATA)
    for inst in [instance1, instance2]:
        instance, results = solve_instance(inst)
        assert instance.OBJ() == 1830.0
        for v in instance.component_objects(pyo.Var, active=True):
            assert {index: v[index].value for index in v} == {
                ('Mon', 'DailyWeekDay'): 1.0,
                ('Tue', 'DailyWeekDay'): 0.0,
                ('Wed', 'DailyWeekDay'): 3.0,
                ('Thu', 'DailyWeekDay'): 0.0,
                ('Fri', 'DailyWeekDay'): 2.0,
                ('Sat', 'DailyWeekend'): 0.0,
                ('Sun', 'DailyWeekend'): 0.0,
                ('Mon', 'ThreeWeekDay'): 1.0,
                ('Tue', 'ThreeWeekDay'): 0.0,
                ('Wed', 'ThreeWeekDay'): 0.0,
                ('Sat', 'Weekend'): 0.0,
                ('Mon', 'AllWeekDay'): 4.0,
                ('Sat', 'AllWeek'): 4.0}


def test_agg_planning():
    model = scheduling(prob_class="agg_planning")
    instance1 = model.create_instance(AGG_PLANNING_DATA)
    instance2 = scheduling(prob_class="agg_planning",
                           filename=AGG_PLANNING_DATA)
    for inst in [instance1, instance2]:
        instance, results = solve_instance(inst)
        assert instance.OBJ() == 865_650
        for v in instance.component_objects(pyo.Var, active=True):
            if v.name == "Produce":
                assert {index: v[index].value
                        for index in v} == {'Jan': 1350.0, 'Feb': 1400.0,
                                            'Mar': 1000.0, 'Apr': 550.0,
                                            'May': 1700.0, 'Jun': 2000.0}
            else:
                assert {index: v[index].value
                        for index in v} == {'Jan': 250.0, 'Feb': 250.0,
                                            'Mar': 250.0, 'Apr': 0.0,
                                            'May': 0.0, 'Jun': 100.0}
