import random

class SlotMachine():

    def __init__(
        self,
        n_arms,
        timesteps_per_episode,
        stationary = True, 
        init_true_q = None,
        n_agents = 1
    ): 
        self.n_arms = n_arms
        self.timesteps = timesteps_per_episode
        self.stationary = stationary
        self.init_true_q = init_true_q
        if not self.init_true_q:
            self.true_q_values = [
                random.gauss(0, 1) for _ in range(self.n_arms)
            ]
        elif type(self.init_true_q) == float:
            self.true_q_values = [
                self.init_true_q for _ in range(self.n_arms)
            ]
        elif type(self.init_true_q) == list:
            self.true_q_values = self.init_true_q
        self.n_agents = n_agents
        self.counter = 0

    def get_reward(self, action):
        reward = random.gauss(self.true_q_values[action], 1)
        self.counter += 1
        if self.counter == self.n_agents:
            self._add_noise()
            self.counter = 0
        return reward
    
    def get_timesteps(self):
        return self.timesteps
    
    def _add_noise(self):
        if not self.stationary:
            self.true_q_values = [
                v + random.gauss(0, 0.01) for v \
                    in self.true_q_values
            ]
    
    def optimal_action(self):
        max_q = max(self.true_q_values)
        action = self.true_q_values.index(max_q)
        return action
    
    def reset(self):
        if not self.init_true_q:
            self.true_q_values = [
                random.gauss(0, 1) for _ in range(self.n_arms)
            ]
        elif type(self.init_true_q) == float:
            self.true_q_values = [
                self.init_true_q for _ in range(self.n_arms)
            ]
        elif type(self.init_true_q) == list:
            self.true_q_values = self.init_true_q