#!/usr/bin/env bash
set -e

cd /root/bot

# http://stackoverflow.com/a/3278427
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
    exit 0
elif [ $LOCAL = $BASE ]; then
    echo "Updating ..."
elif [ $REMOTE = $BASE ]; then
    echo "WTF? Need to push."
    exit 1
else
    echo "WTF? Diverged."
    exit 1
fi

git pull
env/bin/pip install --upgrade -r requirements.txt
crontab crontab
