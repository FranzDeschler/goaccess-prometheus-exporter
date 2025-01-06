#!/bin/bash
/usr/bin/goaccess \
  --datetime-format='%d/%b/%Y:%H:%M:%S %z' \
  --log-format='[%x] %^ %^ %s - %m %^ %v "%U" [Client %h] [Length %b] [Gzip %^] [Sent-to %^] "%u" "%R"' \
  --tz='Europe/Berlin' \
  -f /opt/logs/access.log \
  -o /goaccess-prometheus-exporter/metrics.json