class InvalidURLError(Exception):
    """
    Custom exception for invalid url
    """
    def __init__(self, value):
       self.value = value
    # __str__ display function
    def __str__(self):
       return(repr(self.value))


class NcbiAPIError(Exception):
    """
    Custom exception for NCBI API error
    """
    def __init__(self, value):
        self.value = value
    # __str__ display function
    def __str__(self):
        return(repr(self.value))