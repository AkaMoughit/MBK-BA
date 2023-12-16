from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


URL_DATABASE = 'mysql://doadmin:AVNS_IiPgoKqeMWGoDx4J2q1@mbk-db-do-user-14057762-0.c.db.ondigitalocean.com:25060/defaultdb?ssl-mode='

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()