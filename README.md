# goaccess-prometheus-exporter

Prometheus exporter for metrics provided by [GoAccess](https://goaccess.io).

It´s currently configured to work with [Nginx Proxy Manager](https://nginxproxymanager.com) but can easily be
reconfigured to work with any other access logs.

## Setup

1) Download this project to your local file system
```shell
git clone https://github.com/FranzDeschler/goaccess-prometheus-exporter
```

2) Adjust the `GoAccess` call in the `/resources/run_goaccess.sh` script to your needs.
   See the [GoAccess man page](https://goaccess.io/man) for parameters.

3) In the `docker-compose.yml` file, adjust the following settings:
   - `LOG_FILES` environment variable: a comma separated list of file names. Wildcards like "*.log" are also possible.
   - `TIMEZONE` environment variable: A canonical timezone name like "Europe/Berlin". Default is "Etc/UTC".
   - port mapping
   - replace  the `LOG_DIRECTORY` placeholder with the directory where your log files are that you want to monitor

4) Create and run the Docker container.
```shell
docker-compose up
```

## Counter Reset
Note that most metrics provided by this exporter are counters.
Those counters will be reset as soon as log rotation is applied to the log files you are monitoring.
If your log files are rotated daily, the counters will also be reset daily.