class EmailAlreadyExistsError(Exception):
    """Raised when attempting to register with an email that already exists."""


class ValidationError(Exception):
    """Raised when client input fails validation"""
    pass