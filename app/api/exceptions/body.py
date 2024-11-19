from fastapi import HTTPException


class InvalidBodyAndQueryParamsException(HTTPException):
    def __init__(
        self, message="either json body or 'url' query parameter must be provided"
    ):
        super().__init__(status_code=400, detail=message)
