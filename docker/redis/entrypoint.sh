#!/bin/bash
/usr/local/bin/create_config.sh
exec redis-server ./redis.conf
