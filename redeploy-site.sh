#!/bin/sh

tmux kill-server
cd flask-portfolio
git fetch && git reset origin/main --hard
python -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt

tmux new -s flask-portfolio -d
tmux send-keys -t flask-portfolio "source python3-virtualenv/bin/activate" C-m
tmux send-keys -t flask-portfolio "flask run --host=0.0.0.0" C-m