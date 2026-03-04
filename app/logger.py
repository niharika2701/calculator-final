import logging
import os
from app.calculator_config import CalculatorConfig


class Logger:
    _instance: logging.Logger | None = None

    @classmethod
    def get_logger(cls, config: CalculatorConfig | None = None) -> logging.Logger:
        if cls._instance is None:
            cls._instance = cls._setup(config or CalculatorConfig.load())
        return cls._instance

    @classmethod
    def _setup(cls, config: CalculatorConfig) -> logging.Logger:
        logger = logging.getLogger("calculator")
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        os.makedirs(os.path.dirname(config.log_file), exist_ok=True)
        file_handler = logging.FileHandler(
            config.log_file,
            encoding=config.default_encoding
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger

    @classmethod
    def reset(cls) -> None:
        if cls._instance:
            cls._instance.handlers.clear()
        cls._instance = None