#!/bin/bash

PROCESS=`ps -ef|grep -w  celery|grep -v grep|grep -v PPID|awk '{ print $2}'`
for i in $PROCESS
do
	kill -9 $i
done

sleep 2

nohup celery -A tasks.wechat worker -Q celery --loglevel=info >> logs/task.log 2>&1 &
