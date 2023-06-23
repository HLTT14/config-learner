import configparser

config = configparser.ConfigParser()
config.readfp(open(r'config.txt'))

PROMETHEUS_URL = config.get('Urls', 'prometheus_url')
TRAINING_EDGE_HOST_NAME = config.get('Urls', 'training_edge_host_name')
MULTIPLIER_AVERAGE_REQUEST_PROCESSING_TIME = int(config.get('Prometheus', 'multiplier_average_request_processing_time'))
TIME_INTERVAL_BETWEEN_STEPS = int(config.get('Parameters', 'time_interval_between_steps_in_seconds'))

MODELS_DIR = "models/PPO"
LOGS_DIR = "logs"
LOGS_PATH = "logs/logs.xlsx"
#CONFIG_FILE_PATH = "nginx-configs/nginx.conf"
CONFIG_FILE_PATH = "nginx-configs-azd-stream-16/nginx.conf"
CONFIG_KEYS = [
    'worker_processes',
    'worker_connections',
    'multi_accept',
    'proxy_cache_min_uses',
    'output_buffers/1',
    'output_buffers/2',
    'keepalive_timeout',
    'reset_timedout_connection',
    'send_timeout',
    'gzip',
    'gzip_comp_level',
    'open_file_cache/max',
    'open_file_cache/inactive',
    'open_file_cache_valid',
    'open_file_cache_min_uses',
]
