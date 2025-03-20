"""
Modul logging_config.py

Tento modul poskytuje funkci pro nastavení pokročilého logování pomocí vestavěného modulu logging.
Konfigurace zahrnuje rotační souborový handler a konzolový handler.
"""

import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file: str = 'cns_nanoprometheus.log', level: int = logging.DEBUG):
    """
    Nastaví logování pro celý balíček.

    :param log_file: Název souboru, do kterého se logují zprávy.
    :param level: Úroveň logování.
    :return: Konfigurovaný logger.
    """
    logger = logging.getLogger('cns_nanoprometheus')
    logger.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Rotační handler (max 5MB, 3 zálohy)
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler pro výstup na konzoli
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# Při importu můžeme nastavit základní konfiguraci, případně se volá explicitně z aplikačního kódu
setup_logging()
