from fastapi import status
from starlette.types import Message

statuses = {status.HTTP_200_OK: {"model": Message},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message}}
