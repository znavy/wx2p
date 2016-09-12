#!/bin/bash

nohup ./application.py > ./logs/app.out 2>&1 &
echo 'OK'
