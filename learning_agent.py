import torchbnn as bnn
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import random as rand
class DeepQ:
    def __init__(self, agent_id, input_size, output_size, hidden_size, learning_rate, epsilon, decay, gamma, trade_limit = 1000, starting_cash = 10000000, bayesian = True):
        self.bayesian = bayesian
        self.network = None
        if bayesian:
            self.network = nn.Sequential(
                        bnn.BayesLinear(prior_mu=0, prior_sigma=10, in_features=input_size, out_features=hidden_size),
                        nn.Sigmoid(),
                        bnn.BayesLinear(prior_mu=0, prior_sigma=10, in_features=hidden_size, out_features=output_size),
            )
        else:
            self.network = nn.Sequential(
                nn.Linear(in_features=input_size, out_features=hidden_size),
                nn.Sigmoid(),
                nn.Linear(in_features=hidden_size, out_features=output_size)
            )
        self.decay = decay
        self.trade_limit = trade_limit
        self.agent_id = agent_id
        self.epsilon = epsilon
        self.gamma = gamma
        self.mse_loss = nn.MSELoss()
        self.kl_loss = bnn.BKLLoss(reduction='mean', last_layer_only=False)
        self.kl_weight = 0.01
        self.optimizer = torch.optim.Adam(self.network.parameters(), learning_rate)
        self.samples = 500
        self.num_experiences = 0
        self.experiences = np.array([np.array([0.0000001 for i in range(0, 6)]) for j in range(0, self.samples * 2)])
        self.cash = starting_cash
        self.previous_action = 0
        self.previous_state = np.array([0.0, 0.0])
        self.shares = 0
        self.holdings = 0
        self.rewards = 0
        self.gather_states_tensor =torch.tensor(np.array([np.array([0,1]) for i in range(0,self.samples)])).type(torch.int64)
        self.gather_actions_tensor = torch.tensor(np.array([np.array([2]) for i in range(0,self.samples)])).type(torch.int64)
        self.gather_rewards_tensor = torch.tensor(np.array([np.array([3]) for i in range(0,self.samples)])).type(torch.int64)
        self.gather_next_states_tensor =torch.tensor(np.array([np.array([4,5]) for i in range(0,self.samples)])).type(torch.int64)
    def update_experiences(self, reward, bid_ask):
        experience_tuple = [self.previous_state[0],
                            self.previous_state[1],
                            self.previous_action,
                            reward,
                            bid_ask,
                            self.shares]
        i = self.num_experiences % (2 * self.samples)
        self.experiences[i,] = experience_tuple
        if i == 0:
            self.num_experiences = 0
        self.previous_state = np.array([bid_ask, self.shares])
    def train(self):
        idx = np.random.randint(self.experiences.shape[0], size=self.samples)
        sampled_experiences = self.experiences[idx,:]
        sampled_experiences = torch.tensor(sampled_experiences)
        states = torch.gather(sampled_experiences, 1, self.gather_states_tensor)
        actions = torch.gather(sampled_experiences,1, self.gather_actions_tensor)
        rewards = torch.gather(sampled_experiences,1, self.gather_rewards_tensor)
        next_states = torch.gather(sampled_experiences,1, self.gather_next_states_tensor)
        predictions_s = None
        predictions_s_prime = None
        if self.bayesian:
            for i in range(0, 100):
                sample_s = self.network(states.type(torch.float32))
                sample_s_prime = (self.network(next_states.type(torch.float32)) * self.gamma + rewards)
                if predictions_s == None:
                    predictions_s = sample_s
                else:
                    predictions_s = predictions_s + sample_s
                if predictions_s_prime == None:
                    predictions_s_prime = sample_s_prime
                else:
                    predictions_s_prime = predictions_s_prime + sample_s_prime
            predictions_s = predictions_s / 100
            predictions_s_prime = predictions_s_prime / 100
        else:
            predictions_s = self.network(states.type(torch.float32))
            predictions_s_prime = (self.network(next_states.type(torch.float32)) * self.gamma + rewards)
        q_actions = torch.gather(predictions_s, 1, actions.type(torch.int64))
        q_prime_actions = torch.gather(predictions_s_prime, 1, torch.unsqueeze(predictions_s_prime.argmax(1), 1).type(torch.int64))
        self.optimizer.zero_grad()
        if self.bayesian:
            mse = self.mse_loss(q_actions.float(), q_prime_actions.float())
            kl = self.kl_loss(self.network) * self.kl_weight
            cost = (mse + kl).float()
            cost.backward()
            self.optimizer.step()
        else:
            mse = self.mse_loss(q_actions.float(), q_prime_actions.float())
            cost = mse
            cost.backward()
            self.optimizer.step()
    def take_action(self, x, random = False):
        if random == True:
            explore = rand.uniform(0,1)
            if explore > self.epsilon:
                self.epsilon *= self.decay
                with torch.no_grad():
                    if self.bayesian:
                        samples = []
                        mu = None
                        sigma = torch.tensor(np.array([0.0, 0.0, 0.0]))
                        for i in range(0, 100):
                            sample = self.network(torch.tensor(x).type(torch.float32))
                            samples.append(sample)
                            if mu == None:
                                mu = sample
                            else:
                                mu = (mu + sample)
                        mu = mu / 100
                        for sample in samples:
                            sigma += (((mu - sample) ** 2) / 99)
                        if torch.sum(torch.sqrt(sigma)) >= 73.0:
                            return rand.randint(0,2)
                        return mu.argmax()
                    else:
                        return self.network(torch.tensor(x).type(torch.float32)).argmax()
            else:
                self.epsilon *= self.decay
                return rand.randint(0,2)
        else:
            if self.bayesian:
                samples = []
                mu = None
                sigma = torch.tensor(np.array([0.0, 0.0, 0.0]))
                for i in range(0, 100):
                    sample = self.network(torch.tensor(x).type(torch.float32))
                    samples.append(sample)
                    if mu == None:
                        mu = sample
                    else:
                        mu = (mu + sample)
                mu = mu / 100
                for sample in samples:
                    sigma += (((mu - sample) ** 2) / 99)
                return mu.argmax(), torch.sum(torch.sqrt(sigma))
            else:
                return self.network(torch.tensor(x).type(torch.float32)).argmax()







