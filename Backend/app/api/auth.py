from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import auth_service
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> Token:
    """Registers a new user and returns a signed JWT access token."""
    return auth_service.register_user(db=db, user_in=user_in)

@router.post(
    "/login",
    response_model=Token,
    summary="User login with email and password"
)
def login(login_data: UserLogin, db: Session = Depends(get_db)) -> Token:
    """Authenticates credentials and returns a signed JWT access token."""
    return auth_service.authenticate_user(db=db, login_data=login_data)

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user profile"
)
def get_me(current_user: User = Depends(get_current_active_user)) -> UserResponse:
    """Retrieves profile details for the currently authenticated user."""
    return UserResponse.model_validate(current_user)
