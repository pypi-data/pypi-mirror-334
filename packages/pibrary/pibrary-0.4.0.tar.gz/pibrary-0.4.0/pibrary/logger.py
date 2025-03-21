import warnings
from .loguru import logger as loguru_pro

# Optional: Warn users about the new module
warnings.warn(
    "The 'logger' module is deprecated and will be removed in a future version. Please update your imports to use 'pibrary.loguru'.",
    DeprecationWarning,
    stacklevel=2,
)

# Keep using the LoguruPro from loguru.py
logger = loguru_pro

# If users directly used `timeit`, maintain that interface
timeit = logger.timeit
