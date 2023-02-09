from fastapi.exceptions import HTTPException
from app.repositories.users import PersistentUserRepository
from fastapi import status, APIRouter
from app.config.logger import setup_logger
from app.schemas.sessions import SessionCreateSchema, SessionSchema
from app.commands.sessions import CreateSessionCommand
from app.utils.error import GoExploreError


logger = setup_logger(name=__name__)
router = APIRouter()


@router.post('/session', status_code=status.HTTP_200_OK, response_model=SessionSchema)
async def create_session(session_body: SessionCreateSchema):
    try:
        repository = PersistentUserRepository()
        session = CreateSessionCommand(repository, session_body).execute()
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )
    return session
