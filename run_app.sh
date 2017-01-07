#!/bin/bash

PROCESS=`ps -ef|grep -w  application.py|grep -v grep|grep -v PPID|awk '{ print $2}'`
for i in $PROCESS
do
	kill -9 $i
done

sleep 1

nohup ./application.py > ./logs/app.out 2>&1 &
tail -f logs/server.log
