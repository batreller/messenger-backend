from typing import Generic, TypeVar

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class BaseExceptionDetails(BaseModel):
    message: str
    code: str


Details = TypeVar('Details', bound=BaseExceptionDetails)


class CustomException(Generic[Details], Exception):
    details: Details

    def __init__(
        self,
        status_code : int,
        details: Details,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self.details = details
        self.headers = headers

        super().__init__()


async def custom_exceptions_handler(
    _: Request, 
    exc: CustomException
) -> JSONResponse:
    body = {
        "status_code": exc.status_code,
        "details": exc.details.dict()
    }

    return JSONResponse(body, exc.status_code, exc.headers)
