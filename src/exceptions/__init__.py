from fastapi import status
from typing import List


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


class InvalidTransaction(BusinessException):
    def __init__(
        self, message="Invalid transaction. Buyer and Seller must be different"
    ):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


class OrderDoesNotExist(BusinessException):
    def __init__(self, message="Order does not exist."):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class InvalidImageType(BusinessException):
    def __init__(self, content_type: str, ALLOWED_IMAGE_TYPES: List[str]):
        message = f"Invalid image type. Type: {content_type}. Valid Types: {', '.join(ALLOWED_IMAGE_TYPES)}"
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


class FileTooBig(BusinessException):
    def __init__(self, message="File too big. File size must be under 5MB"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


class FileNotExists(BusinessException):
    def __init__(self, file_uri: str):
        message = f"File URI doesn't match or exists. URI = {file_uri}"
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)
