from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aospy_synthetic.abstract_db import AbstractBackend
from sqlite_config import ProjDB, ModelDB, RunDB, VarDB, CalcDB, RegDB


class SQLBackend(AbstractBackend):
    """Implements AbstractBackend methods"""

    def __init__(self, db_path='pass'):
        """Initializes a sqlite database using SQLAlchemy.

        Parameters
        ----------
        db_path : str
            path to the database

        Returns
        -------
        db : SQLAlchemyDB
            backend for use in aospy
        """
        self.DB_PATH = 'sqlite:///test.db'

    def db_obj_from_aospy(self, AospyObj):
        mapping = {
            'Proj': ProjDB,
            'Model': ModelDB,
            'Run': RunDB,
            'Calc': CalcDB,
            'Var': VarDB,
            'Reg': RegDB
        }
        return mapping[AospyObj.__class__.__name__]

    def add(self, AospyObj):
        """Adds an aospy object to the database.
        """
        engine = create_engine(self.DB_PATH, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        db_obj = self.db_obj_from_aospy(AospyObj).as_unique(session, AospyObj)
        session.add(db_obj)
        session.commit()
        session.close()

    def delete():
        raise

    def query():
        raise
