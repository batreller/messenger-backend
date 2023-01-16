import typing
from typing import Generic, Self, TypeVar

from pydantic import BaseModel, Field

from package.exceptions.CustomException import BaseExceptionDetails, CustomException

BodyFields = TypeVar('BodyFields', bound=BaseModel)


class ExceptionDetails(Generic[BodyFields], BaseExceptionDetails):
    errors: BodyFields | None = Field(default=None)


class InvalidDataException(Generic[BodyFields], CustomException[ExceptionDetails]):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        field_error_mapping: BodyFields | None = None
    ) -> None:
        if isinstance(field_error_mapping, BaseModel):
            field_error_mapping = field_error_mapping

        self.details = ExceptionDetails(
            code=code,
            message=message,
            errors=field_error_mapping
        )

        super().__init__(status_code, self.details)



    def populate_errors_with_message(self) -> Self:
        mapping_object_class: BaseModel = self.__orig_class__.__args__[0] # type: ignore
        fields = mapping_object_class.__fields__
        errors_mapping = {}
        for key, field in fields.items():
            if not field.required and field.default is None:
                continue

            errors_mapping[key] = self.details.message

        self.details.errors = typing.cast(BodyFields, errors_mapping)

        return self
