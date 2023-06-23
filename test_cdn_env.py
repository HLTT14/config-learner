from cdn_env import CdnEnv
from utils import beautify_json
from stable_baselines3.common.env_checker import check_env
from perform_action import suggest_change


env = CdnEnv()
env.reset()


def simulate_training():
    while True:
        random_action = env.action_space.sample()
        observation, reward, _, _ = env.step(random_action)
        env.render()


def test_get_observation():
    print(beautify_json(env._get_observation()))


def test_suggest_change():
    print(suggest_change('worker_processes__increase', env.observation_space, env.observation))
    print(suggest_change('worker_processes__decrease', env.observation_space, env.observation))
    print(suggest_change('send_timeout__increase', env.observation_space, env.observation))
    print(suggest_change('send_timeout__decrease', env.observation_space, env.observation))


def test(i):
    return ({
        '1': lambda: check_env(env),
        '2': lambda: test_get_observation(),
        '3': lambda: test_suggest_change(),
        '4': lambda: simulate_training(),
    }.get(i, lambda: 'Invalid')())


menu = '''Choose one of these options:
1- Check Env
2- Test _get_observation function.
3- Test suggest_change function.
4- Simulate Training
'''

option = input(menu)
test(option)
