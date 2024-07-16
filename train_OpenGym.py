from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from tools_OpenGym import CustomGameEnv

env = make_vec_env(lambda: CustomGameEnv(), n_envs=1)

model = PPO("CnnPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

model.save("ppo_customgame")
