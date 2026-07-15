from models.user_model import Users
from sqlalchemy import select
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from auth.auth_schema import CreateUser
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    @staticmethod
    async def register_user(user:CreateUser,db:AsyncSession):
        try:
            user=Users(first_name=user.first_name,last_name=user.last_name,email=user.email)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user 
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def get_user_by_email(email:str,db:AsyncSession):
        try:
            result=await db.execute(select(Users).where(Users.email==email))
            return result.scalars().one_or_none()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_all_user(db:AsyncSession):
        try:
            result=await db.execute(select(Users))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
    