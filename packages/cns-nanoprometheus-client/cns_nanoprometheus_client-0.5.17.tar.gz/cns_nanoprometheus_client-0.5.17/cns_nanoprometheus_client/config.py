import os
import json
import logging

logger = logging.getLogger("cns_nanoprometheus.config")

DEFAULT_CONFIG = {
    "host": "localhost",
    "port": 5000,
    "timeout": 5.0,
    "log_file": "cns_nanoprometheus.log",
    "log_level": "DEBUG"
}

def load_config(config_file: str = None) -> dict:
    config = DEFAULT_CONFIG.copy()
    if config_file:
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                file_config = json.load(f)
            config.update(file_config)
            logger.info(f"Konfigurace načtena ze souboru {config_file}")
        except Exception as e:
            logger.exception(f"Chyba při načítání konfigurace ze souboru {config_file}: {e}")
    else:
        logger.info("Používám výchozí konfiguraci.")
    
    config["host"] = os.getenv("CNS_NANO_HOST", config["host"])
    config["port"] = int(os.getenv("CNS_NANO_PORT", config["port"]))
    config["timeout"] = float(os.getenv("CNS_NANO_TIMEOUT", config["timeout"]))
    config["log_file"] = os.getenv("CNS_NANO_LOG_FILE", config["log_file"])
    config["log_level"] = os.getenv("CNS_NANO_LOG_LEVEL", config["log_level"])
    
    return config
