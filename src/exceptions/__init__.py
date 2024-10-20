from fastapi import status


class BusinessException(Exception):
    def __init__(self, message: str, status_code: status):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return self.message


class UserDoesNotExist(BusinessException):
    def __init__(self, message="User does not exist."):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class ProductDoesNotExist(BusinessException):
    def __init__(self, message="Product does not exist."):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class AdvertisingDoesNotExist(BusinessException):
    def __init__(self, message="Advertising does not exist."):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class TransactionDoesNotExist(BusinessException):
    def __init__(self, message="Transaction does not exist."):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class OrderDoesNotExist(BusinessException):
    def __init__(self, message="Order does not exist."):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

