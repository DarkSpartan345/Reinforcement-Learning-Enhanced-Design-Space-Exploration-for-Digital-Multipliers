import numpy as np
from tqdm import tqdm
from gymnasium.vector import AsyncVectorEnv
from stable_baselines3.common.vec_env import SubprocVecEnv
import time
from Envs.Env_parallel_Processor import BinaryMathEnvParallel
class Parallel_Agents_vector():

    def __init__(self,action_values):
        self.action_values=action_values
        self.actions=6
        self.max_reward=-90    

    def policy_sarsa(self, states, epsilon=0., N_envs=1):
        random_values = np.random.random(N_envs)
        exploration_indices = random_values < epsilon
        target_indices = ~exploration_indices

        actions = np.empty(N_envs, dtype=int)

        # Asignar acciones de exploración
        actions[exploration_indices] = self.exploration_policy(np.sum(exploration_indices))

        # Asignar acciones de política objetivo
        actions[target_indices] = self.target_policy(states[target_indices])
        
        return actions

    def target_policy(self, states):
        # Obtener valores de acción para todos los estados a la vez
        action_values = self.action_values[states[:, 0], states[:, 1], states[:, 2]]
        
        # Seleccionar las mejores acciones de forma vectorizada
        max_actions = np.argmax(action_values, axis=1)
        
        # Devolver las mejores acciones por estado
        return max_actions

    def exploration_policy(self, N_envs):
        # Generar acciones aleatorias en un solo paso
        return np.random.randint(0, 6, size=N_envs)
  
    @staticmethod
    def epsilon_decay(initial_epsilon, min_epsilon, decay_rate, episode):
        return max(min_epsilon, initial_epsilon * np.exp(-decay_rate * episode))   
     
    def make_envs(self,env_id):
        def __init__():
            return BinaryMathEnvParallel(Proof=20, height=2, Bits=2,env_id=env_id)
        return __init__
      
    def n_step_sarsa(self, policy, episodes, epsilon_decay, alpha=0.1,
                     gamma=0.99, epsilon=0.2, n=6, N_ENVS=4):
        reward_episode = []
        envs = AsyncVectorEnv([self.make_envs(env_id=i) for i in range(N_ENVS)])
        for episode in tqdm(range(1, 10 + 1)):
            epsilon = epsilon if epsilon_decay is None else epsilon_decay(episode=episode)
            states = envs.reset()[0]
            actions = policy(states=states, epsilon=epsilon, N_envs=N_ENVS)
            transitions = []
            max_reward=envs.call("max_reward")
            done = np.zeros(N_ENVS, dtype=bool)
            truncated = np.zeros(N_ENVS, dtype=bool)
            t = 0
            episode_rewards = np.zeros(N_ENVS)
            while True:
                if not np.any(done) and not np.any(truncated):
                    next_states, rewards, dones, truncateds, _ = envs.step(actions)
                    next_actions = policy(next_states, epsilon=epsilon, N_envs=N_ENVS)
                    transitions.append([states, actions, rewards])
                    episode_rewards = rewards
                    if t >= n:
                                                # Inicializar G acumulado para todos los entornos
                        G = np.zeros(N_ENVS)

                        # Aplicar actualizaciones solo a los entornos no finalizados
                        not_done_indices = ~dones
                        G[not_done_indices] = self.action_values[
                            next_states[not_done_indices, 0],
                            next_states[not_done_indices, 1],
                            next_states[not_done_indices, 2],
                            next_actions[not_done_indices]
                        ]

                        # Obtener todas las recompensas, estados y acciones en las últimas transiciones (desde t-n)
                        rewards_rev = transitions[t-n:, 2]  # Recompensas de t-n a t
                        states_rev = transitions[t-n:, 0]   # Estados de t-n a t
                        actions_rev = transitions[t-n:, 1]  # Acciones de t-n a t

                        # Acumular los valores de G para todas las recompensas
                        # Invertir las recompensas para hacer el cálculo en el orden correcto
                        discount_factors = np.logspace(0, len(rewards_rev)-1, num=len(rewards_rev), base=gamma)
                        G = np.sum(rewards_rev * discount_factors[:, None], axis=0) + gamma**n * G

                        # Actualizar los valores de acción de forma vectorizada
                        # Índices para actualizar en self.action_values
                        indices_0 = states_rev[:, :, 0]
                        indices_1 = states_rev[:, :, 1]
                        indices_2 = states_rev[:, :, 2]

                        # Actualización del valor de acción (sin bucle)
                        self.action_values[indices_0, indices_1, indices_2, actions_rev] += alpha * (
                            G - self.action_values[indices_0, indices_1, indices_2, actions_rev]
                        )
                        t += 1
                    states = next_states
                    actions = next_actions
                    done = dones
                    truncated = truncateds
                else:
                    # Actualizar los valores
                    print(f"banderas2:{envs.call("flags")}")
                    if np.any(envs.call("flags")):
                        print(episode_rewards)
                        envs.call("new_max_reward", max_reward=np.max(episode_rewards))
                    print(envs.call("max_reward"))
                    print(envs.call("flags"))
                    break
            reward_episode.append(np.mean(episode_rewards))
            max_episode_reward = np.max(episode_rewards)
            index_max = np.argmax(episode_rewards)
            if max_episode_reward> self.max_reward:
                    self.max_reward = episode_rewards[index_max]
                    print(f"New max reward: {self.max_reward} in environment {index_max} at episode {episode}")
        return reward_episode








