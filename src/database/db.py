import contextlib
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from src.conf.config import config

print(config.DB_URL)

class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(autoflush=False, autocommit=False,
                                                                     bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self):
        """
        The session function is a context manager that provides a transactional scope around
        a series of operations. It will start a new transaction and commit all changes upon successful
        completion of the block, or rollback the transaction in case an exception occurs.
        The session function can be used as follows:
        
        :param self: Represent the instance of the class
        :return: A generator object
        :doc-author: Trelent
        """
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except:
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    async with sessionmanager.session() as session:
        return session
