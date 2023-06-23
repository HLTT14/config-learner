import os
from cdn_env import CdnEnv
from stable_baselines3 import PPO
from constants import MODELS_DIR, LOGS_DIR
from datetime import datetime 
import traceback
import sys
import email_utils

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

model_path = f"{MODELS_DIR}/model.zip"

env = CdnEnv()

already_trained_model = os.path.isfile(model_path)

if already_trained_model:
    print(f'{datetime.now().replace(microsecond=0)}: model exists, loading it')
    # Load the trained agent
    model = PPO.load(model_path, env=env, verbose=1, tensorboard_log=LOGS_DIR)
else:
    print(f'{datetime.now().replace(microsecond=0)}: model does not exist, creating it')
    # Instantiate the agent
    model = PPO(policy="MultiInputPolicy", env=env, verbose=1, 
                batch_size=8, #64
                tensorboard_log=LOGS_DIR)

env.reset()

if not already_trained_model:
    ITERATIONS = 20
    # how frequently do you want to save the model
    TIMESTEPS = 10
    for i in range(ITERATIONS):
        try:
            print(f"{datetime.now().replace(microsecond=0)}: Training the new model in iteration {i}")
            # Train the agent
            model = model.learn(
                total_timesteps=TIMESTEPS,
                reset_num_timesteps=True,
                tb_log_name="PPO")
            print(f"{datetime.now().replace(microsecond=0)}: end of iteration {i}")
            # Save the agent
            model.save(model_path)
            print(f"{datetime.now().replace(microsecond=0)}: model saved on iteration {i}")
        except Exception as e:   
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            exception_message = ''.join('!! ' + line for line in lines)  # Log it or whatever here
            print(f"exception in train_model: {exception_message}")
            email_utils.email_exception(message=f'{str(datetime.date.today())} - {exception_message}')
            model.save(model_path)
            print(f"{datetime.now().replace(microsecond=0)}: model saved on iteration {i}")

while True:
    obs = env.reset()
    done = False
    while not done:
        try:
            action, _states = model.predict(obs)
            obs, reward, done, info = env.step(action)
            model.learn(total_timesteps=1)
            model.save(model_path)
        except Exception as e:   
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            exception_message = ''.join('!! ' + line for line in lines)  # Log it or whatever here
            print(f"exception in train_model: {exception_message}")
            email_utils.email_exception(message=f'{str(datetime.date.today())} - {exception_message}')
            model.save(model_path)
            print(f"{datetime.now().replace(microsecond=0)}: model saved")

