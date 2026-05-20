from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import models
from database import get_db
from utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users Operations"]
)

# --- USER VALIDATION SCHEMAS ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr  
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

# --- USER ENDPOINTS ---

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists 
    existing_user = db.query(models.DBUser).filter(
        (models.DBUser.email == user.email) | (models.DBUser.username == user.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or Email already registered."
        )

    # Hash the plain text password safely
    encrypted_password = hash_password(user.password)

    # Save the new user record
    new_user = models.DBUser(
        username=user.username,
        email=user.email,
        hashed_password=encrypted_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
