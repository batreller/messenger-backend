from fastapi import status

from package.exceptions.CustomException import CustomException

credentials_exception = CustomException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    message="Could not validate credentials",
    code="NOT_AUHORIZED",
    headers={"WWW-Authenticate": "Bearer"}
)
