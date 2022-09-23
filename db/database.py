from os import environ
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv('db/.env')
SQLALCHEMY_DATABASE_URL = environ.get('DB_CONNECTION')+'://'+environ.get('DB_USERNAME')+':'+environ.get('DB_PASSWORD')+'@'+environ.get('DB_HOST')+':'+environ.get('DB_PORT')+'/'+environ.get('DB_DATABASE')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()