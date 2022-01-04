class AdminPrivilegesException(Exception):
    """Exception raised for admin privileges errors.

    Attributes:
        value -- returned value which raise the error
        message -- explanation of the error
    """

    def __init__(self, value, message):
        self.value = value
        self.message = message
        super().__init__(self.message)
