import os
from sqlalchemy import MetaData,create_engine
from databases import Database
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
server = os.getenv("MYSQL_HOST")
db = os.getenv("MYSQL_DATABASE")
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{server}/{db}"

database = Database(DATABASE_URL)
metadata = MetaData()