class Response():
    endpoint: str
    error: bool
    error_text: str
    response: str
    status: int
    outbound: str

    def __init__(self, endpoint, error=False, error_text='', response='', status=0, outbound='') -> None:
        self.endpoint = endpoint
        self.error = error
        self.error_text = error_text
        self.response = response
        self.status = status
        self.outbound = outbound

    def __str__(self) -> str:
        return f"Response: {self.endpoint} Status: {self.status}"

    def __repr__(self) -> str:
        return f"Response({self.endpoint}, {self.status}, {self.error}, {self.response})"
