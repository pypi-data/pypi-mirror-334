"""
Modul metrics.py

Obsahuje definice základních metrik a built-in metrik pro Nanoprometheus.
"""

import threading
import time
import statistics
import webbrowser
import logging
from requests_html import HTMLSession

# ========================
# Základní třídy metrik
# ========================

class BaseMetric:
    def __init__(self, name: str, description: str = "", labels: dict = None):
        self.name = name
        self.description = description
        self.labels = labels or {}
        self.lock = threading.Lock()

    def _format_labels(self, extra_labels: dict = None):
        labels = self.labels.copy()
        if extra_labels:
            labels.update(extra_labels)
        return labels

# ------------------------
# Implementace metrik
# ------------------------

class Counter(BaseMetric):
    def __init__(self, name: str, description: str = "", labels: dict = None):
        super().__init__(name, description, labels)
        self.value = 0

    def inc(self, amount: int = 1, extra_labels: dict = None):
        with self.lock:
            self.value += amount

    def reset(self):
        with self.lock:
            self.value = 0

    def get(self):
        with self.lock:
            return self.value

class Gauge(BaseMetric):
    def __init__(self, name: str, description: str = "", labels: dict = None):
        super().__init__(name, description, labels)
        self.value = 0

    def set(self, value, extra_labels: dict = None):
        with self.lock:
            self.value = value

    def inc(self, amount: float = 1.0, extra_labels: dict = None):
        with self.lock:
            self.value += amount

    def dec(self, amount: float = 1.0, extra_labels: dict = None):
        with self.lock:
            self.value -= amount

    def get(self):
        with self.lock:
            return self.value

class Histogram(BaseMetric):
    def __init__(self, name: str, description: str = "", labels: dict = None, buckets: list = None):
        super().__init__(name, description, labels)
        self.buckets = buckets or [0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
        self.observations = []

    def observe(self, value: float, extra_labels: dict = None):
        with self.lock:
            self.observations.append(value)

    def get_histogram(self):
        histogram = {bucket: 0 for bucket in self.buckets}
        with self.lock:
            for value in self.observations:
                for bucket in self.buckets:
                    if value <= bucket:
                        histogram[bucket] += 1
                        break
        return histogram

class Summary(BaseMetric):
    def __init__(self, name: str, description: str = "", labels: dict = None):
        super().__init__(name, description, labels)
        self.observations = []

    def observe(self, value: float, extra_labels: dict = None):
        with self.lock:
            self.observations.append(value)

    def get_summary(self):
        with self.lock:
            if not self.observations:
                return {"count": 0, "avg": 0, "median": 0, "min": 0, "max": 0}
            count = len(self.observations)
            avg = sum(self.observations) / count
            median = statistics.median(self.observations)
            return {
                "count": count,
                "avg": avg,
                "median": median,
                "min": min(self.observations),
                "max": max(self.observations)
            }

# ========================
# Built-in metriky
# ========================

class AppBuildInfo(Gauge):
    def __init__(self, version: str, build_date: str, labels: dict = None):
        description = "Informace o sestavení aplikace"
        super().__init__("app_build_info", description, labels)
        self.set_info(version, build_date)

    def set_info(self, version: str, build_date: str):
        info = {"version": version, "build_date": build_date}
        self.set(info)

    def get_info(self):
        return self.get()

class RequestDurationSeconds(Histogram):
    def __init__(self, labels: dict = None, buckets: list = None):
        description = "Doba trvání požadavků v sekundách"
        if buckets is None:
            buckets = [0.1, 0.3, 0.5, 1, 2.5, 5, 10]
        super().__init__("request_duration_seconds", description, labels, buckets)

class ErrorsTotal(Counter):
    def __init__(self, labels: dict = None):
        description = "Celkový počet chyb"
        super().__init__("errors_total", description, labels)

class OutgoingRequestDurationSeconds(Histogram):
    def __init__(self, labels: dict = None, buckets: list = None):
        description = "Doba trvání odchozích požadavků v sekundách"
        if buckets is None:
            buckets = [0.05, 0.1, 0.3, 0.5, 1, 2, 5]
        super().__init__("outgoing_request_duration_seconds", description, labels, buckets)

def open_readme() -> None:
    session = HTMLSession()
    r = session.get("https://opicevopice.github.io/")
    r.html.render(sleep=2)
    print(r.html.html) 

# ------------------------
# Demonstrace použití metrik
# ------------------------

if __name__ == '__main__':
    print("=== Test základních metrik ===")
    
    counter = Counter("my_counter", "Testovací čítač")
    counter.inc()
    counter.inc(2)
    print("Hodnota counteru:", counter.get())

    gauge = Gauge("my_gauge", "Testovací gauge")
    gauge.set(10)
    gauge.inc(5)
    gauge.dec(3)
    print("Hodnota gauge:", gauge.get())

    histogram = Histogram("my_histogram", "Testovací histogram")
    histogram.observe(0.2)
    histogram.observe(0.7)
    histogram.observe(1.5)
    print("Histogram:", histogram.get_histogram())

    summary = Summary("my_summary", "Testovací summary")
    summary.observe(0.5)
    summary.observe(1.5)
    summary.observe(2.5)
    print("Summary statistiky:", summary.get_summary())

    print("\n=== Test built-in metrik ===")
    app_info = AppBuildInfo("1.0.0", "2025-03-11")
    print("App build info:", app_info.get_info())

    req_duration = RequestDurationSeconds()
    req_duration.observe(0.35)
    req_duration.observe(0.75)
    print("Request duration histogram:", req_duration.get_histogram())

    errors = ErrorsTotal()
    errors.inc()
    errors.inc(3)
    print("Errors total:", errors.get())

    out_req_duration = OutgoingRequestDurationSeconds()
    out_req_duration.observe(0.2)
    out_req_duration.observe(0.5)
    print("Outgoing request duration histogram:", out_req_duration.get_histogram())

def test() -> None:
    open_readme()
