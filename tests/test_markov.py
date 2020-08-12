import json

from ormm.markov import markov_discrete_time

MARKOV_PATH = "ormm/markov/example_data/"
INCOME_TAX_DATA = MARKOV_PATH + "income_tax.json"


def _later_test_for_markov():
    json_data = json.load(INCOME_TAX_DATA)
    audit_history = json_data["History"]
    years = json_data["Years"]
    markov_discrete_time(data=audit_history, time_data=years)
