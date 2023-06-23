#!/usr/bin/env bash
mkdir -p '/home/vahid/gor_files'

# sets the default value of days_ago to 1 if $1 is not provided
days_ago=${1:-1}

yesterday=$(date -d "-${days_ago} days" '+%Y-%m-%d')

mv /var/log/remote/azd-stream-9.myket.ir/${yesterday}* /home/vahid/gor_files
chown vahid: /home/vahid/gor_files/${yesterday}*
find . -size 0 -delete
#gzip -d ${yesterday}*
#mv ${yesterday}.log.1 ${yesterday}.log