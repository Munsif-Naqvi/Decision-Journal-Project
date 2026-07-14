class EmailAlreadyExistsError(Exception):
    """Raised when attempting to register with an email that already exists."""


class ValidationError(Exception):
    """Raised when client input fails validation"""
    pass

class InvalidCredentialsError(Exception):
    """Raised when client enters invalid login credentials """
    pass

class UserDoesNotExistError(Exception):
    """Raised when attempting to access account that does not exist"""
    pass

class InvalidTokenError(Exception):
    """Raised when invalid JWT token is provided """
    pass

class DecisionDoesNotExistError(Exception):
    """Raised when attempting to access decision that does not exist"""
    pass

class DecisionAlreadyReviewedError(Exception):
    """Raised when attempting to update a reviewed decision"""
    pass