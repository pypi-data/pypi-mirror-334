# cns-nanoprometheus-client

## Úvod

**cns-nanoprometheus-client** je robustní Python balíček určený pro odesílání a správu metrik v rámci systému Nanoprometheus. Tento balíček nabízí širokou škálu nástrojů a funkcionalit, mezi které patří:

- **MetricsClient** – klient pro odesílání metrik přes TCP socket.
- Základní metriky: **Counter**, **Gauge**, **Histogram** a **Summary**.
- Vestavěné metriky jako **AppBuildInfo**, **RequestDurationSeconds**, **ErrorsTotal** a **OutgoingRequestDurationSeconds**.
- Bezpečné obaly pro metriky: **SafeMetricsLog** a **SafeMetricsNoLog**.
- Pokročilé logování pomocí vestavěného modulu `logging` s možností rotačního logování.
- Dodatečné moduly jako **config.py** pro načítání konfigurace, **aggregator.py** pro agregaci metrik a **exceptions.py** pro vlastní chybové stavy.
- Volitelný CLI entry point pro snadné spuštění testovací funkce a demonstraci funkcionality.

Tento soubor README.md poskytuje podrobný návod, jak nainstalovat, konfigurovat a používat tento balíček.

## Obsah

- [Funkcionalita](#funkcionalita)
- [Instalace](#instalace)
- [Použití](#použití)
  - [Základní příklady](#zaklad)
  - [Konfigurace logování](#logging)
- [Licence](#licence)
## Funkcionalita

Balíček **cns-nanoprometheus-client** nabízí několik modulů:

- **client.py:** Obsahuje třídu `MetricsClient`, která umožňuje odesílání metrik ve formě JSON zpráv přes TCP socket.
- **metrics.py:** Implementuje základní metriky jako Counter, Gauge, Histogram a Summary. Dále obsahuje vestavěné metriky pro sledování klíčových událostí v aplikaci. Funkce `test()` volá další funkci `open_readme()`, která otevře specifikovanou URL ve výchozím prohlížeči.
- **safe_metrics.py:** Zajišťuje obaly pro metriky, které potlačují výjimky tak, aby nedošlo k pádu aplikace. Nabízí variantu s logováním i variantu bez logování.
- **logging_config.py:** Konfiguruje pokročilé logování pomocí `logging` a `RotatingFileHandler`.
- **config.py, aggregator.py a exceptions.py:** Poskytují dodatečnou funkcionalitu pro načítání konfigurace, agregaci metrik a definici vlastních chybových stavů.

## Instalace

Nejprve doporučujeme vytvořit virtuální prostředí:

```bash
python3 -m venv venv
source venv/bin/activate      # Na Linuxu/macOS
venv\Scripts\activate         # Na Windows
```

Balíček lze nainstalovat z PyPI:

pip install cns-nanoprometheus-client

Nebo, pokud pracujete s lokálním repozitářem, použijte režim vývoje:

pip install -e .


## Pouziti
### Zaklad
Po instalaci můžete balíček importovat a používat takto:
```
from cns_nanoprometheus_client import MetricsClient, Counter

# Vytvoření klienta pro odesílání metrik
client = MetricsClient(host='127.0.0.1', port=5000)
success = client.send_metric("test_metric", 42, {"env": "production"})
if success:
    print("Metrika byla úspěšně odeslána.")
else:
    print("Odeslání metriky selhalo.")

# Použití základní metriky Counter
counter = Counter("my_counter", "Testovací čítač")
counter.inc()
print("Aktuální hodnota čítače:", counter.get())
```

### Logging
```
import logging
from cns_nanoprometheus_client.logging_config import setup_logging

# Nastavení logování (výchozí logovací soubor a úroveň)
logger = setup_logging(log_file="custom.log", level=logging.INFO)
logger.info("Logování je úspěšně nakonfigurováno.")
```
## Licence

MIT License

Copyright (c) 2025 Roman Skvara

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
