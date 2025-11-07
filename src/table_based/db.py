from sqlalchemy import create_engine
from src.common.config import settings
from urllib.parse import quote_plus  # NEW

def get_engine():
    # URL-encode the password so special chars like @, #, $, % won't break the URL
    safe_password = quote_plus(settings.DB_PASSWORD)
    conn_str = (
        f"mysql+pymysql://{settings.DB_USER}:{safe_password}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    engine = create_engine(conn_str, echo=False, future=True)
    return engine
