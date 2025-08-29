from Envs.env_base import BinaryMathEnv
import numpy as np
from datetime import datetime
import os
class BinaryMathEnvParallel(BinaryMathEnv):

    def __init__(self,maxi,Proof=20, height=2, Bits=2,env_id=0):
        super().__init__(Proof=Proof, height=height, Bits=Bits,maxi=maxi)
        self.env_id = env_id
        self.arch_multiplier=f"Verilog/multiplier_env_{self.env_id}_2.v"
        self.arch_multipliermax=f"Verilog/multipliermax_env_{self.env_id}_2.v"
        self.arch_multiplier_8bit_tb=f"Verilog/multiplier_8bit_tb_env_{self.env_id}_2.v"
        self.arch_simv=f"Verilog/simv_env_{self.env_id}"
    def step(self, action):
        return super().step(action,arch_multiplier=self.arch_multiplier,
                            arch_multipliermax=self.arch_multipliermax,
                            arch_multiplier_8bit_tb=self.arch_multiplier_8bit_tb,
                            arch_simv=self.arch_simv)
    def max_reward(self):
        return self.max_reward_data
    def flags(self):
        return self.flag
    def new_max_reward(self,max_reward):
        self.max_reward_data=max_reward
        self.flag=False
    def closed(self,arch_multiplier="Verilog/multiplier.v",
               arch_multipliermax="Verilog/multipliermax.v",
               arch_multiplier_8bit_tb="Verilog/multiplier_8bit_tb.v",
               arch_simv="Verilog/simv"):
        terminated=True
        test_cases,results=super().generate_verilog(arch_multiplier=self.arch_multiplier,
                                                 arch_multiplier_8bit_tb=self.arch_multiplier_8bit_tb,
                                                 arch_simv=self.arch_simv)
        test_cases_results= test_cases[:, 0] * test_cases[:, 1]
        error = np.abs((results - test_cases_results) / test_cases_results)
        error_mean = np.mean(error)
        self.reward=self.maxi*error_mean+100
        if error_mean<self.min_error:
            with open(self.arch_multiplier, 'r') as f:
                content=f.read()
            with open(self.arch_multipliermax, 'w') as f:
                f.write(content)
            self.min_error=error_mean
        if error_mean<0.1:
            name_multiplier=f"max_e_{error_mean:.2f}_{datetime.now().strftime('%D_%H_%m')}.v"
            arch_multiplier=f"Verilog/{name_multiplier}"
            os.makedirs(os.path.dirname(arch_multiplier), exist_ok=True)
            with open(self.arch_multiplier, 'r') as f:
                content=f.read()
            with open(arch_multiplier, 'w') as f:
                f.write(content)
        return terminated

    #def OpenLane(name_multiplier="multiplier",arch_multiplier="Verilog/Max2bits/max_e_0.03_07_05_04.v"):
     #   import subprocess
        # Ejecutar la regla 'say_hello' del Makefile
      #  subprocess.run(["make", "OPENLANE",f"DESIGN={name_multiplier}",f"VERILOG_FILES={arch_multiplier}"])