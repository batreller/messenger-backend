from typing import Generic, TypeVar

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ExceptionDetails(BaseModel):
    message: str
    code: str


AdditionalDetails = TypeVar('AdditionalDetails', bound=BaseModel)


class CustomException(Generic[AdditionalDetails], Exception):
    additional_details: AdditionalDetails | None

    def __init__(
        self,
        status_code : int,
        code: str,
        message: str,
        additional_details: AdditionalDetails | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self.details = ExceptionDetails(
            code=code,
            message=message
        )

        self.additional_details = additional_details
        self.headers = headers

        super().__init__()


async def custom_exceptions_handler(
    _: Request, 
    exc: CustomException
) -> JSONResponse:
    additional = dict()
    if exc.additional_details is not None:
        additional = exc.additional_details.dict()

    body = {
        "status_code": exc.status_code,
        "details": {
            **exc.details.dict(),
            **additional
        }
    }

    return JSONResponse(body, exc.status_code, exc.headers)
