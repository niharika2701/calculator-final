import sys
from colorama import Fore, Style, init as colorama_init

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.logger import Logger
from app.observers import LoggingObserver, AutoSaveObserver
from app.commands import build_command_registry
from app.exceptions import CalculatorException


def print_banner() -> None:
    print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════╗
║         ADVANCED CALCULATOR v1.0         ║
║   Type 'help' for commands, 'exit' quit  ║
╚══════════════════════════════════════════╝
""" + Style.RESET_ALL)


def print_success(message: str) -> None:
    print(Fore.GREEN + "  ✓ " + message + Style.RESET_ALL)


def print_error(message: str) -> None:
    print(Fore.RED + "  ✗ " + message + Style.RESET_ALL)


def print_info(message: str) -> None:
    print(Fore.YELLOW + message + Style.RESET_ALL)


def run_repl() -> None:  # pragma: no cover
    colorama_init(autoreset=True)

    config = CalculatorConfig.load()
    logger = Logger.get_logger(config)
    calculator = Calculator(config)

    
    calculator.add_observer(LoggingObserver(logger))
    calculator.add_observer(
        AutoSaveObserver(config, calculator.get_history_object())
    )

    commands = build_command_registry()

    print_banner()

    while True:
        try:
            raw = input(Fore.CYAN + "calc> " + Style.RESET_ALL).strip()
        except (EOFError, KeyboardInterrupt):
            print_info("\nGoodbye!")
            sys.exit(0)

        if not raw:
            continue

        parts = raw.split()
        keyword = parts[0].lower()
        args = parts[1:]

        if keyword == "exit":
            print_info("Goodbye!")
            sys.exit(0)

        if keyword not in commands:
            print_error(
                f"Unknown command: '{keyword}'. Type 'help' for options."
            )
            continue

        try:
            output = commands[keyword].execute(args, calculator, config)
            print_success(output)
        except CalculatorException as e:
            print_error(str(e))
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            logger.exception("Unexpected REPL error: %s", e)


if __name__ == "__main__":
    run_repl()  # pragma: no cover