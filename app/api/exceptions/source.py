from fastapi import HTTPException


class SourceNotFoundException(HTTPException):
    def __init__(self, message="source not found"):
        super().__init__(status_code=404, detail=message)


class SourceAlreadyExistsException(HTTPException):
    def __init__(self, message="source already exists"):
        super().__init__(status_code=400, detail=message)
