from fastapi import APIRouter, Depends
from wdq.app.schemas.user import User, UserCreate
from wdq.app.db.database import AsyncSession, get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Placeholder for user creation logic
    return {"id": 1, "username": user.username}