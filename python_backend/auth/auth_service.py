from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.security import Authentication
from auth.auth_repo import UserRepository
from dependencies.otp_service import OTPService
from dependencies.email_service import email_service


class AuthService:
    @staticmethod
    async def login(db: AsyncSession, email: str):
        user = await UserRepository.get_user_by_email(db, email)
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found or inactive",)
        otp = OTPService.generate_and_store(email)

        email_service.send_invite(
            to_email=email,
            token=otp,
            subject="Your login OTP",
            message=f"Your OTP is <strong>{otp}</strong>. It expires in 5 minutes.")

        return {"message": "OTP sent successfully"}

    @staticmethod
    async def verify_otp(db: AsyncSession, email: str, otp: str) :
        user = await UserRepository.get_by_email(db, email) 
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found or inactive",)
        OTPService.verify(email, otp)
        token_data = {"sub": str(user.id),"role":user.role_name}
        return {
            "access_token": Authentication.create_access_token(token_data),
            "refresh_token": Authentication.create_refresh_token(token_data),
            "token_type": "bearer"}

