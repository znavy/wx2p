#!/bin/bash

celery -A tasks.wechat worker -Q celery --loglevel=info
