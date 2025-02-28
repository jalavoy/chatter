import datetime
import asyncio
from sqlalchemy import Column, String, DateTime, Text, Integer, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///chatter.db"

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

    async def save(self, session):
        self.updated_at = datetime.datetime.now()
        session.add(self)
        await session.commit()


class Config(BaseModel):
    __tablename__ = "config"
    id = Column(Integer, primary_key=True, index=True)
    config_name = Column(String)
    config_value = Column(String)


class Prompt(BaseModel):
    __tablename__ = "prompt"
    id = Column(Integer, primary_key=True, index=True)
    prompt_name = Column(String)
    prompt_text = Column(Text)


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_models())


class ConfigRepository:
    async def get_config_by_name(config_name: str):
        async with async_session() as session:
            q = select(Config).where(Config.config_name == config_name)
            response = await session.execute(q)
            result = response.first()
            if result:
                return result[0].config_value
            return None


class PromptRepository:
    async def get_prompt_by_name(prompt_name: str):
        async with async_session() as session:
            q = select(Prompt).where(Prompt.prompt_name == prompt_name)
            response = await session.execute(q)
            result = response.first()
            if result:
                return result[0].prompt_text
            return None
