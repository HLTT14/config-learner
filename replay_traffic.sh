#!/usr/bin/env bash
date

path=/home/vahid/config-learner

days_ago=${1:-1}
yesterday=$(date -d "-${days_ago} days" '+%Y-%m-%d')
echo "set yesterday=$yesterday"

sudo $path/copy_nginx_log_to_home.sh $days_ago

source $path/venv/bin/activate

mkdir -p '/home/vahid/logs'

echo "convert yesterday traffic to gor"
python $path/convert_nginx_traffic_to_gor.py --days_ago $days_ago >> /home/vahid/logs/convert_to_gor_logs_${yesterday}.txt

echo "replay yesterday traffic"
nohup /home/vahid/goreplay/goreplay --input-file /home/vahid/gor_files/${yesterday}.gor  --output-http https://azd-stream-16.myket.ir --output-http-timeout 300s --output-http-track-response --verbose 10 > /home/vahid/logs/run_gor_logs${yesterday}.txt 2>&1 

