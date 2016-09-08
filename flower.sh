#!/bin/bash

celery -A tasks.tasks flower --broker_api=http://h2r:h2r123123@192.168.1.118:15672/api/
