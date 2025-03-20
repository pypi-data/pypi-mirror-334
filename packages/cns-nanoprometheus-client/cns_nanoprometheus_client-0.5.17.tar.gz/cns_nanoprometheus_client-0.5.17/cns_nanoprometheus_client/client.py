"""
Modul client.py

Obsahuje třídu MetricsClient, která umožňuje odesílání jednotlivých měření
do Nanoprometheus systému přes socket. Pro logování využíváme pokročilý logging.
"""

import socket
import json
import time
import logging

# Získáme logger pro tento modul
logger = logging.getLogger('cns_nanoprometheus.client')

class MetricsClient:
    """
    Třída MetricsClient zajišťuje odesílání metrik přes TCP socket.
    """

    def __init__(self, host: str = 'localhost', port: int = 5000, timeout: float = 5.0):
        """
        Inicializace klienta.

        :param host: Adresa serveru.
        :param port: Port serveru.
        :param timeout: Timeout pro socket.
        """
        self.host = host
        self.port = port
        self.timeout = timeout

    def send_metric(self, metric_name: str, value, labels: dict = None) -> bool:
        """
        Odeslání metriky na server.

        :param metric_name: Název metriky.
        :param value: Hodnota metriky.
        :param labels: Slovník s dodatečnými informacemi.
        :return: True pokud se podařilo odeslat, jinak False.
        """
        data = {
            "timestamp": time.time(),
            "metric": metric_name,
            "value": value,
            "labels": labels or {}
        }
        try:
            serialized = json.dumps(data)
            with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
                sock.sendall(serialized.encode('utf-8'))
            return True
        except Exception as e:
            logger.exception(f"Chyba při odesílání metriky {metric_name}: {e}")
            return False

    def __repr__(self):
        return f"<MetricsClient host={self.host} port={self.port}>"

# --- Demonstrace použití ---
if __name__ == '__main__':
    # Ukázkový běh klienta, který se pokusí odeslat testovací metriku.
    client = MetricsClient()
    success = client.send_metric("test_metric", 123, {"env": "test"})
    if success:
        print("Metrika odeslána úspěšně.")
    else:
        print("Odeslání metriky selhalo.")
