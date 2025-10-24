from collections.abc import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import Integer, String, UUID
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

import os 
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    nickname: Mapped[str] = mapped_column(String, nullable=False)


class Entry(Base):
    __tablename__ = "entry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[UUID] = mapped_column(UUID)
    account_email: Mapped[str] = mapped_column(String)
    account_name: Mapped[str] = mapped_column(String)
    score: Mapped[int] = mapped_column(Integer)
    problem: Mapped[str] = mapped_column(String)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_entry_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, Entry)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
