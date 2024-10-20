from config import AppConfig
from loguru import logger

logger = logger.opt(lazy=True).bind(application_name=AppConfig.application_name)
