#%%
import multiprocessing
import copy

class Testbed():

    def __init__(
        self,
        n_runs,
        environment,
        agents
    ):
        self.n_runs = n_runs
        self.env = environment
        self.agents = [agent[0] for agent in agents] # list of tuples of the form (object of class Player, 'name')
        self.agents_names = [agent[1] for agent in agents]
        n_timesteps = self.env.get_timesteps()
        self.results = {}
        for agent_name in self.agents_names:
            self.results[agent_name] = {
                'rewards': [[None for _ in range(n_timesteps)] for _ in range(self.n_runs)],
                'optimal_action': [[None for _ in range(n_timesteps)] for _ in range(self.n_runs)]
            }

    # def _reset_env_and_agents(self):
    #     self.env.reset()
    #     for agent in self.agents:
    #             agent.reset()

    def _choose_actions(self, env, run, timestep):
        optimal_action = env.optimal_action()
        actions = []
        for agent, agent_name in zip(self.agents, self.agents_names):
            action = agent.choose_action()
            actions.append(action)
            self.results[agent_name]['optimal_action'][run][timestep] = \
                action == optimal_action
        return actions

    def _get_rewards(self, env, actions, run, timestep):
        rewards = []
        for i, agent_name in enumerate(self.agents_names):
            reward = env.get_reward(actions[i])
            rewards.append(reward)
            self.results[agent_name]['rewards'][run][timestep] = reward
        return rewards 

    def _update_agents(self, actions, rewards):
        for agent, (action, reward) in zip(self.agents, zip(actions, rewards)):
            agent.update(action, reward)

    def _perform_one_run(self, run):
        env = copy.deepcopy(self.env)
        n_timesteps = self.env.get_timesteps()
        for timestep in range(n_timesteps):
            actions = self._choose_actions(env, run, timestep)
            rewards = self._get_rewards(env, actions, run, timestep)
            self._update_agents(actions, rewards)
        # for agent_name in self.agents_names:
        #     for key in ['rewards', 'optimal_action']:
        #         self.results[agent_name][key] = self.results[agent_name][key]

    def run_experiment(self):
        # n_timesteps = self.env.get_timesteps()
        # for run in range(self.n_runs):
        #     self._reset_env_and_agents()
        #     for timestep in range(n_timesteps):
        #         actions = self._choose_actions(run, timestep)
        #         rewards = self._get_rewards(actions, run, timestep)
        #         self._update_agents(actions, rewards)
        runs = [run for run in range(n_runs)]
        p = multiprocessing.Pool()
        p.map(self._perform_one_run, runs)

#%%
from environment import SlotMachine
from agent import Player, Strategy
n_runs = 2000
n_timesteps = 10000
n_arms = 10
strategy = Strategy(
    'eps_greedy',
    0.1
)
environment = SlotMachine(
    n_arms = n_arms, 
    timesteps_per_episode = n_timesteps, 
    stationary = False
)
agent_0 = Player(
    n_arms = n_arms, 
    strategy = strategy,
    update_type = 'constant',
    alpha = 0.1
)
agent_1 = Player(
    n_arms = n_arms, 
    strategy = strategy,
    update_type = 'average'
)
testbed = Testbed(
    n_runs = n_runs,
    environment = environment,
    agents = [(agent_0, 'constant'), (agent_1, 'average')]
)
if __name__ == '__main__':
    testbed.run_experiment()
#%%
testbed.results