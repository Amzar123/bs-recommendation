class Response:
    """
    Represents a response object.

    Attributes:
        message (str): A message associated with the response.
        data (any): Additional data associated with the response.
        code (int): A code associated with the response.
    """

    def __init__(self, message=None, data=None, code=None):
        self.message = message
        self.data = data
        self.code = code

    def to_dict(self):
        """
        Converts the response object to a dictionary.

        Returns:
            dict: A dictionary representation of the response object.
        """
        return {
            'code': self.code,
            'message': self.message,
            'data': self.data
        }
