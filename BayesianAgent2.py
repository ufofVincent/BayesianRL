import numpy as np
import random

class BayesianAgent2:
    
    def __init__(self, agent_id, initial_belief, observations, variance, learning_rate = 0.7, tradingLimit = 1000):
        self.learning_rate = learning_rate
        self.agent_id = agent_id
        self.initial_belief = initial_belief
        self.belief = initial_belief
        self.tradingLimit = tradingLimit
        
        self.curr_iteration = 0
        # self.oberservations = [random.randint(initial_belief, initial_belief * 2)]
        self.obsevations = observations
        self.variance = variance
        
        self.midpoints = []
        
    def take_action(self, midpoint,i):
                
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
                
        self.belief = self.learning_rate * self.belief + (1-self.learning_rate) * np.random.normal(self.obsevations[i], self.variance)
        
        print(self.belief)
        
        self.midpoints.append(midpoint)   
            
        return action, old_belief, amount