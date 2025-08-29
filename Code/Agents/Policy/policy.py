import numpy as np
from collections import deque
class Policy():
    def __init__(self,action_values,actions,epsilon):
        self.actions=actions
        self.action_values=action_values
        self.epsilon=epsilon
        
        # Métodos para la política de exploración y objetivo

    def exploration_policy_action_probs(self, action_probs=None):
        """
        Política de exploración basada en Softmax o aleatoria.

        :param action_probs: Probabilidades de las acciones para la política Softmax.
        :return: Acción seleccionada.
        """
        
        if action_probs is not None:
            return np.random.choice(len(action_probs), p=action_probs)
        else:
            return np.random.randint(self.actions)

    def target_policy(self, state):
        """
        Política objetivo basada en la acción con el valor Q más alto.

        :param state: Estado actual.
        :return: Acción seleccionada por la política objetivo.
        """
        av = self.action_values[state]
        return np.random.choice(np.flatnonzero(av == av.max()))
    
    def exploration_policy_random(self):
         return np.random.randint(self.actions)
    
    def epsilon_greedy(self,state):
        if np.random.random() < self.epsilon:
            return self.exploration_policy_random()
        else:
            return self.target_policy(state)
    @staticmethod
    def epsilon_decay(initial_epsilon, min_epsilon, decay_rate, episode):
        return max(min_epsilon, initial_epsilon * np.exp(-decay_rate * episode))
    
    def policy_softmax_epsilon_greedy(self,state,epsilon):
        if np.random.random() < self.epsilon:
            return self.exploration_policy_random()
        else:
            av=self.action_values[state]
            soft=np.exp(av) / np.sum(np.exp(av), axis = 0)
            return np.random.choice(len(av),p=soft)
        
class PrioritizedReplayBuffer:
    def __init__(self, buffer_size=10000, alpha=0.6):
        self.buffer = deque(maxlen=buffer_size)  # Transiciones almacenadas
        self.priorities = deque(maxlen=buffer_size)  # Prioridades asociadas a las transiciones
        self.alpha = alpha  # Factor de priorización (0 = uniforme, 1 = completamente priorizado)
    
    def add(self, transition):
        # Agregar transición y asignarle la prioridad máxima inicial
        self.buffer.append(transition)
        max_priority = max(self.priorities) if self.priorities else 1.0
        self.priorities.append(max_priority)
    
    def sample(self, batch_size, beta=0.4):
        # Convertir prioridades en probabilidades
        priorities = np.array(self.priorities)
        probabilities = priorities ** self.alpha
        probabilities /= probabilities.sum()  # Normalizar

        # Muestrear transiciones basadas en probabilidades ponderadas
        indices = np.random.choice(len(self.buffer), batch_size, p=probabilities)
        transitions = [self.buffer[idx] for idx in indices]

        # Ponderar las muestras para corregir el sesgo (IS weights)
        total = len(self.buffer)
        weights = (total * probabilities[indices]) ** (-beta)
        weights /= weights.max()  # Normalizar

        return transitions, indices, weights
    
    def update_priorities(self, indices, td_errors):
        # Actualizar las prioridades de las transiciones seleccionadas
        for idx, td_error in zip(indices, td_errors):
            self.priorities[idx] = abs(td_error) + 1e-5  # Evitar prioridades de 0