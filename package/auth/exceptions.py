from fastapi import status

from package.exceptions.CustomException import BaseExceptionDetails, CustomException

credentials_exception = CustomException[BaseExceptionDetails](
    status_code=status.HTTP_401_UNAUTHORIZED,
    details=BaseExceptionDetails(
        message="Could not validate credentials",
        code="NOT_AUHORIZED"
    ),
    headers={"WWW-Authenticate": "Bearer"},
)
