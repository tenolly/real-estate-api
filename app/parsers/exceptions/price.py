from .parser import ParserException


class PriceNotFoundException(ParserException):
    def __init__(self, *args):
        super().__init__(*args)
