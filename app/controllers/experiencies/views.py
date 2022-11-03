from fastapi.exceptions import HTTPException
from app.repositories.experience import PersistentExperienceRepository
from fastapi import status, APIRouter
from app.config.logger import setup_logger
from app.schemas.experience import ExperienceCreateSchema, ExperienceSchema
from app.commands.experiencies import (
    CreateExperienceCommand,
    GetExperienceCommand,
    ExperienceAlreadyExistsError,
    ExperienceNotFoundError,
)


logger = setup_logger(name=__name__)
router = APIRouter()


@router.post(
    '/experiencies',
    status_code=status.HTTP_201_CREATED,
    response_model=ExperienceSchema,
)
async def create_experience(experience_body: ExperienceCreateSchema):
    try:
        repository = PersistentExperienceRepository()
        experience = CreateExperienceCommand(repository, experience_body).execute()
        return experience
    except ExperienceAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )


#
#
# @router.get(
#    '/users/{id}',
#    status_code=status.HTTP_200_OK,
#    response_model=UserSchema
# )
# async def get_user(id: str):
#    try:
#        repository = PersistentUserRepository()
#        user = GetUserCommand(repository, id).execute()
#    except UserNotFoundError as e:
#        raise HTTPException(
#            status_code=status.HTTP_404_NOT_FOUND,
#            detail=str(e)
#        )
#    except Exception as e:
#        logger.error(e)
#        raise HTTPException(
#            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#            detail="Internal Error"
#        )
#
#    return user
#
