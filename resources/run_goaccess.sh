#!/bin/bash

if [ -z "$LOG_FILES" ]; then
  echo "LOG_FILES environment variable is not set."
  exit 1
fi

LOG_PATHS=""
if [[ "$LOG_FILES" == *,* ]]; then
  # multiple log files
  # replace commas with spaces
  LOG_FILES="${LOG_FILES//,/ }"

  for file in LOG_FILES; do
    LOG_PATHS+="/opt/logs/$file "
  done
else
  # single log file
  LOG_PATHS="/opt/logs/$LOG_FILES"
fi

/usr/bin/goaccess \
  --datetime-format='%d/%b/%Y:%H:%M:%S %z' \
  --log-format='[%x] %^ %^ %s - %m %^ %v "%U" [Client %h] [Length %b] [Gzip %^] [Sent-to %^] "%u" "%R"' \
  --tz=$TIMEZONE \
  -f $LOG_PATHS \
  -o /goaccess-prometheus-exporter/metrics.json