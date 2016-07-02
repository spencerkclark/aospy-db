from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from aospy_synthetic.db.abstract_db import AbstractBackend
from sqlalchemy_config import (initialize_db,
                               ProjDB, ModelDB, RunDB,
                               VarDB, CalcDB, RegionDB)


class SQLAlchemyDB(AbstractBackend):
    """Implements AbstractBackend methods"""

    def __init__(self, db_path='sqlite:///test.db'):
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
        self.DB_PATH = db_path
        self.engine = create_engine(self.DB_PATH, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        initialize_db(self.DB_PATH)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _db_cls_from_aospy_cls(self, AospyObj):
        mapping = {
            'Proj': ProjDB,
            'Model': ModelDB,
            'Run': RunDB,
            'Calc': CalcDB,
            'Var': VarDB,
            'Region': RegionDB
        }
        return mapping[AospyObj.__class__.__name__]

    def add(self, AospyObj):
        """Adds an aospy object to the database.
        """
        with self.session_scope() as session:
            db_obj = self._db_cls_from_aospy_cls(AospyObj).as_unique(session,
                                                                     AospyObj)
            session.add(db_obj)

    def delete():
        raise

    def query():
        raise
