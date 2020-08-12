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
