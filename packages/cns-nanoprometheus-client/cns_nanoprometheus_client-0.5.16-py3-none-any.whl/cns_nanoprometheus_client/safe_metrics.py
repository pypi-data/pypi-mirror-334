"""
Modul safe_metrics.py

Obsahuje obaly pro metriky, které zajistí, že výjimky nebudou probublávat do aplikace.
Implementace využívá pokročilý logging (modul logging) pro zaznamenávání chyb.
"""

import functools
import logging

# Získáme logger pro tento modul
logger = logging.getLogger('cns_nanoprometheus.safe_metrics')

class SafeMetricsLog:
    """
    Obal pro metriky, který loguje výjimky pomocí pokročilého logování.
    """
    def __init__(self, metric):
        self._metric = metric

    def __getattr__(self, attr):
        orig_attr = getattr(self._metric, attr)
        if callable(orig_attr):
            @functools.wraps(orig_attr)
            def safe_call(*args, **kwargs):
                try:
                    return orig_attr(*args, **kwargs)
                except Exception as e:
                    logger.exception(
                        f"Výjimka v metodě {attr} u metriky {self._metric.name}: {e}"
                    )
                    return None
            return safe_call
        else:
            return orig_attr

class SafeMetricsNoLog:
    """
    Obal pro metriky, který potlačuje výjimky bez logování.
    """
    def __init__(self, metric):
        self._metric = metric

    def __getattr__(self, attr):
        orig_attr = getattr(self._metric, attr)
        if callable(orig_attr):
            @functools.wraps(orig_attr)
            def safe_call(*args, **kwargs):
                try:
                    return orig_attr(*args, **kwargs)
                except Exception:
                    # Potlačíme výjimku bez logování
                    return None
            return safe_call
        else:
            return orig_attr

# ------------------------
# Demonstrace použití Safe Metrics obalů
# ------------------------

if __name__ == '__main__':
    from metrics import Counter

    print("=== Test SafeMetricsLog a SafeMetricsNoLog ===")
    
    # Vytvoříme metrický objekt, který simuluje výjimku
    faulty_metric = Counter("faulty_counter", "Čítač, který simuluje výjimku")
    
    # Předěláme metodu inc tak, aby vyvolávala výjimku
    def faulty_inc(*args, **kwargs):
        raise ValueError("Simulovaná výjimka")
    faulty_metric.inc = faulty_inc

    safe_log = SafeMetricsLog(faulty_metric)
    safe_nolog = SafeMetricsNoLog(faulty_metric)

    print("Test SafeMetricsLog:")
    result_log = safe_log.inc()  # Výjimka bude zalogována pomocí pokročilého logování
    print("Výsledek s logováním:", result_log)

    print("Test SafeMetricsNoLog:")
    result_nolog = safe_nolog.inc()  # Výjimka bude potlačena bez logování
    print("Výsledek bez logování:", result_nolog)
