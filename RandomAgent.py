import random as rand
from numpy import random

class RandomAgent:
    
    def __init__(self, agent_id, lam):
        self.agent_id = agent_id
        self.timer = 0
        self.holdingLimit = 10000
        self.lam = lam
    
    # buyPrices are prices at which buyers are willing to buy, which is used when selling
    # sellPrices are prices at which sellers are willing to sell, which is used when buying
    def take_action(self, buyPrices, sellPrices):
        
        # designate 0 to be sell, and 1 to be buy, 2 is do nothing
        decision = rand.randint(0,2)
        if self.timer ==0:
            if decision == 0 and len(buyPrices) != 0:
                price = rand.choice(buyPrices)
                shares = rand.randint(0, self.holdingLimit)
 
                self.timer = random.poisson(self.lam, 1)[0]
                return decision, price, shares
        
            elif decision == 1 and len(sellPrices) != 0:
                price = rand.choice(sellPrices)
                shares = rand.randint(0, self.holdingLimit)
            
                self.timer = random.poisson(self.lam, 1)[0]
                return decision, price, shares
        
            else:
                return None, None, None
        else:
            self.timer -= 1
            return None, None, None
            
        