import numpy as np
class BayesianAgent2:
    def __init__(self, agent_id, initial_belief, observations, variance, lam, learning_rate = 0.7, tradingLimit = 250):
        self.learning_rate = learning_rate
        self.agent_id = agent_id
        self.initial_belief = initial_belief
        self.belief = initial_belief
        self.tradingLimit = tradingLimit
        self.lam = lam
        self.timer = 0
        self.last_trade_info = 0
        self.curr_iteration = 0
        # self.oberservations = [random.randint(initial_belief, initial_belief * 2)]
        self.obsevations = observations
        self.variance = variance
        # self.midpoints = []
    def take_action(self, midpoint,i):
        action = None
        amount = None
        old_belief = self.belief
        if self.timer != 0:
            if self.belief > midpoint:
                action = 1
                amount = self.tradingLimit
            else:
                action = 0
                amount  = self.tradingLimit
            self.timer = np.random.poisson(self.lam, 1)[0]
            self.belief = self.learning_rate * self.belief + (1-self.learning_rate) * np.random.normal(self.obsevations[i], self.variance)
        # print(self.belief)
        # self.midpoints.append(midpoint)
            return action, old_belief, amount
        else:
            self.timer -= 1
            return None, None, None
