import numpy as np
from tqdm import tqdm
from Agents.Policy.policy import Policy
from Agents.Policy.policy import PrioritizedReplayBuffer
from Utils.Store import Store


class Agents():

    def __init__(self,action_values,env):
        self.action_values=action_values
        self.env=env
        self.actions=6
        self.max_reward=-90

    def n_step_sarsa(self,policy, episodes,epsilon_decay, alpha=0.1,
                 gamma=0.99, epsilon=0.2, n=6):
        reward_episode=[]
        for episode in tqdm(range(1,episodes+1)):
            epsilon= epsilon if epsilon_decay == None else epsilon_decay(episode=episode)
            state = self.env.reset()[0]
            action = policy(state=state)
            transitions = []
            done,trucated = False,False
            t = 0

            while t-n < len(transitions):
                
                if not done and not trucated:
                    next_state,reward,done,trucated,_=self.env.step(action)
                    next_action = policy(next_state)
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
            if episode % 100 == 0:
                Store.save_vars(action_values=self.action_values,reward_episode=reward_episode,filepath_vars="Vars.pkl")
        return reward_episode
    
# agente Q_learning con politicas

    def soft_sarsa_n_steps(self, n=5, gamma=0.99, alpha=0.1, tau=15, episodes=1000):
        reward_episode = []

        for episode in tqdm(range(1, episodes + 1)):
            state = self.env.reset()[0]
            done = False
            truncated=False
            reward_e = 0

            # Inicializar la lista de transiciones para n-steps
            state_action_rewards = []
            rewards = []
            actions = []
            
            # Tomar la primera acción según la política de exploración (Softmax)
            exp_Q = np.exp(self.action_values[tuple(state)] / tau)
            action_probs = exp_Q / np.sum(exp_Q)
            action = Policy.exploration_policy_action_probs(action_probs)

            while  not done and not truncated:
                state_action_rewards.append((state, action))  # Guardar la transición actual
                rewards.append(0)  # Inicializar recompensa (se actualizará con los pasos)
                actions.append(action)

                # Tomar acción en el entorno
                new_state, reward, done, truncated, _ = self.env.step(action)

                # Guardar la recompensa
                rewards[-1] = reward
                
                # Seleccionar nueva acción usando la política objetivo (Softmax)
                exp_Q_new = np.exp(self.action_values[tuple(new_state)] / tau)
                action_probs_new = exp_Q_new / np.sum(exp_Q_new)
                new_action = Policy.exploration_policy_action_probs(action_probs_new)

                # Actualizar el estado y la acción
                state = new_state
                action = new_action

                # Si se han acumulado suficientes pasos n
                if len(state_action_rewards) >= n:
                    # Calcular el retorno para la secuencia de transiciones
                    G = 0
                    for i in range(n):
                        G = gamma * G + rewards[-(i + 1)]

                    # Tomar el primer par estado-acción
                    state_n, action_n = state_action_rewards[0]
                    # Realizar la actualización de Q(s, a) para el primer paso en la secuencia
                    qsa = self.action_values[state_n] [action_n]
                    self.action_values[state_n] [action_n] = qsa + alpha * (G - qsa)

                    # Eliminar el primer paso de la secuencia
                    state_action_rewards.pop(0)
                    rewards.pop(0)
                    actions.pop(0)

            reward_episode.append(reward_e)

        return reward_episode
    def QlearningExperienceReplay(self,policy, alpha=0.1,episodes=100000,
                 gamma=0.99, epsilon=0.2, alpha_priority=0.6,beta=0.4, buffer_size=500, batch_size=16):
        reward_episode = []
        replay_buffer = PrioritizedReplayBuffer(buffer_size, alpha_priority)
        for episode in tqdm(range(1, episodes + 1)):
            state = self.env.reset()[0]
            done = False
            truncated=False
            total_reward=0
            while not done and not truncated:
                # Seleccionar acción y ejecutar en el entorno
                
                action = policy(state)
                next_state, reward, done,truncated, _ = self.env.step(action)

                # Almacenar la transición en el buffer
                replay_buffer.add((state, action, reward, next_state, done))

                # Actualizar Q-values usando Prioritized Experience Replay
                self.update_q_values(replay_buffer=replay_buffer,batch_size=batch_size,gamma=gamma,alpha=alpha)

                state = next_state
                total_reward += reward  # Acumular recompensa

            reward_episode.append(reward)

        return reward_episode
    def update_q_values(self,replay_buffer,batch_size=64,gamma=0.99,alpha=0.1):
        # Asegurarse de que haya suficientes transiciones en el buffer para un minibatch
        if len(replay_buffer.buffer) < batch_size:
            return

        # Muestrear un minibatch del buffer priorizado
        transitions, indices, weights = replay_buffer.sample(batch_size)

        td_errors = []
        states = tuple([t[0] for t in transitions])
        actions = np.array([t[1] for t in transitions])
        rewards = np.array([t[2] for t in transitions])
        next_states = tuple([t[3] for t in transitions])
        dones = np.array([t[4] for t in transitions])

        # Obtener las mejores acciones para los estados siguientes (next_states)
        best_next_actions = [np.argmax(self.action_values[next_states[i]])for i in  range(batch_size)]

        # Calcular los targets de manera vectorizada
        targets = rewards + gamma * np.array([self.action_values[next_states[i]] [best_next_actions[i]]for i in  range(batch_size)]) * (1 - dones)

        # Calcular los TD errors
        action_state=np.array([self.action_values[states[i]][actions[i]] for i in range(batch_size)])
        td_errors = targets - action_state

        # Actualizar la tabla Q con los pesos IS de manera vectorizada
        action_state += alpha * td_errors * weights

        # Actualizar las prioridades
        replay_buffer.update_priorities(indices, np.abs(td_errors) + 1e-5)
        
        # Actualizar las prioridades en el buffer
        replay_buffer.update_priorities(indices, td_errors)


    

        

        