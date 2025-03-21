"""Module providing RESTObject class"""

from .basic_auth import BasicAuth


class RESTObject(object):
    """
    Generic REST config class, provides standardised properties
    for generating a requests call 
    """

    operation: str
    endpoint: str
    params: dict
    headers: dict
    payload: str
    basic_auth: BasicAuth
    error_status: list[int]

    def __init__(self, **kwargs) -> None:
        self.operation = 'get'
        self.params = {}
        self.payload = ''
        self.headers = {}
        self.basic_auth = None
        self.error_status = [403, 404, ]
        self.__dict__.update(kwargs)
