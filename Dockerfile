FROM alpine:latest

RUN apk update &&  \
    apk add --no-cache \
    bash \
    python3 \
    "goaccess=1.9.3-r0"

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /goaccess-prometheus-exporter
COPY /src/* .
COPY /resources/* .
RUN chmod +x run_goaccess.sh

VOLUME ["/opt/logs"]
EXPOSE 9100
ENTRYPOINT ["python3", "/goaccess-prometheus-exporter/main.py"]