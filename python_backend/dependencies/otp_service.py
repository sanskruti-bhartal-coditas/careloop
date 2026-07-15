import random
import redis
from fastapi import HTTPException, status
from config import settings
from dependencies.security import Authentication

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)

OTP_TTL_SECONDS = 300   

class OTPService:
    @staticmethod
    def generate_and_store(email: str):
        otp = str(random.randint(100000, 999999))
        print(otp)
        key = f"otp:{email}"
        redis_client.setex(key, OTP_TTL_SECONDS, Authentication.hash_password(otp))
        return otp

    @staticmethod
    def verify(email: str, otp: str) :
        key = f"otp:{email}"
        stored_hash = redis_client.get(key)

        if not stored_hash:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="OTP expired or not found. Please request a new one.",)

        if not Authentication.verify_password(otp, stored_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid OTP.",)
 
        redis_client.delete(key)
        return True