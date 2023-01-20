from fastapi import status

from package.exceptions.InvalidData.InvalidDataException import InvalidDataException
from package.routes.user.inputs.BioInput import BioInput

# TODO: Use the validation on the pydantic model to avoid something like this.
INVALID_BIO_MESSAGE = "Bio is too long"


invalid_bio = InvalidDataException[BioInput](
    status_code=status.HTTP_400_BAD_REQUEST,
    code="INVALID_BIO",
    message=INVALID_BIO_MESSAGE
).populate_errors_with_message()
