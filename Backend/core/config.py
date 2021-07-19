import os
import smtplib
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USERNAME")
    POSTGRES_PASS: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "job_board_db")
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


    SECRET_KEY: str = os.getenv("SECRET_KEY")
    TOKEN_ALGORITHM = 'HS256'
    REGISTRATION_TOKEN_LIFETIME = 60 * 60
    USER_TOKEN_LIFETIME = 30 * 60


    
    EMAIL_HOST = ('smtp.gmail.com', 587)
    SSL = True
    EMAIL_HOST_USER ='zeroxlearner@gmail.com'
    EMAIL_HOST_PASSWORD = 'z3rox_Learner'

    
settings = Settings()