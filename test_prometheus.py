from utils import beautify_json
from prometheus import PrometheusReader
from constants import TRAINING_EDGE_HOST_NAME


prometheus_reader = PrometheusReader(host=TRAINING_EDGE_HOST_NAME)
print(beautify_json(prometheus_reader.read_environment()))
