from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import Timestamp
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "")

Base = declarative_base()


class Post(Base, Timestamp):
    __tablename__ = "Post"
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(255))
    createdBy = Column(String(255))
    category = Column(String(255))