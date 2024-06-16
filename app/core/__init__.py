from app.core.config import AuthJWT, DatabaseFactory
from app.core.settings import Setting

settings = Setting()
auth_jwt = AuthJWT()
db_factory = DatabaseFactory(settings.db_url)
