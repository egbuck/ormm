from quantecon.markov import MarkovChain


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


if __name__ == "__main__":
    students_at_university()
