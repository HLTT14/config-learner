# https://github.com/4n4nd/prometheus-api-client-python
# https://prometheus.io/docs/prometheus/latest/querying/examples/
# https://timber.io/blog/promql-for-humans/
# https://docs.signalfx.com/en/latest/integrations/agent/monitors/prometheus-node.html
# https://brian-candler.medium.com/interpreting-prometheus-metrics-for-linux-disk-i-o-utilization-4db53dfedcfc
# https://www.robustperception.io/common-query-patterns-in-promql
# https://www.robustperception.io/how-does-a-prometheus-histogram-work
# https://povilasv.me/prometheus-tracking-request-duration/
# https://gist.github.com/freeseacher/5cfacba691e786d7837dc9d97702b465
# https://github.com/vozlt/nginx-module-vts/blob/master/src/ngx_http_vhost_traffic_status_display_prometheus.h
# https://www.robustperception.io/how-does-a-prometheus-histogram-work
# https://www.martin-helmich.de/en/blog/monitoring-nginx.html
# https://github.com/martin-helmich/prometheus-nginxlog-exporter

import math
from constants import PROMETHEUS_URL, MULTIPLIER_AVERAGE_REQUEST_PROCESSING_TIME
from prometheus_api_client import PrometheusConnect
import sys
import traceback
from collections.abc import Sequence


# TODO use average[5m] for metrics that have instance point
class PrometheusReader:
    def __init__(self, host):
        self.host = host
        self.prometheus = PrometheusConnect(url=PROMETHEUS_URL)
        self.last_successful_results = dict()

    def get_prometheus_query_result_value(self, prometheus_query_result, result_type):
        if result_type == 'scalar':
            return self.get_scalar_value(prometheus_query_result)
        if result_type == 'vector':
            return self.get_vector_value(prometheus_query_result)
        raise Exception(f'unknown result_type: {result_type} in get_prometheus_query_result_value(), prometheus_query_result={prometheus_query_result}')

    def get_scalar_value(self, prometheus_query_result):
        if isinstance(prometheus_query_result, Sequence): 
            prometheus_query_result = prometheus_query_result[0]
        return float(prometheus_query_result['value'][1])

    def get_vector_value(self, prometheus_query_result):
        return prometheus_query_result

    def query_prometheus(self, query, result_type = 'scalar'):
        query = query.replace('$host', self.host)
        query = query.replace('$datacenter', '.*')
        query = query.replace('$type', '.*')
        query = query.replace('job=~"nginx"','job=~".*nginx.*"')
        result = self.prometheus.custom_query(query=query)

        # "value": [ <unix_time>, "<sample_value>" ]
        # source: https://prometheus.io/docs/prometheus/latest/querying/api/#expression-query-result-formats
        if len(result) == 0:
            print(f"query_prometheus {query} returned no result")
            print(f"returning self.last_successful_results[query]: {self.last_successful_results[query]}")
            return self.last_successful_results[query]
        
        output = self.get_prometheus_query_result_value(result, result_type)
        self.last_successful_results[query] = output
        return output
    
    def read_system_resources(self):
        resources = {}
        return resources

        resources['total_ram_memory'] = make_round(int(self.query_prometheus(
            'node_memory_MemTotal_bytes{datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*"}'
        )) / (1024 * 1024 * 1024))

        resources['total_disk'] = make_round(int(self.query_prometheus(
            'node_filesystem_size_bytes{datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*", mountpoint="/"}'
        )) / (1024 * 1024 * 1024))

        resources['cpu_cores'] = int(self.query_prometheus(
            'count(count(node_cpu_seconds_total{datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*"}) by (cpu))'
            # 'count(node_cpu_seconds_total{mode="idle", datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*"})'
        ))
        return resources

    def read_system_status(self):
        status = {}
        status['system_load'] = make_round(float(self.query_prometheus(
            'avg(node_load5{instance=~"$host.myket.*"}) /  count(count(node_cpu_seconds_total{instance=~"$host.myket.*"}) by (cpu))'
        )) * 100)

        status['cpu_usage'] = make_round(float(self.query_prometheus(
            '1 - avg(rate(node_cpu_seconds_total{datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*" ,mode="idle"}[5m]))'
        )) * 100)

        status['cpu_iowait'] = make_round(float(self.query_prometheus(
            'avg(rate(node_cpu_seconds_total{datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*" ,mode="iowait"}[5m]))'
        )) * 100)

        status['ram_memory_usage'] = make_round(float(self.query_prometheus(
            '1 - node_memory_MemAvailable_bytes{datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*"} / node_memory_MemTotal_bytes{datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*"}'
        )) * 100)

        #status['disk_usage'] = make_round(float(self.query_prometheus(
        #    '1 - (node_filesystem_avail_bytes{datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*", mountpoint="/"} / node_filesystem_size_bytes{datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*", mountpoint="/"})'
        #)) * 100)

        status['disk_io_usage'] = make_round(float(self.query_prometheus(
            'rate(node_disk_io_time_seconds_total {datacenter=~".*", node_type=~".*", instance=~"$host.myket.*", device=~"[a-z]*[a-z]"}[5m])'
        )) * 100)

        #status['disk_iops_reads'] = make_round(float(self.query_prometheus(
        #    'rate(node_disk_reads_completed_total {datacenter=~".*", node_type=~".*", instance=~"$host.myket.*", device=~"[a-z]*[a-z]"}[5m])'
        #)))

        status['disk_read_usage'] = make_round(float(self.query_prometheus(
            'rate(node_disk_read_time_seconds_total {datacenter=~".*", node_type=~".*", instance=~"$host.myket.*", device=~"[a-z]*[a-z]"}[5m])'
        )) * 20)

        #status['disk_iops_writes'] = make_round(float(self.query_prometheus(
        #    'rate(node_disk_writes_completed_total {datacenter=~".*", node_type=~".*", instance=~"$host.myket.*", device=~"[a-z]*[a-z]"}[5m])'
        #)))

        status['disk_write_usage'] = make_round(float(self.query_prometheus(
            'rate(node_disk_write_time_seconds_total {datacenter=~".*", node_type=~".*", instance=~"$host.myket.*", device=~"[a-z]*[a-z]"}[5m])'
        )) * 100)

        status['disk_reads_mbps'] = make_round(float(self.query_prometheus(
            'rate(node_disk_read_bytes_total {datacenter=~".*", node_type=~".*", instance=~"$host.myket.*", device=~"[a-z]*[a-z]"}[5m])'
        )) / (1024 * 1024 * 10))

        status['disk_writes_mbps'] = make_round(float(self.query_prometheus(
            'rate(node_disk_written_bytes_total {datacenter=~".*", node_type=~".*", instance=~"$host.myket.*", device=~"[a-z]*[a-z]"}[5m])'
        )) / (1024 * 1024 * 10))

        return status

    def read_input_load(self):
        workload = {}
        workload['number_of_requests_per_second'] = make_round(float(self.query_prometheus(
            'rate(nginx_vts_server_requests_total{job=~"nginx", datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*", host="*", code="total"}[5m])'
        )))

        workload['average_response_size_mb'] = make_round(float(self.query_prometheus(
            'sum(rate(nginx_vts_filter_bytes_total {job=~"nginx", datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*", direction="out"}[5m]))'
        )) / (1024 * 1024 * 10))

        return workload

    def read_system_performance(self):
        performance = {}

        # TODO nginx_vts_server_request_seconds vs. nginx_vts_filter_request_seconds
        weights = {
            'apk' : 1,
            'diff' : 1,
            'obb' : 1,

            'key':0.1,
            'playlist' : 0.2,
            'video-segments': 1,

            'image': 0.3,
        }

        averge_request_processing_times = self.query_prometheus(
            'avg_over_time(nginx_vts_filter_request_seconds{job=~".*", datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*", filter=~"uri.*", filter_name!~"others"}[5m])',
            'vector'
        )

        number_of_requests = self.query_prometheus(
            'rate(nginx_vts_filter_requests_total{job=~".*", datacenter=~"$datacenter", node_type=~".*", instance=~"$host.myket.*", direction="2xx",filter_name!~"others"}[5m])',
            'vector'
        )

        weighted_sum_request_processing_time_in_seconds = 0
        weighted_total_number_of_requests = 0
        for averge_request_processing_time in averge_request_processing_times:
            filter_name = averge_request_processing_time['metric']['filter_name']
            if not filter_name in weights:
                raise Exception(f"uknown filter name '{filter_name}'")
            number_of_requests_of_this_kind = self.get_scalar_value([r for r in number_of_requests if r['metric']['filter_name'] == filter_name])
            weighted_number_of_requests_of_this_kind = weights[filter_name] * number_of_requests_of_this_kind
            weighted_sum_request_processing_time_in_seconds += weighted_number_of_requests_of_this_kind * self.get_scalar_value(averge_request_processing_time)
            weighted_total_number_of_requests += weighted_number_of_requests_of_this_kind

        if weighted_total_number_of_requests:
            performance['average_request_processing_time_in_seconds'] = MULTIPLIER_AVERAGE_REQUEST_PROCESSING_TIME * weighted_sum_request_processing_time_in_seconds / weighted_total_number_of_requests
        else:
            # prevent 'division by zero'
            performance['average_request_processing_time_in_seconds'] = 0

        #state['p95_request_processing_time_in_seconds'] = make_round(float(self.query_prometheus(
        #    'histogram_quantile(0.95, nginx_vts_filter_request_duration_seconds {job=~"nginx", datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*", filter=~"uri.*"}[5m])'
        #)) / (1024 * 1024))

        performance['nginx_cache_hit_ratio'] = make_round(float(self.query_prometheus(
            'sum(rate(nginx_vts_cache_requests_total{job=~"nginx", datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*", status="hit"}[5m])) / (sum(rate(nginx_vts_cache_requests_total{job=~"nginx", datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*"}[5m])))'
        , 'scalar')) * 100)

        performance['nginx_writing_connections'] = make_round(float(self.query_prometheus(
            'avg_over_time(nginx_vts_main_connections{job=~"nginx", datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*", status="writing"}[5m])'
        )) / 10 )

        performance['average_network_transmit_mbps'] = make_round(float(self.query_prometheus(
            'sum(rate(node_network_transmit_bytes_total{datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*" ,device!~"tap.*|veth.*|br.*|docker.*|virbr*|lo*"}[5m]) * 8)'
        )) / (1024 * 1024 * 100))

        performance['number_of_5xx_errors_per_second'] = make_round(float(self.query_prometheus(
            'rate(nginx_vts_server_requests_total{job=~"nginx", datacenter=~"$datacenter", node_type=~"$type", instance=~"$host.myket.*", host="*", code="5xx"}[5m])'
        )) * 100)

        return performance

    def read_environment(self):
        state = {}
        state.update(self.read_system_resources())
        state.update(self.read_system_status())
        state.update(self.read_input_load())
        state.update(self.read_system_performance())
        return state


def make_round(x):
    if math.isnan(x):
        return 0
    else:
        return round(x)
