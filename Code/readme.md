# Proyecto de Aprendizaje por Refuerzo Paralelo (SARSA)

Este proyecto implementa un sistema de **aprendizaje por refuerzo** (SARSA y SARSA N-steps) en un entorno paralelo con múltiples workers.  
El código permite entrenar agentes en paralelo compartiendo una **Q-table global**, evaluando estrategias de cooperación y variaciones con ruido.  

---

## 📂 Estructura del proyecto

```
.
├── Agents/                 # Agentes de RL
│   ├── Agent_Parallel_Procesor.py
│   └── Strategy/strategy.py
├── Envs/                   # Entornos personalizados
│   ├── env_base.py
│   ├── environment.py
│   └── Env_parallel_Processor.py
├── Utils/                  # Utilidades y manejo de logs
│   ├── Stats.py
│   └── Store.py
├── Logs/                   # Carpeta donde se guardan los logs
├── Verilog/                # Archivos de prueba en Verilog
├── main_Parallel_Procesor.py   # Script principal
├── Requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```

---

## ⚙️ Requisitos previos

- Python **3.10+**
- Git
- Opcional: compilador de Verilog si deseas ejecutar los testbenchs en `/Verilog`

---


2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```

3. Activa el entorno:

   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate
     ```

4. Instala dependencias:
   ```bash
   pip install -r Requirements.txt
   ```

---

## ▶️ Uso

El script principal es **`main_Parallel_Procesor.py`**.  

Para ver todas las opciones disponibles:
```bash
python main_Parallel_Procesor.py -h
```

Ejemplo de ejecución:
```bash
python main_Parallel_Procesor.py --w 4 --ep 1000 --s cooperation --a SARSA
```

Parámetros disponibles:
- `--w`: cantidad de workers (default: 12)  
- `--ep`: número de episodios por worker (default: 100000)  
- `--B`: bits usados (default: 2)  
- `--H`: altura de la representación (default: 2)  
- `--s`: estrategia a ejecutar (`independent`, `cooperation`, `cooperation_with_noise`, `cooperation_under_advantage`, `cooperation_under_advantage_with_noise`)  
- `--a`: algoritmo a ejecutar (`SARSA`, `SARSA_N_STEPS`)  

---

## 📊 Logs

Los resultados del entrenamiento se almacenan en la carpeta **`Logs/`** con un nombre que incluye la fecha y hora.  
Ejemplo:
```
Logs/2025-09-02/log_25-09-02_19worker0.log
```

---

## 📜 Licencia

Este proyecto está bajo la licencia MIT (puedes modificarla si lo prefieres).