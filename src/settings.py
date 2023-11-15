from os import getenv

API_PORT = getenv("API_PORT") or 80
ENV = getenv("ENV") or "development"
DB_URL = (
    getenv("DB_URL")
    or f"postgresql+psycopg2://postgres:postgres@localhost:15432/hotel_{ENV}"
)
IS_DEBUG = bool(int(getenv("IS_DEBUG", "0"))) or True
