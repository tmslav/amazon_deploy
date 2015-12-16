#!/bin/sh
cd /home/ubuntu/
yes | rm -rf amazon_deploy
git pull https://github.com/tmslav/amazon_deploy.git
tmux new-session -d "/usr/bin/python  /home/ubuntu/amazon_deploy/app.py"
