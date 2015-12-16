#!/bin/sh
cd /home/ubuntu/amazon_deploy
git pull
tmux new-session "/usr/bin/python  /home/ubuntu/amazon_deploy/app.py"
