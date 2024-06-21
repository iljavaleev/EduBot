import os
from typing import Self

from dotenv import load_dotenv
from sqlalchemy import URL, select
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from utils.utils import logs

load_dotenv()


def get_engine():
    return create_async_engine(
        URL.create(
            drivername='postgresql+asyncpg',
            username=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host='db',
            port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB')
        )
    )


class Base(AsyncAttrs, DeclarativeBase):

    @classmethod
    @logs
    async def get_custom_query(cls, query):
        async with AsyncSession(
                get_engine(),
                expire_on_commit=False
        ) as session:
            res = await session.execute(query)
            return res

    @classmethod
    @logs
    async def get(cls, **kwargs) -> Self | None:
        async with AsyncSession(
                get_engine(),
                expire_on_commit=False
        ) as session:
            instance = await session.execute(select(cls).filter_by(**kwargs))
            return instance.scalar()

    @classmethod
    @logs
    async def get_all(
            cls,
            stmt=None,
            **kwargs
    ) -> list[Self] | None:
        async with AsyncSession(
                get_engine(),
                expire_on_commit=False
        ) as session:
            if stmt is not None:
                instances = await session.execute(stmt)
            else:
                instances = await session.execute(
                    select(cls).filter_by(**kwargs)
                )
            return instances.scalars().all()  # type: ignore

    @logs
    async def save(self):
        async with AsyncSession(get_engine(), expire_on_commit=False) \
                as session:
            session.add(self)
            await session.commit()
            await session.refresh(self)
            return self

    @logs
    async def update(self, **kwargs):
        if self.id:
            for key, value in kwargs.items():
                setattr(self, key, value)
            return await self.save()

    @logs
    async def destroy(self):
        async with AsyncSession(
                get_engine(),
                expire_on_commit=False
        ) as session:
            await session.delete(self)
            return await session.commit()

    @classmethod
    @logs
    async def create(cls, **kwargs) -> Self:
        instance = cls(**kwargs)  # type: ignore
        return await instance.save()

    @classmethod
    @logs
    async def get_or_create(cls, **kwargs) -> tuple[Self, bool]:
        instance = await cls.get(**kwargs)
        if instance is None:
            instance = await cls.create(**kwargs)
            return instance, True
        return instance, False
