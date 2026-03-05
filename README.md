# Advanced Calculator Application

A feature-rich command-line calculator built with Python, implementing multiple
design patterns and professional software engineering practices.

## Features

- 10 arithmetic operations: add, subtract, multiply, divide, power, root,
  modulus, int_divide, percent, abs_diff
- Undo/Redo functionality via the Memento Pattern
- Auto-save and logging via the Observer Pattern
- Dynamic help menu via the Decorator Pattern
- Command encapsulation via the Command Pattern
- Color-coded output via Colorama
- CSV history persistence via Pandas
- 98% test coverage with 131 tests

## Design Patterns Used

| Pattern | Location | Purpose |
|---|---|---|
| Factory | `OperationFactory` | Creates operation instances by name |
| Decorator | `@register_operation` | Auto-registers operations and builds help menu |
| Memento | `CalcMemento` + `History` | Undo/redo snapshots |
| Observer | `LoggingObserver`, `AutoSaveObserver` | React to calculations |
| Command | `ReplCommand` subclasses | Encapsulate REPL actions |

## Project Structure
```
calculator-app/
├── app/
│   ├── __init__.py
│   ├── calculator.py          # Central orchestrator
│   ├── calculation.py         # Immutable calculation record
│   ├── calculator_config.py   # Configuration via .env
│   ├── calculator_memento.py  # Memento Pattern snapshots
│   ├── commands.py            # Command Pattern REPL commands
│   ├── exceptions.py          # Custom exception hierarchy
│   ├── history.py             # History with undo/redo
│   ├── input_validators.py    # Input validation
│   ├── logger.py              # Centralized logging
│   ├── observers.py           # Observer Pattern implementations
│   └── operations.py          # Operations with Factory + Decorator
├── tests/
│   ├── test_calculation.py
│   ├── test_calculator.py
│   ├── test_commands.py
│   ├── test_history.py
│   ├── test_memento.py
│   ├── test_observers.py
│   ├── test_operations.py
│   └── test_validators.py
├── .env
├── .github/
│   └── workflows/
│       └── python-app.yml
├── main.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/niharika2701/calculator-final
cd calculator-final
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment

Create a `.env` file in the project root:
```
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1e15
CALCULATOR_DEFAULT_ENCODING=utf-8
CALCULATOR_LOG_FILE=logs/calculator.log
CALCULATOR_HISTORY_FILE=history/calculator_history.csv
```

## Usage

### Start the REPL
```bash
python main.py
```

### Available Commands

#### Arithmetic Operations
```
calc> add 3 5           → 8
calc> subtract 10 3     → 7
calc> multiply 4 5      → 20
calc> divide 10 2       → 5
calc> power 2 8         → 256
calc> root 27 3         → 3.0
calc> modulus 10 3      → 1
calc> int_divide 10 3   → 3
calc> percent 50 200    → 25.0
calc> abs_diff 5 3      → 2
```

#### History Management
```
calc> history           # Display all calculations
calc> clear             # Clear all history
calc> undo              # Undo last calculation
calc> redo              # Redo last undone calculation
```

#### Persistence
```
calc> save              # Save history to CSV
calc> load              # Load history from CSV
```

#### Other
```
calc> help              # Show all commands
calc> exit              # Exit the application
```

## Configuration

All settings are managed via the `.env` file:

| Variable | Default | Description |
|---|---|---|
| `CALCULATOR_LOG_DIR` | `logs` | Directory for log files |
| `CALCULATOR_HISTORY_DIR` | `history` | Directory for history files |
| `CALCULATOR_MAX_HISTORY_SIZE` | `100` | Maximum history entries |
| `CALCULATOR_AUTO_SAVE` | `true` | Auto-save after each calculation |
| `CALCULATOR_PRECISION` | `10` | Decimal places in results |
| `CALCULATOR_MAX_INPUT_VALUE` | `1e15` | Maximum allowed input value |
| `CALCULATOR_DEFAULT_ENCODING` | `utf-8` | File encoding |
| `CALCULATOR_LOG_FILE` | `logs/calculator.log` | Log file path |
| `CALCULATOR_HISTORY_FILE` | `history/calculator_history.csv` | History CSV path |

## Testing

### Run all tests
```bash
python -m pytest --cov=app --cov-report=term-missing -v
```

### Run a specific test file
```bash
python -m pytest tests/test_calculator.py -v
```

### Check coverage only
```bash
python -m pytest --cov=app --cov-fail-under=90
```

Current coverage: **98%** across 131 tests.

## CI/CD

GitHub Actions automatically runs on every push and pull request to `main`:

- Sets up Python 3.11
- Installs all dependencies
- Creates `.env` for CI environment
- Runs all tests with coverage
- Fails the build if coverage drops below 90%

See `.github/workflows/python-app.yml` for the full workflow configuration.

## Logging

Logs are written to `logs/calculator.log`. Each calculation is recorded with:
```
2024-01-15 10:23:45 | INFO     | CALCULATION | op=add | a=3 | b=5 | result=8
```

Log levels:
- `INFO` — all calculations and normal events
- `WARNING` — recoverable issues
- `ERROR` — failures requiring attention