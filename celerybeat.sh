#!/bin/bash
cd /home/local_server
source env/bin/activate
exec celery -A server beat --loglevel=info
