#!/bin/bash

nohup flower -A tasks.wechat --port=5555 > /dev/null 2>&1 &
