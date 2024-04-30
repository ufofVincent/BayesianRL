import numpy as np
import random

class BayesianAgent2:
    
    def __init__(self, agent_id, initial_belief, learning_rate = 0.7, tradingLimit = 1000):
        self.learning_rate = learning_rate
        self.agent_id = agent_id
        self.initial_belief = initial_belief
        self.belief = initial_belief
        self.tradingLimit = tradingLimit
        
        self.midpoints = []
        
    def take_action(self, midpoint):
                
        action = None
        amount = None
        
        old_belief = self.belief
                
        if self.belief > midpoint:
            
            action = 1
            percetange = (self.belief - midpoint) / self.belief
            
            if percetange > 0.2:
                amount = self.tradingLimit
            else:
                amount = self.tradingLimit * (percetange / 0.2)
                
            
        else:
            
            action = 0
            percetange = (midpoint - self.belief) / self.belief
            
            if percetange > 0.2:
                amount = self.tradingLimit
            else:
                amount = self.tradingLimit * (percetange / 0.2)
                
        self.belief = self.learning_rate * self.belief + (1-self.learning_rate) * midpoint
        
        print(self.belief)
        
        self.midpoints.append(midpoint)   
            
        return action, old_belief, amount