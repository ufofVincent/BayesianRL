from LimitOrderBook import LimitOrderBook
from RandomAgent import RandomAgent
from BayesianAgent import BayesianAgent
import matplotlib.pyplot as plt

import random
import time
from numpy import random

class TradeWorld:

    def __init__(self, iterations):
        # self.randomAgents = []
        # self.bayesianAgents = []
        random_a = RandomAgent(1, 30)
        bayesian_a = BayesianAgent(2, 20, 20)

        # self.totalAgents = 50
        # self.trips = 5
        self.iterations = iterations
        self.fixed_cost = 0
        self.floating_cost = 0
        self.market_shock_timer = random.poisson(10000, 1)[0]
        self.crash_or_bubble = False
        self.current_belief = 0
        self.cob_duration = 0
        
        self.lob = LimitOrderBook() # need to write a function to read in a limit order book from stock data

        # for num in range(1, self.totalAgents):
        #     if num < self.totalAgents // 2:
        #         self.randomAgents.append(RandomAgent(num, 10000))
        #     else:
        #         self.bayesianAgents.append(BayesianAgent(num, 10000))
        
        self.agents = [bayesian_a, random_a]
        self.beliefs = []
                
    def run_simulation(self):
        for i in range(self.iterations):
            # agent_list = random.shuffle(self.agents)
            for agent in self.agents:
            
            # for num in range(1, self.totalAgents):
            
            #     type = random.choices([0, 1])
            
            #     currAgent = None
            #     if type == 0:
            #         currAgent = self.randomAgents.pop()
            #     else:
            #         currAgent = self.bayesianAgents.pop()
                
            #     cashBeforeTrades = currAgent.cash
                if self.cob_duration == 0:
                    self.crash_or_bubble = False
                    self.current_belief = 0
                    self.market_shock_timer = random.poisson(10000, 1)[0]
            
                if type(agent) == RandomAgent:
                    decision, price, shares = agent.take_action(list(self.lob.buy_orders.keys()), list(self.lob.sell_orders.keys()))
                else:
                    belief = 0
                    if self.crash_or_bubble == False:
                        if i == 0:
                            belief = 100
                        else:
                            belief = self.lob.mid_point()
                    elif self.crash_or_bumble == False and self.market_shock_timer == 0:
                        belief = abs(self.lob.mid_point() + ((self.lob.mid_point() * random.randint(0.10, 0.50)) * random.choice([-1, 1])))
                        self.cob_duration = random.poisson(1000, 1)[0]
                        self.current_belief = belief
                        self.crash_or_bubble == True
                    else:
                        belief = self.current_belief
                        self.cob_duration -= 1
                    if belief == None:
                        decision, price, shares = agent.take_action(100)
                    else:
                        decision, price, shares = agent.take_action(belief)
                
                if decision == 0:
                    print(price)
                    average_transacted, amount = self.lob.fill_sell_order(price, shares, agent.agent_id)
                elif decision == 1:
                    print(price)
                    average_transacted, amount = self.lob.fill_buy_order(price, shares, agent.agent_id)
                else:
                    continue
            self.market_shock_timer -= 1
            
            
            # if type == 0:
            #     print("This random agent made ", (currAgent.cash - cashBeforeTrades))
            # else:
            #     print("This Bayesian agent made ", (currAgent.cash - cashBeforeTrades))
            print(belief)
            self.beliefs.append(abs(belief))
            # print(i)
world = TradeWorld(1000000)
world.run_simulation()
iteration = [i for i in range(0, 1000000)]
beliefs = world.beliefs
plt.plot(iteration, beliefs)
plt.show()
