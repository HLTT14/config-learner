from constants import CONFIG_FILE_PATH, CONFIG_KEYS
from nginx_configurator import NginxConfigurator
import random

# copied from cdn_env.py, UPDATE it if required
observation_set = {
    # configuration
    'worker_processes': list(range(1, 16+1)) + ['auto'],
    'worker_connections': [512, 1024, 2048, 4096, 8192],
    'multi_accept': ['off', 'on'],
    'proxy_cache_min_uses': list(range(1, 8+1)),
    'output_buffers/1': list(range(1, 4+1)),
    'output_buffers/2': ['4k', '8k', '16k', '32k', '64k', '128k'],
    'keepalive_timeout': [15, 30, 60, 75, 90],
    'reset_timedout_connection': ['off', 'on'],
    'send_timeout': ['15s', '20s', '30s', '45s', '60s', '75s'],
    'gzip': ['off', 'on'],
    'gzip_comp_level': list(range(1, 9+1)),
    'open_file_cache/max': list(range(2000, 20000, 2000)),
    'open_file_cache/inactive': ['30s', '1m', '90s', '2m', '210s', '5m', '450s', '10m'],
    'open_file_cache_valid': ['30s', '1m', '90s', '2m', '210s', '5m', '10m'],
    'open_file_cache_min_uses': list(range(1, 4+1)),
}

def create_random_config(nginx):
    for config in CONFIG_KEYS: 
        value = random.choice(observation_set[config])
        print(f"set {config}:{value}")
        nginx.set_config_value(config, value)
   
def main():
    nginx = NginxConfigurator(CONFIG_FILE_PATH)
    create_random_config(nginx)
    nginx._save_config()

if __name__ == '__main__':
    main()