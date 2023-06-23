from constants import CONFIG_FILE_PATH, CONFIG_KEYS
from nginx_configurator import NginxConfigurator


nginx = NginxConfigurator(CONFIG_FILE_PATH)


def test_get_config_values(keys):
    print(nginx.get_config_values(keys))


def test_set_config_value():
    nginx.set_config_value('worker_processes', "1")
    nginx.set_config_value('open_file_cache/max', "5000")
    nginx.set_config_value('sendfile_max_chunk', "128k")
    nginx.set_config_value('output_buffers/2', "32k")


def test(i):
    return ({
        '1': lambda: test_set_config_value(),
        '2': lambda: test_get_config_values(CONFIG_KEYS),
    }.get(i, lambda: 'Invalid')())


menu = '''Choose one of these options:
1- Test set_config_value function.
2- Test get_config_values function.
'''

option = input(menu)
test(option)

