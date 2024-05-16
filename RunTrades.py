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
        self.bayesian_agent_training = np.array([])
        self.nn_agent_training = np.array([])
        self.bayesian_agent_testing = np.array([])
        self.nn_agent_testing = np.array([])
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
        self.agents.append(DeepQ(2, 2, 3, 10, 0.0025, 1, 0.9999, 0.9, bayesian=True))
        self.agents.append(DeepQ(2, 2, 3, 10, 0.0025, 1, 0.9999, 0.9, bayesian=False))
        # self.agents.append(DeepQ(2, 2, 3, 10, 0.0025, 1, 0.99, 0.9, bayesian=True))
        # self.agents.append(DeepQ(2, 2, 3, 10, 0.0025, 1, 0.99, 0.9, bayesian=False))
        self.agents.append(MarketMakerAgent(1, 1))
        self.beliefs = []
        self.midpoints = []
        self.train = True
    def run_simulation(self):
        for i in range(self.iterations):
            if i == self.iterations / 2:
                self.train = False
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
                        if i == self.iterations / 2:
                            agent.rewards = 0
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
                        if self.train:
                            agent.update_experiences(reward, bid_ask)
                        if i % 1000 == 0 and self.train == True:
                            agent.train()
                            # print("training")
                            # print(agent.rewards)
                        sig = 0
                        if self.train:
                            action = agent.take_action(np.array([bid_ask, agent.shares]), random = True)
                        else:
                            if agent.bayesian:
                                action, sig = agent.take_action(np.array([bid_ask, agent.shares]), random = False)
                            else:
                                action = agent.take_action(np.array([bid_ask, agent.shares]), random = False)
                        agent.previous_action = decision
                        if agent.bayesian:
                            if self.train:
                                # self.bayesian_agent_training[i % int(self.iterations / 2)] = agent.rewards
                                self.bayesian_agent_training = np.append(self.bayesian_agent_training, agent.rewards)
                            else:
                                self.bayesian_agent_testing = np.append(self.bayesian_agent_testing, agent.rewards)
                        else:
                            if self.train:
                                # self.nn_agent_training[i % int(self.iterations / 2)] = agent.rewards
                                self.nn_agent_training = np.append(self.nn_agent_training, agent.rewards)
                            else:
                                self.nn_agent_testing = np.append(self.nn_agent_testing, agent.rewards)
                        if action == 1: #take neutral position
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
                        elif action == 0: #take short position
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
world = TradeWorld(100000)
world.run_simulation()
# iteration = [i for i in range(0, len(world.midpoints) - 20)]
# beliefs = world.beliefs
# plt.plot(iteration, world.midpoints[20:])
plt.plot(np.array([i for i in range(0, len(world.bayesian_agent_training))]), world.bayesian_agent_training)
plt.title("Bayesian Agent Training")
plt.xlabel("Iteration")
plt.ylabel("Rewards")
plt.savefig("Bayesian_Agent_Training11")
plt.close()
plt.plot(np.array([i for i in range(0, len(world.nn_agent_training))]), world.nn_agent_training)
plt.title("Non-Bayesian Agent Training")
plt.xlabel("Iteration")
plt.ylabel("Rewards")
plt.savefig("Non-Bayesian_Agent_Training11")
plt.close()
plt.plot(np.array([i for i in range(0, len(world.bayesian_agent_testing))]), world.bayesian_agent_testing)
plt.title("Bayesian Agent Testing")
plt.xlabel("Iteration")
plt.ylabel("Rewards")
plt.savefig("Bayesian_Agent_Testing11")
plt.close()
plt.plot(np.array([i for i in range(0, len(world.nn_agent_testing))]), world.nn_agent_testing)
plt.title("Non-Bayesian Agent Testing")
plt.xlabel("Iteration")
plt.ylabel("Rewards")
plt.savefig("Non-Bayesian_Agent_Testing11")
plt.close()
