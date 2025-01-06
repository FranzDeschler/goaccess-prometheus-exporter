class MetricsConverter:
    """
    Converts the metrics provided by goaccess to prometheus exposition format.
    See https://github.com/prometheus/docs/blob/main/content/docs/instrumenting/exposition_formats.md
    """

    def __init__(self, metrics):
        self.metrics = metrics
        self.result = ""

    def convert(self):
        self._log_size()
        self._log_parsing_time()
        self._total_requests()
        self._valid_requests()
        self._failed_requests()
        self._excluded_requests()
        self._not_found()
        self._transferred_bytes()
        self._requests_by_os()
        self._requests_by_browser()
        self._time_distribution()
        self._virtual_hosts()
        self._status_codes()
        return self.result

    def _log_size(self):
        self._counter(
            "log_size_bytes",
            "The size of the log file(s) in bytes.",
            self.metrics["general"]["log_size"])

    def _log_parsing_time(self):
        self._gauge(
            "log_parsing_time_seconds",
            "The time required to parse the logs in seconds.",
            self.metrics["general"]["generation_time"])

    def _total_requests(self):
        self._counter(
            "http_requests_total",
            "The total number of HTTP requests.",
            self.metrics["general"]["total_requests"])

    def _valid_requests(self):
        self._counter(
            "http_valid_requests_total",
            "The total number of valid HTTP requests.",
            self.metrics["general"]["valid_requests"])

    def _failed_requests(self):
        self._counter(
            "http_failed_requests_total",
            "The total number of failed HTTP requests.",
            self.metrics["general"]["failed_requests"])

    def _excluded_requests(self):
        self._counter(
            "http_excluded_requests_total",
            "The total number of excluded HTTP requests.",
            self.metrics["general"]["excluded_hits"])

    def _not_found(self):
        self._counter(
            "http_requests_not_found_total",
            "The total number of HTTP requests that returned 404 status code.",
            self.metrics["not_found"]["metadata"]["hits"]["total"]["value"])

    def _transferred_bytes(self):
        self._counter(
            "transferred_bytes_total",
            "The total number of transferred bytes.",
            self.metrics["general"]["bandwidth"])

    def _requests_by_os(self):
        self._histogram(
            "http_request_os",
            "The number of HTTP requests per operating system.",
            "os")

    def _requests_by_browser(self):
        self._histogram(
            "http_request_browser",
            "The number of HTTP requests per browser.",
            "browsers", "browser")

    def _time_distribution(self):
        self._histogram(
            "http_request_hour",
            "The number of HTTP requests distributed over the hours of the day.",
            "visit_time", "hour")

    def _virtual_hosts(self):
        self._histogram(
            "http_request_vhost",
            "The number of HTTP requests per virtual host.",
            "vhosts", "host")

    def _status_codes(self):
        self._histogram(
            "http_request_status_code",
            "The number of HTTP requests per status code.",
            "status_codes", "status_code")

    def _counter(self, name, description, value):
        self.result += self._stringify(name, description, "counter", value)

    def _gauge(self, name, description, value):
        self.result += self._stringify(name, description, "gauge", value)

    def _histogram(self, name, description, category, label_name=None):
        if label_name is None:
            label_name = category

        sum = self.metrics[category]["metadata"]["hits"]["total"]["value"]
        self.result += (f"# HELP {name} {description}\n"
                        f"# TYPE {name} histogram\n"
                        f"{name}_sum {sum}\n")

        for entry in self.metrics[category]["data"]:
            data = entry["data"]
            value = entry["hits"]["count"]
            self.result += f'{name}{{{label_name}="{data}"}} {value}\n'

    @staticmethod
    def _stringify(name, description, type, value):
        return (f"# HELP {name} {description}\n"
                f"# TYPE {name} {type}\n"
                f"{name} {value}\n")
