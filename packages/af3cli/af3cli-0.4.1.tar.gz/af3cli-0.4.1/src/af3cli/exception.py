class AFMissingFieldError(Exception):
    """
    Custom exception raised when a required field is missing.
    """
    pass


class AFSequenceError(Exception):
    """
        Represents a custom exception for sequence-related errors.
    """
    pass


class AFTemplateError(Exception):
    """
    Represents a custom exception for template-related errors.
    """
    pass


class AFModificationError(Exception):
    """
    Represents a custom exception for modification-related errors.
    """
    pass


class AFMSAError(Exception):
    """
    Represents a custom exception for MSA-related errors.
    """
    pass
