#!/bin/bash

celery -A tasks.tasks worker -Q celery --loglevel=info
