import random as rand
from numpy import random

class BayesianAgent:
    
    def __init__(self, id, variance, lam):
        self.agent_id = id
        self.holdingLimit = 1000
        self.variance = variance
        self.timer = 0
        self.lam = lam
    
    def take_action(self, midpoint):
        belief = rand.normalvariate(midpoint, self.variance)
        if self.timer == 0:
            if belief > midpoint:
                k = (abs(belief - midpoint)) / self.variance

                if k < 1:
                    amount = k * self.holdingLimit
                else:
                    amount = self.holdingLimit
                self.timer = random.poisson(self.lam, 1)
                
                return 1, belief, amount
            elif belief == midpoint:
                return None
            else:
                k = (abs(belief - midpoint)) / self.variance

                if k < 1:
                    amount = k * self.holdingLimit
                else:
                    amount = self.holdingLimit
                self.timer = random.poisson(self.lam, 1)
                return 0, belief, amount
        else:
            self.timer -= 1
            return None
    
