from sqlalchemy.ext.asyncio import AsyncSession
from auth.auth_service import AuthService
from fastapi import Depends,APIRouter,Form
from dependencies.session import get_db
from dependencies.deps import get_current_user
from auth.auth_schema import UserOut,OTPVerifyRequest

router=APIRouter(prefix='/auth',tags=["Auth"])

@router.post("/login")
async def login(email, db: AsyncSession = Depends(get_db)):
    return await AuthService.login(email,db)


@router.post('/otp/verify')
async def verify_otp(data:OTPVerifyRequest,db:AsyncSession=Depends(get_db)):
    return await AuthService.verify_otp(db,email=data.email,otp=data.otp)

@router.post("/refresh")
async def refresh(payload, db: AsyncSession = Depends(get_db)):
    return await AuthService.refresh_tokens(db, refresh_token=payload.refresh_token)

@router.get("/me", response_model=UserOut)
async def get_me(current_user=Depends(get_current_user)):
    return current_user