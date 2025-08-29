import gymnasium as gym
import numpy as np
import pygame
import random
from Envs.env_base import BinaryMathEnv


class BinaryMathEnvSecuencial(BinaryMathEnv):
    """
    Entorno de Gym personalizado para operaciones de matemáticas binarias.
    Versión pasiva sin interacción de teclado.
    """
    
    def __init__(self, render_mode=None,Bits=8,Proof=4,height=8,maxi=100):
        super().__init__(Bits=Bits,Proof=Proof,height=height,maxi=maxi)
        self.render_mode = render_mode
        self.window = None
        self.clock = None
        pygame.init()
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
        
        # Dimensiones de la pantalla
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        
        # Colores
        self.COLORS = {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'GRAY': (200, 200, 200),
            'BLUE': (100, 150, 255),
            'RED': (255, 100, 100),
            'GREEN': (100, 255, 100)    
        }

    def reset(self, seed=None, options=None):
        """Reiniciar el entorno a su estado inicial."""
        observation=super().reset(seed=seed)
        self.window=None
        # Renderizar si está en modo humano
        if self.render_mode == 'human':
            self._render_frame()
        return observation
    
    def render(self):
        """Método de renderizado para diferentes modos."""
        if self.render_mode is None:
            return
        
        if self.render_mode == 'human':
            self._render_frame()
        elif self.render_mode == 'rgb_array':
            return self._render_rgb_array()
    
    def _render_frame(self):
        """Renderizar frame para modo humano pasivo."""
        # Crear ventana si no existe
        if self.window is None:
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            pygame.display.set_caption('Entorno de Matemáticas Binarias')
        
        if self.clock is None:
            self.clock = pygame.time.Clock()
        
        # Limpiar pantalla
        self.window.fill(self.COLORS['WHITE'])
        # Título de la fase
        title = self.font_large.render(
            self.phase_names[self.current_phase], 
            True, self.COLORS['BLUE']
        )
        self.window.blit(title, (50, 50))
        
        # Renderizar según la fase
        if self.current_phase != 2:
            # Mostrar cuadrícula de selección
            for i, value in enumerate(self.display_grid[self.current_phase]):
                color = self.COLORS['RED'] if i == self.cursor_position else self.COLORS['GRAY']
                text = self.font_medium.render(value, True, color) if not self.N or self.current_phase>2 or value=='1' else self.font_medium.render("~"+value, True, color)
                self.window.blit(text, (300 + i * 50, 200))
        
        else:
            width = 40
            height = 30
            text_color = self.COLORS['GREEN']
            for row in range(self.height):
                for col in range(2*self.Bits):
                    # Calcular la posición (x, y) de cada cuadrado
                    index = (2*self.Bits) * row + col
                    x = (col * width) + 50
                    y = (row * height) + 100
                    
                    # Resaltar la casilla actual del cursor
                    if index == self.cursor_position:
                        border_color = self.COLORS['RED']
                        fill_color = pygame.Color(255, 100, 100, 50)  # Rojo semi-transparente
                    else:
                        border_color = self.COLORS['BLUE']
                        fill_color = None

                    
                    # Renderizar texto de la casilla
                    selected_text = self.font_small.render(
                        self.suma_grid[index], 
                        True, text_color
                    )
                    
                    # Dibujar el fondo si es necesario
                    if fill_color:
                        fill_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                        fill_surf.fill(fill_color)
                        self.window.blit(fill_surf, (x, y))
                    
                    # Dibujar el texto
                    self.window.blit(selected_text, (x, y+5))
                    
                    # Dibujar el borde
                    pygame.draw.rect(self.window, border_color, (x, y, width, height), 1)
            
            # Mostrar información adicional de la posición del cursor
            cursor_info = self.font_small.render(
                f"Posición del Cursor: Fila {self.cursor_position // (2*self.Bits)}, Columna {self.cursor_position % (2*self.Bits)}", 
                True, self.COLORS['BLACK']
            )
            self.window.blit(cursor_info, (50, 450))
        
        # Mostrar números seleccionados
        selected_text = self.font_small.render(
            f"Números: {self.selected_numbers}", 
            True, self.COLORS['GREEN']
        )
        self.window.blit(selected_text, (50, 500))
        
        # Mostrar resultados de multiplicación
        mult_text = self.font_small.render(
            f"Multiplicaciones: {self.multiplication_results}", 
            True, self.COLORS['GREEN']
        )
        self.window.blit(mult_text, (50, 550))
        
        # Actualizar pantalla
        pygame.display.flip()
        
        # Controlar la velocidad de fotogramas
        self.clock.tick(30)


 