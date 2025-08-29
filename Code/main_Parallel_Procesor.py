import numpy as np
import multiprocessing as mp
from functools import partial
from Agents.Agent_Parallel_Procesor import Parallel_Agents_Procesors
from Agents.Strategy.strategy import strategy
from tqdm import tqdm
from Utils.Store import Store
from datetime import datetime
import os
import argparse
import traceback

def worker(worker_id,best_reward,reward, global_q_table, episodes, epsilon_decay,dim_states,actions,height=2,bits=2,alpha=0.1,gamma=0.99,epsilon=0.2,stategy="cooperation_under_advantage_with_noise"):

    name_log = f"log_{datetime.now().strftime('%y-%m-%d_%H')}worker{worker_id}.log"
    logs = Store(name_log)
    local_q_table=np.random.rand(*dim_states, actions)
    local_agent = Parallel_Agents_Procesors(action_values=local_q_table)  # Cada worker inicia con la tabla global
    logs.log(f"SARSA con workers Dependientes con ruido con ventaja \n Reward {reward} Bits {bits} Height {height} \n Episodios: {episodes} \n epsilon {epsilon} \n alpha {alpha} \n gamma {gamma} \n worker_id {worker_id} \n")
    local_reward = float("-inf")
    try:
        for episode in tqdm(range(episodes)):
            if update_flags[worker_id]:  
                with lock:
                    Strategy = strategy(logs=logs,shape=local_agent.action_values.shape,stategy=stategy,global_q_table=global_q_table,worker_id=worker_id,episode=episode,best_reward=best_reward,local_reward=local_reward,q_table_agent=local_agent.action_values)
                    local_agent.action_values=Strategy.q_table_agent
                    update_flags[worker_id] = False
            total_reward = local_agent.n_step_sarsa(policy=local_agent.policy_sarsa,episodes=1,epsilon_decay=epsilon_decay, alpha=alpha, gamma=gamma,epsilon=epsilon,env_id=worker_id,height=2,bits=2,reward=reward)
            local_reward = total_reward[-1] if total_reward[-1]>local_reward else local_reward
            with lock:
                if total_reward[-1] > best_reward.value:
                    best_reward.value = total_reward[-1]
                    global_q_table[:] = local_agent.action_values.flatten()  # Copia la tabla local a la global
                    error_mean=(total_reward[-1]-100)/reward
                    update_flags[:] = [True] * len(update_flags)  # Activa todas las banderas
                    update_flags[worker_id] = False  # Excepto la del worker actual
                    print(f"Worker {worker_id} actualizó la Q-table con recompensa: {total_reward[-1]} con error medio:{error_mean}")
                    #logs.save_vars(local_agent.action_values,total_reward[-1],f"q_table_Parallel_Process_b_{Bits}h{height}.pkl")
                    logs.log(f" Episode {episode} actualizó la Q-table con recompensa: {total_reward[-1]} con error medio:{error_mean}")
    except Exception as e:
        print(f"Error en worker {worker_id}: {e}")
        logs.log(traceback.format_exc())
if __name__ == "__main__":
    
    # Crear el parser
    parser = argparse.ArgumentParser(description="Ejecutar script con parámetros modificables")
    parser.add_argument("--w", type=int, default=12, help="Cantidad de Workers (por defecto: 4)")
    parser.add_argument("--ep", type=int, default=100000, help="Número de episodios (por defecto: 1000)")
    parser.add_argument("--B", type=int, default=2, help="Bits (por defecto: 2)")
    parser.add_argument("--H", type=int, default=2, help="Height (por defecto: 2)")
    parser.add_argument("--s", type=str, required=True,
                        choices=["cooperation", "cooperation_with_noise", 
                                 "cooperation_under_advantage", "cooperation_under_advantage_with_noise"],
                        help="Estrategia a ejecutar")

    # Parsear argumentos
    args = parser.parse_args()
    num_workers = parser.parse_args().w
    name_log=[f"log_{datetime.now().strftime('%Y-%m-%d %H_%M')}w{w}_.log" for w in range(num_workers)]
    episodes_per_worker = parser.parse_args().ep
    stategy= parser.parse_args().s
    print(f"Ejecutando con {num_workers} workers y {episodes_per_worker} episodios por worker.")
    print(f"nombre de logs {name_log}")
    #logs=Store(name_log)
    #logs.log(f"Ejecutando con {num_workers} workers y {episodes_per_worker} episodios por worker.")
    # Definir dimensiones
    
    height, Bits = parser.parse_args().H, parser.parse_args().B
    #print(f"ejecutando a {Bits} bits y una altura de {height} ")
    #logs.log(f"ejecutando a {Bits} bits y una altura de {height} ")
    CC = 2 * height * Bits
    dim_states = (4, CC+1, CC+2)
    actions = 6  # Número de acciones
    q_table=f"q_table_Parallel_Process_b_{Bits}h{height}.pkl"
    #if os.path.exists(q_table):
         #action_values,reward_episode=logs.load_vars(q_table)
         #global_q_table = mp.Array('d', action_values.flatten())
    # else:
    # Variables compartidas
    global_q_table = mp.Array('d', np.random.rand(*dim_states, actions).flatten())
    best_reward = mp.Value('d', -float('inf'))
    update_flags = mp.Array('b', [False] * num_workers)  # Vector booleano de actualizaciones
    lock = mp.Lock()
    
    processes = []
    alpha=[0.05,0.1,0.2,0.35]
    gamma=[0.9,0.93,0.97,0.99]
    epsilon = [0.1, 0.2, 0.3, 0.4]
    reward=-100
    episodes=episodes_per_worker
    for worker_id in range(num_workers):
        if worker_id<4:
            alphaE= alpha[worker_id]
            p = mp.Process(target=worker, args=(worker_id,best_reward,reward, global_q_table, episodes, None,dim_states,actions,height,Bits,alphaE,0.99,0.2,stategy))
            processes.append(p)
        elif worker_id<8:
            gammaE= gamma[worker_id%4]
            p = mp.Process(target=worker, args=(worker_id,best_reward,reward, global_q_table, episodes, None,dim_states,actions,height,Bits,0.1,gammaE,0.2,stategy))
            processes.append(p)
        else:
            epsilonE = epsilon[worker_id % 4]
            p = mp.Process(target=worker, args=(worker_id,best_reward,reward, global_q_table, episodes, None,dim_states,actions,height,Bits,0.1,0.99,epsilonE,stategy))
            processes.append(p)
        p.start()
    # Iniciar los procesos
    for p in processes:
        p.join()
    print("Entrenamiento completado.")