from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Thiết lập cơ sở dữ liêu

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/users_database"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
