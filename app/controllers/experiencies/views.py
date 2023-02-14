from fastapi.exceptions import HTTPException
from app.commands.experiencies.experiencies import SearchExperiencesCommand
from app.parsers.search_parser import SearchExperienceParser
from app.repositories.experience import PersistentExperienceRepository
from typing import List
from fastapi import Depends, status, APIRouter
from app.config.logger import setup_logger
from app.schemas.experience import (
    ExperienceCreateSchema,
    ExperienceSchema,
    SearchExperience,
)
from app.commands.experiencies import (
    CreateExperienceCommand,
    GetExperienceCommand,
)
from app.utils.error import GoExploreError


logger = setup_logger(name=__name__)
router = APIRouter()


@router.post(
    '/experiences',
    status_code=status.HTTP_201_CREATED,
    response_model=ExperienceSchema,
)
async def create_experience(experience_body: ExperienceCreateSchema):
    try:
        repository = PersistentExperienceRepository()
        experience = CreateExperienceCommand(repository, experience_body).execute()
        return experience
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )


@router.get(
    '/experiences/{id}',
    status_code=status.HTTP_200_OK,
    response_model=ExperienceSchema,
)
async def get_experience(id: str):
    try:
        repository = PersistentExperienceRepository()
        experience = GetExperienceCommand(repository, id).execute()
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )

    return experience


@router.get(
    '/experiences',
    status_code=status.HTTP_200_OK,
    response_model=List[ExperienceSchema],
)
async def search_experiences(params: SearchExperience = Depends()):
    try:
        search = SearchExperienceParser().parse(params)
        repository = PersistentExperienceRepository()
        experiences = SearchExperiencesCommand(repository, search).execute()
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )

    return experiences
