# data_access/db_context.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BusinessObject.models import Base

class DBContext:
    def __init__(self, db_url="mssql+pyodbc://@DESKTOP-PEG8VKH/CarPark?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def ensure_schema(self):
        Base.metadata.create_all(self.engine)