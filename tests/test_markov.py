from quantecon.markov import MarkovChain
import scipy.stats
import numpy as np


def income_tax_audit():
    """A simple example of markov chain"""
    # Define MarkovChain object - P is transition matrix
    income_tax_audit = MarkovChain(
        P=[[0.6, 0.4],
           [0.5, 0.5]], state_values=[0, 1])
    # Show useful attributes/methods
    print("cdfs()")
    print(income_tax_audit.cdfs)
    print("Simulate")
    print(income_tax_audit.simulate(ts_length=25))
    print("Stationary Distributions")
    print(income_tax_audit.stationary_distributions)


def students_at_university():
    """A simple example of markov chain"""
    # Define MarkovChain object - P is transition matrix
    # Data - this would be more like data from a simulation
    #    or perhaps for later, the steady state probabilities
    data = {0: 10, 1: 20, 2: 30, 3: 15, 4: 15, 5: 10}
    # Average arrival rate
    arrival_rate = sum(hour * count for hour, count in data.items())
    print(arrival_rate)
    # Average interarrival time in minutes
    interarrival_time = (1 / arrival_rate)
    print(interarrival_time * 60)


def computer_repair():
    """
    One worker requires 2 days to repair a machine, and there are 2 of them.
    They fail as independent events: 0.2 to fail, 0.8 to not fail within
        the day.
    We use the binomial distribution to model the event of 0, 1, or 2 failures.
    There are 5 possible states, which we will define as (s_1, s_2):
        s_1 = num days first machine been in shop
        s_2 = num days second has been in shop
        s_1 = 0 if machine not failed, 1 if in first day of repair, 2 if second
        The 5 possible states: (0,0), (1,0), (2,0), (1,1), (2,1)
    """
    # Failure of computers is binomial
    #   p = 0.2 and n = 2
    pmf = scipy.stats.binom.pmf(k=[0, 1, 2], n=2, p=0.2)
    p_0, p_1, p_2 = pmf[0], pmf[1], pmf[2]
    # Define trainsition matrix
    transition_matrix = [[p_0, p_1, 0.0, p_2, 0.0],
                         [0.0, 0.0, 0.8, 0.0, 0.2],
                         [0.8, 0.2, 0.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0, 1.0],
                         [0.0, 1.0, 0.0, 0.0, 0.0]]
    markov = MarkovChain(
        P=transition_matrix,
        state_values=[(0, 0), (1, 0), (2, 0), (1, 1), (2, 1)])
    print(markov)


def light_bulb_replace():
    """
    How many of the bulbs on average will have to be replaced each month?
        How much the budget for the repairs should be?
    Time of fauliure is uncertain
        variety of maintenance optioins
    failed bulbs are replaced monthly - use this for time intervals for dist
    """
    # Define state space, the age of the bulb
    state_space = [0, 1, 2, 3, 4]  # new, 1 month, 2 month, etc.
    num_states = len(state_space)
    num_bulbs = 1_000
    # probability of bulb failing based on age of bulb in months
    prob = [0.5, 0.1, 0.1, 0.1, 0.2]
    cdf = np.cumsum(prob)
    cond_prob = [p / (1 - cdf[ind - 1])
                 if ind > 0 else p for ind, p in enumerate(prob)]
    cond_prob[-1] = 1  # roundoff error overriding
    transition_matrix = np.zeros(shape=(num_states, num_states))
    transition_matrix[:, 0] = cond_prob
    for row in range(num_states - 1):
        transition_matrix[row, row + 1] = 1 - transition_matrix[row, 0]
    print("Transition Matrix:")
    print(transition_matrix)

    # Costs of inspecting & replacing light bulbs
    inspect_cost = 0.10
    replace_cost = 2
    cost_vector = [inspect_cost + replace_cost * transition_matrix[x, 0]
                   for x in range(num_states)]
    print("Cost Vector:")
    print(cost_vector)

    # Transient probabilities
    #  all bulbs start at age 0 (new sign)
    #  estimate how many bulbs will be replaced during each of first 12 months?
    # q(n): probability dist for age of bulb at time n
    q = np.array([[1, 0, 0, 0, 0]])  # row 0 is q(0), row 1 is q(1), etc.
    # q_n = q_(n-1) * P
    for _ in range(1, 13):  # for the 12 months
        q = np.vstack((q, np.matmul(q[-1], transition_matrix)))
    # Calculate expected transient costs - don't include month 0
    exp_trans_cost = np.delete(np.matmul(q, cost_vector), 0)
    total_trans_cost = sum(exp_trans_cost) * num_bulbs
    num_replaced = int(sum(q[1:, 0]) * num_bulbs)
    print("Transient Probabilities:")
    print(q)
    print(f"Expected Total Transient Cost: ${total_trans_cost:,.2f}")
    print(f"Expected # of Replacements: {num_replaced:,d}")


if __name__ == "__main__":
    light_bulb_replace()
