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
            ModelDBs = [self._get_or_create(session, ModelDB,
                                            AospyObj.models[m])
                        for m in AospyObj.models] # I think you should use the flag to track in db here.
            # Something along the lines of if AospyObj.models[m].track then add to the list.
            DBObj = self._get_or_create(session, ProjDB, AospyObj, **kwargs)
            DBObj.models = ModelDBs
        elif isinstance(AospyObj, Model):
            RunDBs = [self._get_or_create(session, RunDB, AospyObj.runs[r])
                      for r in AospyObj.runs]
            DBObj = self._get_or_create(session, ModelDB, AospyObj, **kwargs)
            DBObj.runs = RunDBs
        elif isinstance(AospyObj, Run):
            DBObj = self._get_or_create(session, RunDB, AospyObj, **kwargs)
        elif isinstance(AospyObj, Var):
            DBObj = self._get_or_create(session, VarDB, AospyObj, **kwargs)
        else:
            rn = self._get_or_create(session, RunDB, AospyObj.run[0])
            vr = self._get_or_create(session, VarDB, AospyObj.var)
            DBObj = self._get_or_create(session, CalcDB, AospyObj, **kwargs)
            DBObj.db_run = rn
            DBObj.db_var = vr
        session.commit()
        session.close()
        return DBObj

    def delete(self, AospyObj):
        pass

    def query(self):
        pass

    def _get_or_create(self, session, DBObj, AospyObj, **kwargs):
        """Returns the existing or new instance of an aospy DB object.

        Parameters
        ----------
        session : session
            Active SQLAlchemy database session
        DBObj : AospyDBEntry
            AospyDBEntry object to construct
        AospyObj : Proj, Model, Run, Var, or Calc
            Aospy object to find or store in database
        **kwargs
            Additional attributes to set within the database object for this
            particular aospy object (meant for setting attributes that are
            defined in the DB, but NOT in the AospyObj).

        Returns
        -------
        DBObj : AospyDBEntry
            The AospyDBEntry associated with the provided AospyObj
        """
        # Query for the existing object via overlapping parameters
        # and kwargs
        params = self._query_params(AospyObj, DBObj)
        filter_params = self._merge_two_dicts(params, kwargs)
        instance = session.query(DBObj).filter_by(**filter_params).first()
        if instance:
            return instance
        else:
            instance = DBObj(AospyObj, **kwargs)
            session.add(instance)
            return instance

    @staticmethod
    def _merge_two_dicts(x, y):
        """From SO 38987"""
        z = x.copy()
        z.update(y)
        return z

    def _query_params(self, AospyObj, DBObj):
        return dict((attr, value) for attr, value in
                    AospyObj.__dict__.iteritems()
                    if (hasattr(DBObj, attr) and
                        (attr not in ['projects', 'models',
                                      'runs', 'calculations', 'variables'])))
