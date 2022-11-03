from fastapi.exceptions import HTTPException
from app.repositories.users import PersistentUserRepository
from fastapi import status, APIRouter
from app.config.logger import setup_logger
from app.schemas.users import UserCreateSchema, UserSchema
from app.commands.users import CreateUserCommand, GetUserCommand
from app.utils.error import GoExploreError


logger = setup_logger(name=__name__)
router = APIRouter()


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user(user_body: UserCreateSchema):
    try:
        repository = PersistentUserRepository()
        user = CreateUserCommand(repository, user_body).execute()
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )
    return user


@router.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user(id: str):
    try:
        repository = PersistentUserRepository()
        user = GetUserCommand(repository, id).execute()
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )

    return user
