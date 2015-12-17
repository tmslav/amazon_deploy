#!/bin/sh
cd /home/ubuntu/
yes | rm -rf amazon_deploy
git clone https://github.com/tmslav/amazon_deploy.git
cd amazon_deploy
tmux new-session -d "python  app.py"
