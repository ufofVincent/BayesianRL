from ..Agents import RandomAgent
from ..Agents import BayesianAgent
from ..Envirionment import LimitOrderBook
import random
import time

class TradeWorld:

    def __init__(self):
        self.randomAgents = []
        self.bayesianAgents = []

        self.totalAgents = 100
        
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
                
            decision, price, shares = currAgent.take_action()
            
            if decision == 0:
                self.lob.fill_sell_order(price, shares, currAgent.agent_id)
            else:
                self.lob.fill_buy_order(price, shares, currAgent.agent_id)
            
            time.sleep(1)
