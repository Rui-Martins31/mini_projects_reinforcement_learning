import numpy as np
import gymnasium as gym
import os

DIRECTORY_PATH: str  = os.path.dirname(os.path.abspath(__file__))
FILE_PATH: str       = DIRECTORY_PATH + '/q_map.npy'
q_map                = np.load(file=FILE_PATH)
env: gym.Env         = gym.make("FrozenLake-v1", render_mode="human", is_slippery=False)

## DEBUG 
print(f"{q_map = }")

# Evaluation phase
total_reward: int      = 0
num_test_episodes: int = 100
for _ in range(num_test_episodes):
    observation, _ = env.reset()
    done = False
    while not done:
        action = np.argmax(q_map[observation])  # Greedy policy
        next_observation, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        if terminated and reward == 0:
            reward = -1
        total_reward += reward
        observation = next_observation
avg_reward = total_reward / num_test_episodes
print(f"Average reward over {num_test_episodes} episodes: {avg_reward}")