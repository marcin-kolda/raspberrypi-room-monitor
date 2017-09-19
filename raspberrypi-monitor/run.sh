#!/usr/bin/env bash
./update.sh
ssh -t pi@dex.local 'cd  ~/conf-room-monitor/;python run_sensors.py'