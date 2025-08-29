import numpy as np
class strategy:
    
    def __init__(self,logs,shape,stategy,global_q_table=None,worker_id=None,episode=None,best_reward=None,local_reward=None,q_table_agent=None):
        
        self.logs=logs
        self.shape=shape
        self.Strategy=stategy
        if stategy=="cooperation":
            self.q_table_agent=self.Cooperation(global_q_table,worker_id,episode)
        elif stategy=="cooperation_with_noise":
            self.q_table_agent=self.Cooperation_with_noise(global_q_table,worker_id,episode)
        elif stategy=="cooperation_under_advantage":
            self.q_table_agent=self.Cooperation_under_advantage(best_reward,local_reward,global_q_table,worker_id,episode,q_table_agent)
        elif stategy=="cooperation_under_advantage_with_noise":
            self.q_table_agent=self.Cooperation_under_advantage_with_noise(best_reward,local_reward,global_q_table,worker_id,episode,q_table_agent)
        else:
            print("estrategia no valida")
            raise ValueError("Estrategia no válida")
    def Cooperation(self,global_q_table,worker_id,episode):
        q_table_agent= np.copy(global_q_table).reshape(self.shape)
        self.logs.log(f"Worker {worker_id} copió la Q-table global en episodio {episode}.")
        return q_table_agent
    def Cooperation_with_noise(self,global_q_table,worker_id,episode):
        q_table_agent=self.Cooperation(global_q_table,worker_id,episode)
        q_table_agent = q_table_agent*np.random.normal(loc=0.5, scale=0.5, size=self.shape)
        return q_table_agent
    def Cooperation_under_advantage(self,best_reward,local_reward,global_q_table,worker_id,episode,q_table_agent):
        adv = best_reward - local_reward
        sigmo= 1/(1+np.exp(-adv+6))
        self.deci=np.random.choice([False,True], p=[1-sigmo, sigmo])
        q_table_agent= self.Cooperation(global_q_table,worker_id,episode) if self.deci else q_table_agent
        if not self.deci:
            self.logs.log(f"worker {worker_id} NO copió la Q-table global en episodio {episode}.")
        return q_table_agent
    def Cooperation_under_advantage_with_noise(self,best_reward,local_reward,global_q_table,worker_id,episode,q_table_agent):
        self.Cooperation_under_advantage(best_reward,local_reward,global_q_table,worker_id,episode,q_table_agent)
        q_table_agent = q_table_agent*np.random.normal(loc=0.5, scale=0.5, size=self.shape) if self.deci else q_table_agent
        return q_table_agent