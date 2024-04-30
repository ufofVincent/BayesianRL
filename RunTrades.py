from LimitOrderBook import LimitOrderBook
from RandomAgent import RandomAgent
from BayesianAgent import BayesianAgent
from BayesianAgent2 import BayesianAgent2
import matplotlib.pyplot as plt
from itertools import islice

import random
import time
from numpy import random

class TradeWorld:

    def __init__(self, iterations):
        # self.randomAgents = []
        # self.bayesianAgents = []
        random_a = RandomAgent(1, 5)
        random_a_2 = RandomAgent(1, 5)
        bayesian_a = BayesianAgent(2, 10, 5)
        bayesian_a_2 = BayesianAgent(2, 10, 5)
        self.bayesian_a_2 = BayesianAgent2(3, 100)
        self.bayesian_a_2_2 = BayesianAgent2(3, 100)

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
        
        self.agents = []
        
        for i in range(0, 3):
            self.agents.append(BayesianAgent(2, 10, 5))
        
        for i in range(0, 3):
            self.agents.append(RandomAgent(1, 5))
            
        for i in range(0,3):
            self.agents.append(BayesianAgent2(3, 100))
        
        self.beliefs = []
        self.midpoints = []
                
    def run_simulation(self):
        for i in range(self.iterations):
            # agent_list = random.shuffle(self.agents)
            
            random.shuffle(self.agents)
            
            
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
                    
                    def take(n, iterable):
                        """Return the first n items of the iterable as a list."""
                        return list(islice(iterable, n))
                    
                    top_twenty_buys = take(20, list(self.lob.buy_orders.keys()))
                    top_twemty_sells = take(20, list(self.lob.sell_orders.keys()))
                    
                    
                    decision, price, shares = agent.take_action(top_twenty_buys, top_twemty_sells)
                elif type(agent) == BayesianAgent:
                    belief = 0
                    if self.crash_or_bubble == False:
                        if i == 0:
                            belief = 100
                        else:
                            belief = self.lob.mid_point()
                    elif self.crash_or_bumble == False and self.market_shock_timer == 0:
                        belief = abs(self.lob.mid_point() + ((self.lob.mid_point() * random.randint(0.10, 0.20)) * random.choice([-1, 1])))
                        self.cob_duration = random.poisson(250, 1)[0]
                        self.current_belief = belief
                        self.crash_or_bubble == True
                    else:
                        belief = self.current_belief
                        self.cob_duration -= 1
                    if belief == None:
                        decision, price, shares = agent.take_action(100)
                    else:
                        decision, price, shares = agent.take_action(belief)
                else:
                    decision, price, shares = agent.take_action(self.lob.mid_point())
                
                if decision == 0:
                    #print(belief)
                    average_transacted, amount = self.lob.fill_sell_order(price, shares, agent.agent_id)
                elif decision == 1:
                    #print(belief)
                    average_transacted, amount = self.lob.fill_buy_order(price, shares, agent.agent_id)
                else:
                    continue
                
                self.midpoints.append(self.lob.mid_point())
                
            self.market_shock_timer -= 1
            
            
            # if type == 0:
            #     print("This random agent made ", (currAgent.cash - cashBeforeTrades))
            # else:
            #     print("This Bayesian agent made ", (currAgent.cash - cashBeforeTrades))
            
            if belief != None:
                
                self.beliefs.append(abs(belief))
            else:
                print("None!")
                self.beliefs.append(0)
            # print(i)
            
world = TradeWorld(10000)
world.run_simulation()
iteration = [i for i in range(0, len(world.midpoints))]
beliefs = world.beliefs
plt.plot(iteration, world.midpoints)
plt.show()
