import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from Envs.environment import BinaryMathEnv
from Agents import Agents
import json
def graficar_estados_q_uniformes(Q_table, estados, acciones):
    """
    Muestra un gráfico con los estados representados como círculos divididos en porciones iguales,
    donde cada porción corresponde a una acción y se anota el valor Q.

    Args:
        Q_table (dict): La tabla Q donde las claves son los estados y los valores son arrays de valores Q para cada acción.
        estados (list): Lista de estados que se desea graficar.
        acciones (list): Lista de acciones posibles en el entorno.
    """
    num_estados = len(estados)
    columnas = 6  # Fijamos 6 gráficos por fila
    filas = int(np.ceil(num_estados / columnas))
    
    # Ajustar el tamaño de la figura para incluir 6 gráficos por fila
    fig, axes = plt.subplots(filas, columnas, figsize=(15, 3 * filas))
    axes = axes.flatten()  # Asegurar que podemos iterar sobre los ejes fácilmente
    
    for i, estado in enumerate(estados):
        ax = axes[i]
        valores_q = Q_table.get(estado, [0] * len(acciones))  # Valores Q o ceros si el estado no está en la tabla
        
        # Dividir el círculo en porciones iguales
        num_acciones = len(acciones)
        angulos = np.linspace(0, 2 * np.pi, num_acciones + 1)
        
        for j, (angulo_inicio, angulo_fin) in enumerate(zip(angulos[:-1], angulos[1:])):
            # Dibujar cada porción como un triángulo dentro del círculo
            x = [0, np.cos(angulo_inicio), np.cos(angulo_fin)]
            y = [0, np.sin(angulo_inicio), np.sin(angulo_fin)]
            ax.fill(x, y, color=sns.color_palette("pastel", num_acciones)[j], edgecolor='black')
            
            # Posicionar el texto dentro de la porción
            theta = (angulo_inicio + angulo_fin) / 2
            x_text = 0.6 * np.cos(theta)
            y_text = 0.6 * np.sin(theta)
            ax.text(x_text, y_text, f"{valores_q[j]:.2f}", ha='center', va='center', fontsize=8)
        
        ax.set_title(f"Estado {estado}", fontsize=9)
        ax.axis('equal')  # Asegura que el círculo sea perfecto
        ax.axis('off')  # Oculta los ejes para una mejor visualización
    
    # Eliminar ejes sobrantes si no hay suficientes estados
    for j in range(len(estados), len(axes)):
        fig.delaxes(axes[j])
    
    plt.tight_layout()
    plt.show()
def informes_json(i,it,dim_states,actions,episodes,nombre_archivo,var,Reward=100,alpha=0.1,
                 gamma=0.99, epsilon=0.2, n=6):
    print(i)
    max_reward=[]
    env=BinaryMathEnv(render_mode=None,Proof=20,height=2,Bits=2,maxi=Reward)
    reward_episode=[]
    action_values=np.zeros(shape=(dim_states[0],dim_states[1]+2,dim_states[2]+1,actions))
    Agent=Agents(action_values=action_values,env=env)
    reward_episode=Agent.n_step_sarsa(policy=Agent.policy_softmax_sarsa, episodes=episodes,alpha=alpha,
                                        gamma=gamma,epsilon=epsilon,n=n)
    max_reward.append({"iteracion":it,var:i[1],"max_reward":max(reward_episode)})
    print(max_reward)
    try:
        with open(nombre_archivo, "r") as archivo:
            datos_existentes = json.load(archivo)  # Cargar datos existentes
    except FileNotFoundError:
    # Si el archivo no existe, inicializa una lista vacía
        datos_existentes = []
    if isinstance(datos_existentes, list):
        datos_existentes.extend(max_reward)  # Agregar nuevos diccionarios a la lista
    else:
        print("El archivo JSON no contiene una lista. No se pueden agregar los datos.")
    with open(nombre_archivo, "w") as archivo:
        json.dump(datos_existentes, archivo, indent=4)
    print(f"Lista guardada en {nombre_archivo}")
    return max_reward
# # Ejemplo de uso
# Q_table = {
#     (0, 1): [1.0, 0.5, 0.8, 0.1, 0.0, -0.2],
#     (0, 2): [0.0, -0.1, 0.9, 0.3, 0.0, 0.2],
#     (0, 3): [0.2, 0.1, 0.4, 0.3, 0.0, 0.0],
#     (0, 4): [0.5, 0.6, 0.2, 0.8, 0.1, 0.4],
#     (0, 5): [0.3, 0.2, 0.7, 0.4, 0.5, 0.1],
#     (0, 6): [0.0, 0.1, 0.3, 0.6, 0.8, 0.4],
#     (0, 7): [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
#     (0, 8): [1.0, 0.5, 0.8, 0.1, 0.0, -0.2],
#     (0, 9): [1.0, 0.5, 0.8, 0.1, 0.0, -0.2],
#     (0, 10): [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
#     (0, 11): [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
#     (0, 12): [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
#     (0, 13): [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
# }
# estados = [(0,i) for i in range(13)]  # Lista de estados
# acciones = [0, 1, 2, 3, 4, 5]  # Lista de acciones

# graficar_estados_q_uniformes(Q_table, estados, acciones)
