import os
from dataclasses import dataclass
from dotenv import load_dotenv
from app.exceptions import ConfigurationError

load_dotenv()

@dataclass
class CalculatorConfig:
    log_dir:str
    history_dir:str
    max_history_size:int
    autosave:bool
    precision:int
    max_input:float
    default_encoding:str
    log_file:str
    history_file:str

    @classmethod
    def load(cls) -> "CalculatorConfig":
        try:
            config=cls(
                log_dir=os.getenv("CALCULATOR_LOG_DIR", "logs"),
                history_dir=os.getenv("CALCULATOR_HISTORY_DIR", "history"),
                max_history_size=int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100")),
                auto_save=os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true",
                precision=int(os.getenv("CALCULATOR_PRECISION", "10")),
                max_input_value=float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e15")),
                default_encoding=os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8"),
                log_file=os.getenv("CALCULATOR_LOG_FILE", "logs/calculator.log"),
                history_file=os.getenv("CALCULATOR_HISTORY_FILE", "history/calculator_history.csv"),
            )
         except ValueError as e:
            raise ConfigurationError(f"Invalid configuration value: {e}") from e

        config._ensure_directories()
        return config

    def _ensure_directories(self) -> None:
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)
