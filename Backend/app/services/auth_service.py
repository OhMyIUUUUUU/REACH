import uuid
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.activity import ActivityLog
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token

class AuthService:
    def register_user(self, db: Session, user_in: UserCreate) -> Token:
        # Check if email is already registered
        existing_email = db.query(User).filter(User.email == user_in.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists."
            )

        # Check if username is already taken
        existing_user = db.query(User).filter(User.username == user_in.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists."
            )

        # Create new user record
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            id=uuid.uuid4(),
            email=user_in.email,
            username=user_in.username,
            password_hash=hashed_password,
            role=user_in.role or "user",
            is_active=True
        )
        db.add(db_user)
        
        # Log registration activity
        log = ActivityLog(
            id=uuid.uuid4(),
            user_id=db_user.id,
            action="user_registered",
            details={"email": db_user.email, "username": db_user.username}
        )
        db.add(log)
        db.commit()
        db.refresh(db_user)

        # Generate access token
        token_data = {
            "sub": str(db_user.id),
            "email": db_user.email,
            "role": db_user.role
        }
        access_token = create_access_token(token_data)

        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(db_user)
        )

    def authenticate_user(self, db: Session, login_data: UserLogin) -> Token:
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated."
            )

        # Log login activity
        log = ActivityLog(
            id=uuid.uuid4(),
            user_id=user.id,
            action="user_login",
            details={"email": user.email}
        )
        db.add(log)
        db.commit()

        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
        access_token = create_access_token(token_data)

        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )

    def get_user_by_id(self, db: Session, user_id: str) -> Optional[User]:
        try:
            uid = uuid.UUID(user_id)
            return db.query(User).filter(User.id == uid).first()
        except ValueError:
            return None

auth_service = AuthService()
