#!/bin/bash

PROCESS=`ps -ef|grep -w  application.py|grep -v grep|grep -v PPID|awk '{ print $2}'`
kill -9 $PROCESS

sleep 2

nohup ./application.py > ./logs/app.out 2>&1 &
tail -f logs/server.log
