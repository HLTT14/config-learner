#!/bin/bash

path='/var/log/remote/azd-stream-9.myket.ir/'

# calculate the date for two days ago
two_days_ago=$(date -d "2 days ago" +%Y-%m-%d)

# delete all files in the home directory except for the two most recent
sudo find $path -maxdepth 1 -type f ! -newermt "$two_days_ago" -delete

path='/home/vahid/gor_files/'
sudo find $path -maxdepth 1 -type f ! -newermt "$two_days_ago" -delete