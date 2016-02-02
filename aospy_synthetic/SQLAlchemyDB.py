from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import ClauseElement

from aospy_synthetic.proj import Proj
from aospy_synthetic.model import Model
from aospy_synthetic.run import Run
from aospy_synthetic.var import Var
from aospy_synthetic.calc import Calc
from abstract_db import AbstractBackend
from sqlite_config import ProjDB, ModelDB, RunDB, VarDB, CalcDB


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

    def add(self, AospyObj, **kwargs):
        """Adds an aospy object to the database.
        Implement __init__ in sqlite_config to add
        **kwargs as additional parameter settings.  This is a good workaround
        for issues pertaining to Calc not being one to one in the DB.
        """
        engine = create_engine(self.DB_PATH)
        Session = sessionmaker(bind=engine)
        session = Session()
        if isinstance(AospyObj, Proj):
            ModelDBs = [self._query(session, AospyObj.models[m])
                        for m in AospyObj.models] # I think you should use the flag to track in db here.
            # Something along the lines of if AospyObj.models[m].track then add to the list.
            DBObj = self._get_or_create(session, ProjDB, AospyObj, **kwargs)
            DBObj.models = ModelDBs
        elif isinstance(AospyObj, Model):
            RunDBs = [self._query(session, AospyObj.runs[r])
                      for r in AospyObj.runs]
            DBObj = self._get_or_create(session, ModelDB, AospyObj, **kwargs)
            DBObj.runs = RunDBs
        elif isinstance(AospyObj, Run):
            DBObj = self._get_or_create(session, RunDB, AospyObj, **kwargs)
        elif isinstance(AospyObj, Var):
            DBObj = self._get_or_create(session, VarDB, AospyObj, **kwargs)
        else:
            DBObj = self._get_or_create(session, CalcDB, AospyObj, **kwargs)
        session.commit()
        session.close()
        return DBObj

    def delete(self, AospyObj):
        pass

    def query(self):
        pass

    def _query(self, session, AospyObj):
        if isinstance(AospyObj, Proj):
            params = self._query_params(AospyObj, ProjDB)
            return self._get_or_create(session, ProjDB, AospyObj, **params)
        elif isinstance(AospyObj, Model):
            params = self._query_params(AospyObj, ModelDB)
            return self._get_or_create(session, ModelDB, AospyObj, **params)
        elif isinstance(AospyObj, Run):
            params = self._query_params(AospyObj, RunDB)
            return self._get_or_create(session, RunDB, AospyObj, **params)
        elif isinstance(AospyObj, Var):
            params = self._query_params(AospyObj, VarDB)
            return self._get_or_create(session, VarDB, AospyObj, **params)
        else:
            params = self._query_params(AospyObj, CalcDB)
            return self._get_or_create(session, CalcDB, AospyObj, **params)

    def _get_or_create(self, session, DBObj, AospyObj, **kwargs):
        instance = session.query(DBObj).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = DBObj(AospyObj)
            session.add(instance)
            return instance

    def _query_params(self, AospyObj, DBObj):
        return dict((attr, value) for attr, value in
                    AospyObj.__dict__.iteritems()
                    if (hasattr(DBObj, attr) and
                        (attr not in ['runs', 'models', 'projects', 'calcs'])))
