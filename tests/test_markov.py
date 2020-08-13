from quantecon.markov import MarkovChain
import scipy.stats


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
    # Failure of computers is binomial
    #   p = 0.2 and n = 2
    pmf = scipy.stats.binom.pmf(k=[0, 1, 2], n=2, p=0.2)
    p_0, p_1, p_2 = pmf[0], pmf[1], pmf[2]
    # s_1 = num days first machine been in shop
    # s_2 = num days second has been in shop
    # s_1 = 0 if machine not failed, 1 if in first day of repair, 2 if second
    # 5 possible states - (0,0), (1,0), (2,0), (1,1), (2,1)
    transition_matrix = [[p_0, p_1, 0.0, p_2, 0.0],
                         [0.0, 0.0, 0.8, 0.0, 0.2],
                         [0.8, 0.2, 0.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0, 1.0],
                         [0.0, 1.0, 0.0, 0.0, 0.0]]
    markov = MarkovChain(
        P=transition_matrix,
        state_values=[(0, 0), (1, 0), (2, 0), (1, 1), (2, 1)])
    print(markov)


if __name__ == "__main__":
    students_at_university()
