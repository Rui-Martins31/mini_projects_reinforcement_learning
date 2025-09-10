import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import os

# Create our training environment
env: gym.Env = gym.make("FrozenLake-v1", render_mode="none", map_name="4x4", is_slippery=True)

# Reset environment to start a new episode
observation, info = env.reset()
# observation: what the agent can "see" - Tile position
# info: extra debugging information (usually not needed for basic learning)

print(f"Starting observation: {observation}")
print(f"Starting information: {info}")

# Loop control and debug
episode_over: bool          = False
done: bool                  = False
is_training: bool           = True
MAX_TRIES_CYCLES: int       = 1
MAX_EPISODES_CYCLES: int    = 100000
list_rewards: list[int]     = []

# Explore or exploit
prob_explore: float         = 1.0
prob_explore_decay: float   = 1 / MAX_EPISODES_CYCLES
prob_explore_min: float     = min(prob_explore, 0.1)

# Map
MAP_NUM_OBSERVATIONS: int   = env.observation_space.n
MAP_NUM_ACTIONS: int        = env.action_space.n
env_map:np.ndarray          = np.zeros((MAP_NUM_OBSERVATIONS, MAP_NUM_ACTIONS), dtype=np.float64)

# Bellman equation vars
# Q(s,a)←Q(s,a)+α[r+γ*max​Q(s′,a′)−Q(s,a)]
alpha: float                = 0.9  # learning rate
alpha_decay: float          = 0.999
alpha_min: float            = 0.001
gamma: float                = 0.9  # discount factor

# Save data
best_q_map: np.ndarray      = None
best_reward: int            = 0


for _ in range(0, MAX_TRIES_CYCLES):
    episode_over: bool       = False
    max_episodes_cycles: int = MAX_EPISODES_CYCLES

    while not episode_over:
        # Reset
        done: bool           = False
        observation, _       = env.reset()
        prob_explore         = max(prob_explore - prob_explore_decay, prob_explore_min)
        alpha                = alpha if prob_explore != prob_explore_min else alpha_min # max(alpha * alpha_decay, alpha_min)
        total_episode_reward = 0
        print(f"Cycles left: {max_episodes_cycles}, {prob_explore = }, lr: {alpha}")

        while not done:
            # Choose an action: [0, 1, 2, 3]
            # Randomly or based on previous tries
            if np.random.random() < prob_explore and is_training:
                action  = env.action_space.sample()
            else: 
                # max_ind = np.argmax(env_map[observation])
                max_ind = np.random.choice(np.where(env_map[observation] == env_map[observation].max())[0]) # Select a random max value index in case there's a tie
                action  = max_ind

            # Take action
            next_observation, reward, terminated, truncated, info = env.step(action)

            # reward: +1 everytime the character reaches the gift
            # terminated: True if hits a hole (agent failed)
            # truncated: True if we hit the time limit (500 steps)

            # End episode
            done = terminated or truncated

            # Update
            # if terminated and reward == 0:
            #     reward = -1
            
            if not done:
                brackets = reward + gamma * np.max(env_map[next_observation, :]) - env_map[observation][action]
                env_map[observation][action] += alpha * brackets
            else:
                # When it's done there is no future
                brackets = reward
                env_map[observation][action] += alpha * brackets
                env_map[next_observation] = [ reward for _ in range(MAP_NUM_ACTIONS) ]

            observation = next_observation
            total_episode_reward += reward

        if max_episodes_cycles > 0:
            max_episodes_cycles -= 1
        else:
            episode_over = True

        list_rewards.append(total_episode_reward)
        if total_episode_reward > best_reward:
            best_reward = total_episode_reward
            best_q_map  = env_map

print(f"Episode finished!")
print(f"Map of list_rewards: {best_q_map}")

# Evaluation phase
total_reward = 0
num_test_episodes = 100
for _ in range(num_test_episodes):
    observation, _ = env.reset()
    done = False
    while not done:
        action = np.argmax(best_q_map[observation])  # Greedy policy
        next_observation, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        if terminated and reward == 0:
            reward = -1
        total_reward += reward
        observation = next_observation
avg_reward = total_reward / num_test_episodes
print(f"Average reward over {num_test_episodes} episodes: {avg_reward}")

# Plot learning curve
plt.plot(list_rewards)
plt.xlabel("Episode")
plt.ylabel("Episode Reward")
plt.title("Training Reward per Episode")
plt.show()

env.close()

# Save the q_map
DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_PATH      = DIRECTORY_PATH + '/q_map'
np.save(file=FILE_PATH, arr=best_q_map)