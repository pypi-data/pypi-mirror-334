import statistics
import logging

logger = logging.getLogger("cns_nanoprometheus.aggregator")

def aggregate_metrics(metrics_list):
    """
    Agreguje seznam číselných hodnot a vrací statistický souhrn.
    """
    if not metrics_list:
        logger.warning("Seznam metrik je prázdný.")
        return {"count": 0, "avg": None, "median": None, "min": None, "max": None}
    
    count = len(metrics_list)
    avg = sum(metrics_list) / count
    median = statistics.median(metrics_list)
    return {
        "count": count,
        "avg": avg,
        "median": median,
        "min": min(metrics_list),
        "max": max(metrics_list)
    }

def combine_counters(counters):
    """
    Kombinuje seznam čítačů (číselných hodnot) do jednoho součtu.
    """
    total = sum(counters)
    logger.info(f"Kombinace čítačů: {counters} -> {total}")
    return total
