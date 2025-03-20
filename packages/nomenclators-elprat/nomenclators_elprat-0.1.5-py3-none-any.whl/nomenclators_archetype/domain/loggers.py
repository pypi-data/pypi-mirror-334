"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón(y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
import logging
import sys
import os

LOGGER_LEVEL_NAME = "LOGGER_LEVEL"
LOGGER_LEVEL_DAFAULT = "INFO"
LOGGER_LEVEL = os.getenv("LOGGER_LEVEL", "INFO").upper()

# Default Logger
logging.basicConfig(
    level=getattr(logging, LOGGER_LEVEL, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)
default_logger = logging.getLogger("default_logger")
