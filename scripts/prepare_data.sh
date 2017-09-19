#!/usr/bin/env bash
echo "filtering sensor data"
find data/sensor-raw -type f -name 'sensor_output.log.*' -exec cat {} \; \
| grep -a -E "^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+,\d+,\d+$" > data/sensor_output.csv

echo "merging calendar data data"
cd python/parser

python main.py "/Users/user/workspace/raspberrypi-room-monitor/scripts/data/calendar-raw/*/*.json" "../../data/merged_events.csv"

cd ../..