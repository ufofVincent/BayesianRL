import random as rand

class BayesianAgent:
    
    def __init__(self, id, cash):
        self.agent_id = id
        self.holdings = 0
        self.cash = cash
        self.holdingLimit = 1000
        self.variance = rand.randint(5, 15)
    
    def take_action(self, midpoint):
        belief = rand.normalvariate(midpoint, self.variance)
        if belief > midpoint:
            k = (abs(belief - midpoint)) / self.variance
            amount = k * self.holdingLimit
            return 1, belief, amount
        elif belief == midpoint:
            return None
        else:
            k = (abs(belief - midpoint)) / self.variance
            amount = k * self.holdingLimit
            return 0, belief, amount
    
