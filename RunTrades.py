from LimitOrderBook import LimitOrderBook
from RandomAgent import RandomAgent
from BayesianAgent import BayesianAgent
from BayesianAgent2 import BayesianAgent2
from MarketMakerAgent import MarketMakerAgent
import matplotlib.pyplot as plt
from itertools import islice
from learning_agent import DeepQ
import random
import time
import numpy as np
class TradeWorld:
    def __init__(self, iterations):
        self.iterations = iterations
        self.fixed_cost = 0
        self.floating_cost = 0
        # self.market_shock_timer = np.random.poisson(100000, 1)[0]
        self.current_belief = 0
        # self.cob_duration = 0
        oberservations = [random.randint(80, 120) for i in range(iterations)]
        self.lob = LimitOrderBook() # need to write a function to read in a limit order book from stock data
        self.agents = []
        for i in range(0, 1000):
            self.agents.append(RandomAgent(0, 1))
        for i in range(0,1000):
            self.agents.append(BayesianAgent2(1, 100, oberservations, random.randint(0, 10), 1,  learning_rate=np.random.uniform(0.75, 0.9)))
        
        self.agents.append(DeepQ(2, 2, 3,10, 0.001, 1, 0.99, 0.9, bayesian=True))
        self.agents.append(DeepQ(3, 2, 3,10, 0.001, 1, 0.99, 0.9, bayesian=False))
        self.agents.append(MarketMakerAgent(1, 1))
        self.beliefs = []
        self.midpoints = []
    def run_simulation(self):
        for i in range(self.iterations):
            # agent_list = random.shuffle(self.agents)
            random.shuffle(self.agents)
            # print("LOB Buy Orders: " + str(len(self.lob.buy_orders)))
            # print("LOB Sell Order: " + str(len(self.lob.sell_orders)))
            def take(n, iterable):
                        """Return the first n items of the iterable as a list."""
                        return list(islice(iterable, n))
            decision = None
            shares = None
            price = None
            for agent in self.agents:
                if type(agent) == RandomAgent:
                    top_buys = self.lob.top_n_buy(50)
                    top_sells = self.lob.top_n_sell(50)
                    decision, price, shares = agent.take_action(top_buys, top_sells)
                elif type(agent) == BayesianAgent2:
                    decision, price, shares = agent.take_action(self.lob.mid_point(), i)
                elif type(agent) == MarketMakerAgent:
                    output = agent.take_action(self.lob)
                    if output != None:
                        self.lob = output
                else:
                    try:
                        l1_buy_price = take(1, list(self.lob.buy_orders.keys()))[0]
                        l1_sell_price = take(1, list(self.lob.sell_orders.keys()))[0]
                        l1_buy_volume = sum(tuple[0] for tuple in self.lob.buy_orders[l1_buy_price])
                        l1_sell_volume = sum(tuple[0] for tuple in self.lob.sell_orders[l1_sell_price])
                        bid_ask = l1_buy_volume / l1_sell_volume
                        midpoint = self.lob.mid_point()
                        current_portfolio_val = midpoint * agent.shares + agent.cash
                        previous_portfolio_val = agent.holdings + agent.cash
                        reward = current_portfolio_val - previous_portfolio_val
                        agent.rewards += reward
                        # print(agent.rewards)
                        # agent.holdings = midpoint * agent.shares
                        agent.update_experiences(reward, bid_ask)
                        if i % 10000 == 0:
                            agent.train()
                            print("training")
                            print(agent.rewards)
                        action = agent.take_action(np.array([bid_ask, agent.shares]), random = True)
                        agent.previous_action = decision
                        if action == 0: #take short position
                            if agent.shares == -agent.trade_limit: #do nothing
                                agent.holdings = midpoint * agent.shares
                            elif agent.shares == 0: #take short position from neutral
                                agent.shares = -agent.trade_limit
                                agent.cash = agent.cash + (agent.trade_limit * midpoint)
                                agent.holdings = -agent.trade_limit * midpoint
                            else: #take short position from long
            #                    if we currently have self.shares shares, we need to trade -2000 to get a short position of -self.shares
                                agent.cash = agent.cash + (agent.trade_limit * 2 * midpoint)
                                agent.holdings = -agent.trade_limit * midpoint
                                agent.shares = -agent.trade_limit
                        elif action == 1: #take neutral position
                            if agent.shares == 0: #do nothing
                                agent.holdings = midpoint * agent.shares
                            elif agent.shares == agent.trade_limit: #bail on long position
                                agent.cash = agent.cash + (agent.trade_limit * midpoint)
                                agent.holdings = 0
                                agent.shares = 0
                            else: #bail on short position
                                agent.cash = agent.cash - (agent.trade_limit * midpoint)
                                agent.holdings = 0
                                agent.shares = 0
                        else: #take long position
                            if agent.shares == -agent.trade_limit:
                                agent.cash = agent.cash - (agent.trade_limit * 2 * midpoint)
                                agent.holdings = agent.trade_limit * midpoint
                                agent.shares = agent.trade_limit
                            elif agent.shares == 0:
                                agent.cash = agent.cash - (agent.trade_limit * midpoint)
                                agent.holdings = agent.trade_limit * midpoint
                                agent.shares = agent.trade_limit
                            else:
                                agent.holdings = midpoint * agent.shares
                    except:
                        continue
                if decision == 0:
                    #print(belief)
                    self.lob.fill_sell_order(price, shares, agent.agent_id)
                elif decision == 1:
                    #print(belief)
                    self.lob.fill_buy_order(price, shares, agent.agent_id)
                else:
                    continue
            # self.midpoints.append(self.lob.mid_point())
            print("Iteration " + str(i) + " finished")
world = TradeWorld(1000000)
world.run_simulation()
# iteration = [i for i in range(0, len(world.midpoints) - 20)]
# beliefs = world.beliefs
# plt.plot(iteration, world.midpoints[20:])
plt.show()
