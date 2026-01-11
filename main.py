from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets

app = FastAPI(title="Cloud API", version="1.0.0", description="RESTful API with Authentication")

# Security Configuration
SECRET_KEY = secrets.token_urlsafe(32)  # Generate a random secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# In-memory user storage (replace with database in production)
users_db = {}

# Pydantic Models
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Helper Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(username: str) -> Optional[UserInDB]:
    """Get user from database"""
    if username in users_db:
        user_dict = users_db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user with username and password"""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return User(username=user.username, email=user.email, full_name=user.full_name)

# API Endpoints

@app.get("/")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "cloud-api",
        "version": "2.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/info")
def get_info():
    """API information endpoint"""
    return {
        "name": "Cloud API Microservice",
        "version": "1.0.0",
        "endpoints": ["/", "/info", "/docs", "/register", "/login", "/me"]
    }

@app.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister):
    """Register a new user"""
    # Check if username already exists
    if user_data.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    for existing_user in users_db.values():
        if existing_user.get("email") == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user_dict = {
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "hashed_password": hashed_password
    }
    users_db[user_data.username] = user_dict
    
    return User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name
    )

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint - returns JWT access token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return current_user