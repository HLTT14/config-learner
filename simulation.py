import os
import random
from cdn_env import CdnEnv
from random import randrange
from datetime import datetime
from utils import beautify_json
from stable_baselines3 import PPO
from constants import MODELS_DIR, LOGS_DIR


class PrometheusReaderSimulator:
    @staticmethod
    def read_environment():
        return {
            #"total_ram_memory": 2,
            #"total_disk": 36,
            #"cpu_cores": 2,
            "system_load": randrange(0, 10),
            "cpu_usage": randrange(0, 10),
            "cpu_iowait": randrange(0, 10),
            "ram_memory_usage": randrange(0, 10),
            #"disk_usage": randrange(0, 10),
            "disk_io_usage": randrange(0, 10),
            #"disk_iops_reads": randrange(0, 100),
            "disk_read_usage": randrange(0, 10),
            #"disk_iops_writes": randrange(0, 100),
            "disk_write_usage": randrange(0, 10),
            "disk_reads_mbps": randrange(0, 10),
            "disk_writes_mbps": randrange(0, 10),
            "number_of_requests_per_second": randrange(0, 10),
            "average_response_size_mb": randrange(0, 100),
            "average_request_processing_time_in_seconds": randrange(0, 100),
            "nginx_cache_hit_ratio": randrange(0, 10),
            "nginx_writing_connections": randrange(0, 10),
            "average_network_transmit_mbps": randrange(0, 10),
            "number_of_5xx_errors_per_second": randrange(0, 10),
        }


class NginxConfiguratorSimulator:
    def set_config_value(self, key, value):
        pass

    @staticmethod
    def get_config_values(keys):
        return {
            'worker_processes': random.choice(list(range(1, 16+1)) + ['auto']),
            'worker_connections': random.choice([512, 1024, 2048, 4096, 8192]),
            'multi_accept': random.choice(['off', 'on']),
            'proxy_cache_min_uses': random.choice(list(range(1, 8+1))),
            'output_buffers/1': random.choice(list(range(1, 4+1))),
            'output_buffers/2': random.choice(['4k', '8k', '16k', '32k', '64k', '128k']),
            'keepalive_timeout': random.choice([15, 30, 60, 75, 90]),
            'reset_timedout_connection': random.choice(['off', 'on']),
            'send_timeout': random.choice(['15s', '30s', '45s', '60s', '75s']),
            'gzip': random.choice(['off', 'on']),
            'gzip_comp_level': random.choice(list(range(1, 9+1))),
            'open_file_cache/max': random.choice(list(range(2000, 20000, 2000))),
            'open_file_cache/inactive': random.choice(['30s', '1m', '90s', '2m', '210s', '5m', '450s', '10m']),
            'open_file_cache_valid': random.choice(['30s', '1m', '90s', '2m', '210s', '5m']),
            'open_file_cache_min_uses': random.choice(list(range(1, 4+1))),
        }


class CdnEnvSimulator(CdnEnv):
    def __init__(self):
        super(CdnEnvSimulator, self).__init__()
        self.time_interval_between_steps = 0
        self.prometheus_reader = PrometheusReaderSimulator()
        self.nginx_configurator = NginxConfiguratorSimulator()

    @staticmethod
    def send_configs_to_remote_server():
        pass

    def _log(self):
        with open(f"./{LOGS_DIR}/logs.txt", 'a', encoding='utf-8') as file:
            file.write(f"step#: {self.step_counter}\n")
            file.write(f"time: {datetime.now().replace(microsecond=0)}\n")
            file.write(f"action: {self.action}\n")
            file.write(f"reward: {self.reward}\n")
            file.write(f"server state goodness: {self.server_state_goodness}\n")
            mapped_observation = self._map_observation(self.observation)
            file.write(f"mapped observation: {beautify_json(mapped_observation)}\n")
            file.write('*' * 100 + "\n")


if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

env = CdnEnvSimulator()
env.reset()

model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log=LOGS_DIR)

TIMESTEPS = 10000

for i in range(1, 30):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{MODELS_DIR}/{TIMESTEPS * i}")
