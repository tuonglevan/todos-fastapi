from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_config
from app.core.db import get_async_db_session
from app.exceptions.auth_exceptions import UnauthorizedException
from app.schemas.token import TokenResponse
from app.services import auth as AuthService

# Create router instance
router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/token", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_db_session)):
    user = await AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise UnauthorizedException(detail="Invalid credentials")
    # Generate access token
    access_token = AuthService.create_access_token(user, timedelta(minutes=15))
    # Return the token information
    return {"access_token": access_token, "token_type": "bearer"}