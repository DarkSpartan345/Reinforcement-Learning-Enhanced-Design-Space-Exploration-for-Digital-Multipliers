# Reinforcement Learning Enhanced Design Space Exploration for Digital Multipliers

This repository contains the full codebase, configuration files, and supporting materials for the research project investigating how Reinforcement Learning (RL) can improve Design Space Exploration (DSE) in the context of digital multiplier architectures.

## Project Overview

Digital multipliers are essential components in a wide variety of hardware systems. Optimizing their design requires exploring a vast space of architectural alternatives. This project employs RL agents to intelligently navigate that space, aiming to identify efficient architectures that outperform traditional multipliers in terms of design metrics.

## Repository Structure

```
.
├── Agents
│   ├── Agent_Parallel_Procesor.py        # RL agent implementation with parallel processing
│   └── Strategy/                         # Strategy patterns for agent decision-making
├── Envs
│   ├── env_base.py                       # Base environment class
│   ├── environment.py                    # Environment setup for RL training
│   ├── Env_parallel_Processor.py         # Parallelized environment implementation
├── Logs
│   └── <date>/                           # Training logs with per-worker outputs
├── Utils
│   ├── Stats.py                          # Utility functions for statistics
│   └── Store.py                          # Data storage and management helpers
├── Verilog
│   ├── multiplier_*.v                    # Verilog multiplier designs generated during exploration
│   ├── testbench_template.v              # Testbench template for simulations
├── main_Parallel_Procesor.py             # Main script to launch RL training
├── Requirements.txt                      # Python dependencies
└── multiplier_8bit_tb.vcd                # Example simulation output
```

## Getting Started

### Prerequisites

* Python 3.10+
* Verilog simulator (Icarus Verilog)
* Virtual environment (recommended)

### Installation Project

```bash
# Clone the repository
git clone https://github.com/DarkSpartan345/Reinforcement-Learning-Enhanced-Design-Space-Exploration-for-Digital-Multipliers.git
cd Reinforcement-Learning-Enhanced-Design-Space-Exploration-for-Digital-Multipliers

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r Requirements.txt
```
## Installing Icarus Verilog

This project requires **Icarus Verilog** to simulate the multiplier designs.  
Follow the steps below depending on your operating system:

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install iverilog gtkwave 
```


### Running the Project

To start RL-based exploration with parallel agents:

```bash
cd Code
python main_Parallel_Procesor.py --w 4 --ep 1000 --s cooperation --a SARSA
```

Logs will be saved in the Logs/ directory, and generated Verilog files will appear under Verilog/.

For more details on execution options and how to adjust parameters, please refer to the Code/README.md, which provides a guide to available arguments and configuration choices.

## Results

* RL agents progressively optimize multiplier architectures.
* Logs provide insight into training performance.
* Generated Verilog files can be simulated and compared against baseline multipliers.

## License

This project is licensed under the MIT License.
