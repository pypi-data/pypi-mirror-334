"""
cns_nanoprometheus_client

Tento balíček poskytuje nástroje pro odesílání metrik do systému Nanoprometheus.
Obsahuje:
- MetricsClient: klient pro odesílání měření přes socket.
- Základní metriky: Counter, Gauge, Histogram, Summary.
- Built-in metriky: AppBuildInfo, RequestDurationSeconds, ErrorsTotal, OutgoingRequestDurationSeconds.
- Bezpečné obaly: SafeMetricsLog a SafeMetricsNoLog.
- Pokročilé logování: konfigurace v logging_config.py.
"""

from .client import MetricsClient
from .metrics import (
    Counter, Gauge, Histogram, Summary,
    AppBuildInfo, RequestDurationSeconds, ErrorsTotal, OutgoingRequestDurationSeconds
)
from .safe_metrics import SafeMetricsLog, SafeMetricsNoLog
from .logging_config import setup_logging

__all__ = [
    "MetricsClient",
    "Counter", "Gauge", "Histogram", "Summary",
    "AppBuildInfo", "RequestDurationSeconds", "ErrorsTotal", "OutgoingRequestDurationSeconds",
    "SafeMetricsLog", "SafeMetricsNoLog",
    "setup_logging",
]

def main():
    """
    Hlavní funkce balíčku, která zavolá inicializační funkci z metrics.py.
    """
    from .metrics import test
    test()

if __name__ == '__main__':
    main()
