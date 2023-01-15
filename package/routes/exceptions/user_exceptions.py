from fastapi import HTTPException, status

user_exists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": "USER_EXISTS",
        "message": "This user already exists."
    }
)

wrong_credentials = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": "WRONG_CREDENTIALS",
        "message": "Wrong login credential, try again."
    }
)
