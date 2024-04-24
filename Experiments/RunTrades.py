from ..Agents import RandomAgent
from ..Agents import BayesianAgent
from ..Envirionment import LimitOrderBook
import random
import time

class TradeWorld:

    def __init__(self):
        self.randomAgents = []
        self.bayesianAgents = []

        self.totalAgents = 50
        self.trips = 5
        
        self.fixed_cost = 0
        self.floating_cost = 0
        
        
        self.lob = LimitOrderBook() # need to write a function to read in a limit order book from stock data

        for num in range(1, self.totalAgents):
            if num < self.totalAgents // 2:
                self.randomAgents.append(RandomAgent(num, 10000))
            else:
                self.bayesianAgents.append(BayesianAgent(num, 10000))
                
    def run_trivial_agents(self):
        
        for num in range(1, self.totalAgents):
            
            type = random.choices([0, 1])
            
            currAgent = None
            if type == 0:
                currAgent = self.randomAgents.pop()
            else:
                currAgent = self.bayesianAgents.pop()
                
            cashBeforeTrades = currAgent.cash
            
            values_buy = list(self.lob.buy_orders.values())
            indices_buy = [key for key, val in self.lob.buy_orders.items() if val in values_buy]
                
            values_sell = list(self.lob.sell_orders.values())
            indices_sell = [key for key, val in self.lob.sell_orders.items() if val in values_sell]
            
            for trip in range(1, self.trips):
                
                decision, price, shares = currAgent.take_action(indices_buy, indices_sell)
                
                if decision == 0:
                    currAgent.cash += self.lob.fill_sell_order(price, shares, currAgent.agent_id) - self.fixed_cost - self.floating_cost * shares
                else:
                    currAgent.cash -= self.lob.fill_buy_order(price, shares, currAgent.agent_id) + self.fixed_cost + self.floating_cost * shares
            
            if type == 0:
                print("This random agent made ", (currAgent.cash - cashBeforeTrades))
            else:
                print("This Bayesian agent made ", (currAgent.cash - cashBeforeTrades))
            