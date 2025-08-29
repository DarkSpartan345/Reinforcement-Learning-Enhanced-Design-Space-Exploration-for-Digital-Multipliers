import torch
import gymnasium as gym
from Envs.env_base import BinaryMathEnv
import random

class PreprocessEnv(gym.Wrapper):
    def __init__(self, env):
        super(PreprocessEnv, self).__init__(env)

    def reset(self):
        obs = self.env.reset()[0]  # obs: [fase, cursor_pos, iteracion]
        obs = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)  # Shape: [1, 3]
        return obs

    def step(self, action):
        if isinstance(action, torch.Tensor):
            action = action.item()  # Convertir a int si viene de un tensor

        next_state, reward, done,truncate, info = self.env.step(action)

        next_state = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0)  # Shape: [1, 3]
        reward = torch.tensor([reward], dtype=torch.float32).view(1, -1)         # Shape: [1, 1]
        done = torch.tensor([done], dtype=torch.bool).view(1,-1)                            # Shape: [1]

        return next_state, reward, done,truncate, info
if __name__ == "__main__":
    env = PreprocessEnv(BinaryMathEnv(Proof=20, height=2, Bits=2))

    obs = env.reset()
    print(f"Estado inicial: {obs}, shape: {obs.shape}")

    for t in range(5):
        action = torch.tensor([random.randint(0, 5)])
        next_obs, reward, done,trucate, info = env.step(action)

        print(f"\nPaso {t+1}")
        print(f"Acción: {action.item()}")
        print(f"Obs siguiente: {next_obs}, shape: {next_obs.shape}")
        print(f"Recompensa: {reward.item()}, shape: {reward.shape}")
        print(f"Done: {done}, dtype: {done.dtype}")
        print(f"Info: {info}")

        if done.item():
            print("Episodio terminado.")
            break