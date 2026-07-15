from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import settings

engine=create_async_engine(settings.DATABASE_URL,connect_args={
        "statement_cache_size": 0,
    },
)   
session=async_sessionmaker(bind=engine,expire_on_commit=False)

Base=declarative_base()

async def get_db():
    db=session()
    try:
        yield db
    finally:
        await db.close()
