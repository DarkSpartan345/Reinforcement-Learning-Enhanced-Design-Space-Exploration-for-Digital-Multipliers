import gymnasium as gym
import numpy as np
import random
from datetime import datetime


class BinaryMathEnv(gym.Env):
    """
    Entorno de Gym personalizado para operaciones de matemáticas binarias.
    Versión pasiva sin interacción de teclado.
    """
    
    def __init__(self,Bits=8,Proof=4,height=8,maxi=100):
        super().__init__()  # Inicializar clase base
        # Configuración de entorno
        self.height=height
        self.Proof=Proof
        self.N=False
        self.Bits=Bits
        self.maxi=maxi
        self.it,self.CP=0,0
        # Definir espacios de estados y acciones
        self.CC=height*2*self.Bits
        self.reward=0
        self.suma_grid = [' '] * (self.CC)
        self.action_space = gym.spaces.Discrete(6)  # Izquierda, Derecha, Arriba, Abajo, Seleccionar/Modificar, Negado
        self.observation_space = gym.spaces.MultiDiscrete([4,self.CC, self.CC])  # Fase, posición del cursor, iteracion
        self.observation_space.n=(4,self.CC,self.CC)
        # Estados del juego
        self.min_error=0.9
        self.current_phase = 0
        self.cursor_position = 0
        self.selected_numbers = ['','']
        self.multiplication_results = []
        self.grid_size = (2*self.Bits)  # Tamaño de la cuadrícula
        
        
        # Configuraciones de selección
        self.display_grid = (
        [f"A[{i}]" for i in range(self.Bits - 1, -1, -1)] + ['1'],
        [f"B[{i}]" for i in range(self.Bits - 1, -1, -1)] + ['1'],
            self.suma_grid,
            ['Sí', 'No'],
        )
        # Nombres de fases
        self.max_pos=tuple([len(self.display_grid[current_phase]) - 1 for current_phase in range(4)])
        
        self.phase_names = (
            "Selección de Primer Número Binario",
            "Selección de Segundo Número Binario", 
            "Posicionar Resultado de Multiplicación",
            "Seguir Multiplicando",
        )
        self.pos_cursor_position=(-1,1,-self.grid_size,self.grid_size)
    def step(self, action,arch_multiplier="multiplier.v",arch_multipliermax="multipliermax.v",arch_multiplier_8bit_tb="multiplier_8bit_tb.v",arch_simv="simv"):
        """Ejecutar un paso en el entorno con el flujo de multiplicación deseado."""
        terminated =False
        self.N ^= (action == 5)
        truncated=self.CP>=800
        self.CP+=1
        
        # Acciones de movimiento en la fase de suma
        if self.current_phase == 2:  # Fase de colocar producto parcial

            if action <4 :
                self.cursor_position = max(0, min(self.CC - 1, self.cursor_position + self.pos_cursor_position[action]))
            
            elif action == 4:  # Seleccionar/Modificar
                
                # Verificar si hay un producto para colocar
                if len(self.multiplication_results) > 0:
                    
                    mult_result = self.multiplication_results[-1]
                    
                    # Verificar si el espacio está vacío antes de agregar
                    if self.suma_grid[self.cursor_position] == ' ':
                        self.suma_grid[self.cursor_position] = mult_result
                        
                        # Volver a la fase de preguntar si se sigue multiplicando
                        self.current_phase = 3
                        self.cursor_position = 0
                        self.reward=-1
        
        # Mantener la lógica de movimiento para otras fases
        else:
            if action < 2:  # Izquierda y derecha
                self.cursor_position = action*min(self.max_pos[self.current_phase], self.cursor_position + 1)+(1-action)*max(0, self.cursor_position - 1)
            elif action == 4:  # Seleccionar
                selected_value = self.display_grid[self.current_phase][self.cursor_position]
                if self.current_phase <2:  # Primer número
                    self.selected_numbers[self.current_phase]=selected_value if not self.N or selected_value=='1' else (f"~{selected_value}") 
                    if self.current_phase==1:
                        mult_result = f'(({self.selected_numbers[0]}) & ({self.selected_numbers[1]}))'
                        len_mul=len(set(self.multiplication_results))
                        self.multiplication_results.append(mult_result)
                        self.reward=-1
    
                elif self.current_phase == 3:  # Preguntar si se sigue multiplicando

                    self.current_phase = -1
                    self.cursor_position = 0
                    self.selected_numbers = ['','']
                    self.reward=-1
                    self.it+=1
                    terminated=self.closed(arch_multiplier=arch_multiplier,
                                           arch_multiplier_8bit_tb=arch_multiplier_8bit_tb,
                                           arch_simv=arch_simv,arch_multipliermax=arch_multipliermax) if selected_value == 'No' or self.it==len(self.suma_grid) else False
                        
                self.current_phase += 1
                self.cursor_position = 0
        self.reward= -1000 if truncated else self.reward
        return self._get_observation(), self.reward, terminated, truncated, {}

    def reset(self, seed=None, options=None):
        """Reiniciar el entorno a su estado inicial."""
        super().reset(seed=seed)
        self.current_phase,self.cursor_position = 0,0
        self.CC=(self.height*2*self.Bits)
        self.selected_numbers = ['','']
        self.multiplication_results = []
        self.suma_grid = [' '] * self.CC
        self.it,self.CP=0,0
        
        return self._get_observation(), {}
    def _get_observation(self):
        """Obtener el estado actual del entorno."""
        if self.current_phase<2:
            state=self.cursor_position if not self.N or self.cursor_position==2 else self.cursor_position+len(self.display_grid[self.current_phase])
        else:
            state=self.cursor_position 
        return tuple([self.current_phase, state,self.it])
    
    def closed(self,arch_multiplier="Verilog/multiplier.v",
               arch_multipliermax="Verilog/multipliermax.v",
               arch_multiplier_8bit_tb="Verilog/multiplier_8bit_tb.v",
               arch_simv="Verilog/simv"):
        terminated=True
        test_cases,results=self.generate_verilog(arch_multiplier=arch_multiplier,arch_multiplier_8bit_tb=arch_multiplier_8bit_tb,arch_simv=arch_simv)
        test_cases_results= test_cases[:, 0] * test_cases[:, 1]
        error = np.abs((results - test_cases_results) / test_cases_results)
        error_mean =np.mean(error)
        self.reward=self.maxi*error_mean+100
        if error_mean<self.min_error:
            with open(arch_multiplier, 'r') as f:
                content=f.read()
            with open(arch_multipliermax, 'w') as f:
                f.write(content)
        terminated=True
        return terminated
    def generate_verilog(self,seed=None,arch_multiplier="multiplier.v",arch_multiplier_8bit_tb="multiplier_8bit_tb.v",arch_simv="simv"):
        import subprocess
        dir_arch_simv=arch_simv
        dir_arch_multiplier=arch_multiplier
        dir_arch_multiplier_8bit_tb=arch_multiplier_8bit_tb
        suma_grid=np.array(self.suma_grid).reshape(self.height,2*self.Bits)
        multi=list(set([s for s in self.suma_grid if s.strip() != '']))
        suma={}
        code_mult = f"""
`timescale 1ns/1ps  
module multiplier (
input [{self.Bits-1}:0] A,
input [{self.Bits-1}:0] B,
output [{2*self.Bits-1}:0] P);\n
        // Generación de productos parciales\n"""
        # Generar las líneas de código de manera eficiente
        partial_products = [f" wire pp{j} = {i};" for j, i in enumerate(multi)]
        suma.update({i: f"pp{j}" for j, i in enumerate(multi)})  # Actualizar 'suma' en una sola línea
        # Unir las líneas generadas y agregarlas al código
        code_mult += "\n".join(partial_products) + "\n\n    // Suma de productos parciales\n"

        js = []
        columnas = []

        for j in range(2 * self.Bits):
            columna_actual = suma_grid[:, j]  # Evitar múltiples accesos
            if not np.all(columna_actual == ' '):  # Comprobación eficiente con NumPy
                idx = 2 * self.Bits - j
                js.append(idx)

                # Generar la asignación de columna sin concatenación ineficiente
                valores = [suma[i] for i in columna_actual if i != ' ']
                columnas.append(f"wire [{self.Bits-1}:0] columna{idx} = " + " + ".join(valores) + ";")

        # Construcción eficiente del código
        code_mult += "\n".join(columnas) + "\n"
        code_mult += "assign P = " + " + ".join([f"(columna{i} << {i-1})" for i in js]) + ";\n"
        code_mult += "endmodule"

        with open(arch_multiplier, 'w') as f:
            f.write(code_mult)

        if seed is not None:
            random.seed(seed)
        
        # Generar 4 casos de prueba totalmente aleatorios
        test_cases = np.random.randint(1, 2**self.Bits, size=(self.Proof, 2))
        
        # Contenido del testbench
        with open('Verilog/testbench_template.v', 'r') as file:
            content = file.read()
            content=content.replace("{regsI}",str(self.Bits-1))
            content=content.replace("{regsO}",str(2*self.Bits-1))
            text = "\n".join([
                f"""// Caso {i}: Prueba aleatoria {i}
                A = 8'd{test_cases[i, 0]};  // Acceso más eficiente con NumPy
                B = 8'd{test_cases[i, 1]};
                #10;
                $display("%d", P);
                //$display("A:%b,B:%b,res:%b",A,B P);\n"""
                for i in range(self.Proof)])
            content=content.replace("{Test}",text)

        with open(dir_arch_multiplier_8bit_tb, 'w') as f:
            f.write(content)    
    
        subprocess.run(["iverilog", "-o", dir_arch_simv, dir_arch_multiplier, dir_arch_multiplier_8bit_tb])        
        simulate=subprocess.run(["vvp", dir_arch_simv],capture_output=True)
        text=simulate.stdout.decode('utf-8')
        results = np.array([int(line.strip()) for line in text.split('\n') if line.strip().isdigit()]) #linux
        #results = np.array([int(line.strip()) for line in text.split('\r\n') if line.strip().isdigit()]) # windows
        return test_cases,results
