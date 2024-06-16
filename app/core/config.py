from pathlib import Path

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR.joinpath("jwt-private.pem")
    public_key_path: Path = BASE_DIR.joinpath("jwt-public.pem")
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 2 * 60


class DatabaseFactory:
    def __init__(
        self,
        db_url: str,
        db_echo: bool = False,
    ):
        self.engine = create_async_engine(
            url=db_url,
            echo=db_echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_depends(self):
        async with self.session_factory() as session:
            yield session


# class RedisFactory:
#     def __init__(self, host, port, prefix):
#         self.host = host
#         self.port = port
#         self.prefix = prefix
#         self.r = aioredis.from_url(f"redis://{host}:{port}", decode_responses=True)
#
#     def engine(self):
#         return self.r
#
#
# redis_factory = RedisFactory(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     prefix=settings.REDIS_PREFIX,
# )
#
# redis_engine = redis_factory.engine()
