#!/bin/sh
sleep 30
pip install -r $(pwd)docker-entrypoint-initsolution.d/requirements.txt
python $(pwd)docker-entrypoint-initsolution.d/main.py
