from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from ..abstract_db import AbstractBackend
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
    def _session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def _db_cls_from_aospy_cls(AospyObj):
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
        if AospyObj.track():
            with self._session_scope() as session:
                db_obj = self._db_cls_from_aospy_cls(AospyObj).as_unique(
                    session,
                    AospyObj
                )
                session.add(db_obj)
        else:
            raise RuntimeError('aospy object not set to be tracked in DB')

    def delete(self, AospyObj):
        """Deletes an aospy object from the database if it exists"""
        with self._session_scope() as session:
            q = session.query(self._db_cls_from_aospy_cls(AospyObj))
            db_obj = q.filter_by(hash=hash(AospyObj)).first()
            if db_obj:
                session.delete(db_obj)

    def query():
        raise NotImplementedError()

    @classmethod
    def _get_db_obj_query(cls, session, AospyObj):
        db_cls = cls._db_cls_from_aospy_cls(AospyObj)
        q = session.query(db_cls)
        return q.filter_by(hash=hash(AospyObj))

    # Define hidden testing methods
    def _assertNoDuplicates(self, *AospyObjs):
        with self._session_scope() as session:
            for AospyObj in AospyObjs:
                num_objs = self._get_db_obj_query(session, AospyObj).count()
                assert num_objs == 1

    def _assertNotInDB(self, *AospyObjs):
        with self._session_scope() as session:
            for AospyObj in AospyObjs:
                num_objs = self._get_db_obj_query(session, AospyObj).count()
                assert num_objs == 0

    def _assertDBAttrMatches(self, AospyObj, attr):
        with self._session_scope() as session:
            db_obj = self._get_db_obj_query(session, AospyObj).first()
            self._checkAttrMatches(db_obj, AospyObj, attr)

    @staticmethod
    def _checkAttrMatches(db_obj, AospyObj, attr):
        actual = getattr(db_obj, attr)
        expected = getattr(AospyObj, db_obj._metadata_attrs[attr])
        assert actual == expected

    @classmethod
    def _checkAllMetadataAttrsMatch(cls, db_obj, AospyObj):
        for attr in db_obj._metadata_attrs:
            cls._checkAttrMatches(db_obj, AospyObj, attr)

    @classmethod
    def _checkAllDBAttrsMatchRecursive(cls, db_obj, AospyObj):
        cls._checkAllMetadataAttrsMatch(db_obj, AospyObj)
        for attr in db_obj._db_attrs:
            parent_db_obj = getattr(db_obj, attr)
            parent_aospy_obj = getattr(
                AospyObj,
                db_obj._db_attrs[attr]['aospy_obj_attr']
            )
            if (parent_db_obj or parent_aospy_obj):
                # Recursive check will fail if only parent_db_obj or
                # parent_aospy_obj don't exist (either both need to be present
                # or neither need to be present).  If neither are present
                # recursion ends; if both are present recursion continues.
                # If one is present, getattr throws and error.
                cls._checkAllDBAttrsMatchRecursive(
                    parent_db_obj,
                    parent_aospy_obj
                )

    def _assertEqualAttrsRecursive(self, AospyObj):
        """Recursively check to make sure all attributes of the
        object in question and all its parents', grandparents', etc.
        attributes were all faithfully added to the DB.
        """
        with self._session_scope() as session:
            db_obj = self._get_db_obj_query(session, AospyObj).first()
            self._checkAllDBAttrsMatchRecursive(db_obj, AospyObj)
