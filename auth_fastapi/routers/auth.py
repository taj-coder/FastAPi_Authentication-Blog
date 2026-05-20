import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models
from utils import verify_password

router = APIRouter(
    tags=["Authentication Dashboard"]
)

# --- TOKEN CONFIGURATION KEYS ---
SECRET_KEY = "SUPER_SECRET_SIGNING_KEY_CHANGE_THIS_LATER" # openssl rand -hex 32 or python -c "import secrets; print(secrets.token_hex(32))" manual secret key generating 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    """Generates a secure JWT token with an expiration timestamp."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# OAuth2PasswordRequestForm requires form-data fields: 'username' and 'password'
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Look up user by their email or username
    user = db.query(models.DBUser).filter(
        (models.DBUser.username == form_data.username) | (models.DBUser.email == form_data.username)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
        
    # Verify the plain text password matches the hashed database version
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
        
    # Generate the JWT Token token payload
    access_token = create_access_token(data={"user_id": user.id, "sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi.security import OAuth2PasswordBearer #right side lock 
# Point this to our login path so Swagger UI knows where to authenticate
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Decodes the incoming token to fetch and return the active User object."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = db.query(models.DBUser).filter(models.DBUser.id == user_id).first()
    if user is None:
        raise credentials_exception
        
    return user
