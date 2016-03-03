#!/usr/bin/env bash
set -e

cd /root/bot

git pull
env/bin/pip install --upgrade -r requirements.txt
crontab crontab
