#!/bin/bash

username="${REDIS_USER}"
password="${REDIS_PASSWORD}"

echo "user $username +@all ~* on >$password" > ./redis.conf
