class CalculatorException(Exception):
    pass

class OperationError(CalculatorException):
    pass

class ValidationError(CalculatorException):
    pass

class HistoryError(CalculatorException):
    pass

class ConfigurationError(CalculatorException):
    pass

class CommandError(CalculatorException):
    pass