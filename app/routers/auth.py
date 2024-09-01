from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.dependencies.services import get_auth_service
from app.exceptions.auth_exceptions import UnauthorizedException
from app.schemas.token import TokenResponse
from app.services import auth_service as AuthService

# Create router instance
router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/token", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),  auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise UnauthorizedException(detail="Invalid credentials")
    # Generate access token
    access_token = auth_service.create_access_token(user, timedelta(minutes=15))
    # Return the token information
    return {"access_token": access_token, "token_type": "bearer"}