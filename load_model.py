from cdn_env import CdnEnv
from constants import MODELS_DIR
from stable_baselines3 import PPO


env = CdnEnv()

model_path = f"{MODELS_DIR}/model.zip"

# Load the trained agent
model = PPO.load(model_path, env=env)

# Enjoy trained agent
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
