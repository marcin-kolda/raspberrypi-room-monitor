#!/usr/bin/env bash
mkdir -p data/sensor-raw 2> /dev/null
gsutil -m rsync -r gs://gcs-bucket-with-monitor-data data/sensor-raw

mkdir -p data/calendar-raw 2> /dev/null
gsutil -m rsync -r gs://gcs-bucket-with-calendar-data data/calendar-raw

./prepare_data.sh