import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
server = os.getenv("MYSQL_HOST")
db = os.getenv("MYSQL_DATABASE")
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{server}/{db}"

# echo=Trueは開発用。本番はFalse
engine = create_engine(DATABASE_URL, echo=True)
# sessionmakerは同期式。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependの引数にするには関数型で渡す。インスタンスはエラーになる。
def get_pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")
