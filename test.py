import gym
from cdn_env import CdnEnv

env = CdnEnv()

parameter_value = 4
space_upper_bound = env.observation_space['open_file_cache_min_uses'].n - 1

if parameter_value < space_upper_bound:
    new_value = parameter_value + 1
    is_valid = True
else:
    new_value = parameter_value
    is_valid = False

print(new_value, is_valid)