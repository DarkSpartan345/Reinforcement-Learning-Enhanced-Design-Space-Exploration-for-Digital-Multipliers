import numpy as np
from Envs.Env_parallel_Processor import BinaryMathEnvParallel
import time
class Parallel_Agents_Procesors():

    def __init__(self,action_values):
        self.action_values=action_values
        self.actions=6
        self.max_reward=-90    

    def policy_sarsa(self,state, epsilon=0.):
        if np.random.random() < epsilon:
            return self.exploration_policy(state)
        else:
            return self.target_policy(state)
    def policy_softmax(self,state, tau=0.7,epsilon=0.):
        """
        Calcula la política softmax a partir de los Q-valores y selecciona una acción.

        Parámetros:
        - q_values: Lista o array con los valores Q del estado actual.
        - tau: Temperatura de la política softmax.

        Retorna:
        - action: Índice de la acción seleccionada.
        """
        q_values =self.action_values[state]
        q_values = q_values - np.max(q_values)  # Estabilización numérica
        exp_q = np.exp(q_values / tau)
        policy = exp_q / np.sum(exp_q)
        action = np.random.choice(len(q_values), p=policy)
        return action
        
    @staticmethod
    def epsilon_decay(initial_epsilon, min_epsilon, decay_rate, episode):
        return max(min_epsilon, initial_epsilon * np.exp(-decay_rate * episode))   
     

            
    def exploration_policy(self,state):
        return np.random.randint(6)

    def target_policy(self,state):
        av=self.action_values[state]
        return np.random.choice(np.flatnonzero(av==av.max()))
    def q_learning(self,policy,episodes,epsilon_decay, alpha=0.1, gamma=0.99,epsilon=0.2,env_id=0,height=2,bits=2,reward=-200):
        reward_episode = []
        env = BinaryMathEnvParallel(Proof=20, height=height, Bits=bits,env_id=env_id,maxi=reward)
        for episode in range(1, episodes + 1):
            state = env.reset()[0]
            done = False

            while not done:
                action = self.exploration_policy(state)
                next_state,reward,done,trucated,_=env.step(action)
                next_action = self.target_policy(next_state)

                qsa = self.action_values[state][action]
                next_qsa = self.action_values[next_state][next_action]
                self.action_values[state][action] = qsa + alpha * (reward + gamma * next_qsa - qsa)

                state = next_state
            reward_episode.append(reward)
        return reward_episode
    
    def sarsa(self, policy, episodes,epsilon_decay, alpha=0.1, gamma=0.99, epsilon=0.2,env_id=0,height=2,bits=2,reward=-200):
        reward_episode = []
        env = BinaryMathEnvParallel(Proof=20, height=height, Bits=bits,env_id=env_id,maxi=reward)
         # Entrenamiento
         # Iterar sobre los episodios
        for episode in range(1, episodes + 1):
            epsilon= epsilon if epsilon_decay == None else epsilon_decay(episode=episode)
            state = env.reset()[0]
            action = self.policy_sarsa(state, epsilon)
            done = False
            while not done:
                next_state,reward,done,trucated,_=env.step(action)
                next_action = self.policy_sarsa(next_state, epsilon)

                qsa = self.action_values[state][action]
                next_qsa = self.action_values[next_state][next_action]
                self.action_values[state][action] = qsa + alpha * (reward + gamma * next_qsa - qsa)
                state = next_state
                action = next_action  
            reward_episode.append(reward)
        return reward_episode
      
    def n_step_sarsa(self,policy, episodes,epsilon_decay, alpha=0.1,
                 gamma=0.99, epsilon=0.2, n=6,env_id=0,height=2,bits=2,reward=-200):
        reward_episode=[]
        env = BinaryMathEnvParallel(Proof=20, height=height, Bits=bits,env_id=env_id,maxi=reward)
        for episode in range(1, episodes + 1):
            epsilon= epsilon if epsilon_decay == None else epsilon_decay(episode=episode)
            state = env.reset()[0]
            action = policy(state=state,epsilon=epsilon)
            transitions = []
            done,trucated = False,False
            t = 0
            while t-n < len(transitions):
                if not done and not trucated:
                    next_state,reward,done,trucated,_=env.step(action)
                    next_action = policy(next_state,epsilon=epsilon)
                    transitions.append([state, action, reward])
                if t >= n:
                    G = (1 - done) * self.action_values[next_state][next_action]
                    for state_t, action_t, reward_t in reversed(transitions[t-n:]):
                        G = reward_t + gamma * G
                    self.action_values[state_t][action_t] += alpha * (G - self.action_values[state_t][action_t])

                t += 1
                state = next_state
                action = next_action
            reward_episode.append(reward)
        return reward_episode