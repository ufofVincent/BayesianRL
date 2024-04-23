import random as rand

class RandomAgent:
    
    def __init__(self, id, cash):
        self.agent_id = id
        self.holdings = 0
        self.cash = cash
        self.holdingLimit = 1000
    
    # buyPrices are prices at which buyers are willing to buy, which is used when selling
    # sellPrices are prices at which sellers are willing to sell, which is used when buying
    def take_action(self, buyPrices, sellPrices):
        
        # designate 0 to be sell, and 1 to be buy, 2 is do nothing
        decision = rand.randint(3)
    
        if decision == 0:
            price = rand.choices(buyPrices)
            shares = rand.randint(self.holdingLimit + 1)
            
            self.holdings -= shares    
                
            return decision, price, shares
        
        elif decision == 1:
            price = rand.choices(sellPrices)
            shares = rand.randint(self.holdingLimit + 1)
            
            self.holdings += shares
            
            return decision, price, shares
        
        else:
            
            return None
        