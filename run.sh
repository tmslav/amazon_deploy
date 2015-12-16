#!/bin/sh
cd /home/ubuntu/amazon_deploy
rm *.py
rm *.log
rm *.pyc
rm *.md
rm *.html
git pull
tmux new-session -d "/usr/bin/python  /home/ubuntu/amazon_deploy/app.py"
