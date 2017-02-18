#!/usr/bin/env bash

# trap ctrl-c and call clean_up
trap clean_up SIGHUP SIGINT SIGTERM

function clean_up {
    pkill -f viral_wars_server.py
    pkill -f viral_wars_client.py
}

# start fresh
clean_up

python viral_wars_server.py &
python viral_wars_client.py

clean_up