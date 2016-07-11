from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from ..abstract_db import AbstractBackend
from sqlalchemy_config import (initialize_db,
                               ProjDB, ModelDB, RunDB,
                               VarDB, CalcDB, RegionDB, UnitsDB)


class SQLAlchemyDB(AbstractBackend):
    """Implements AbstractBackend methods"""

    def __init__(self, db_url='sqlite:///test.db'):
        """Initializes a sqlite database using SQLAlchemy and
        returns its handle.

        For details on writing database URLs for local sqlite databases
        see http://docs.sqlalchemy.org/en/latest/core/engines.html.

        Parameters
        ----------
        db_url : str
            Url of database.

        Returns
        -------
        db : SQLAlchemyDB
            Backend for use in aospy.
        """
        self.DB_PATH = db_url
        self.engine = create_engine(self.DB_PATH, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        initialize_db(self.DB_PATH)

    @contextmanager
    def _session_scope(self):
        """Creates a scoped session environment for use with the database.

        Examples
        --------
        A scoped session automatically handles creating and closing a session,
        such that no hanging active sessions persist.

        .. ipython:: python

            from sqlalchemy_db import SQLAlchemyDB
            from sqlalchemy_config import ProjDB
            from test_objs import projects
            db = SQLAlchemyDB()
            with db._session_scope() as session:
                q = session.query(ProjDB)
                db_obj = q.filter_by(hashcode=hash(projects.p)).first()
        """
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
        """Returns the database class associated with a given aospy core
        object.

        Parameters
        ----------
        AospyObj
            Aospy core object.

        Returns
        -------
        DBObj
            Sqlalchemy database row object.
        """
        mapping = {
            'Proj': ProjDB,
            'Model': ModelDB,
            'Run': RunDB,
            'Calc': CalcDB,
            'Var': VarDB,
            'Region': RegionDB,
            'Units': UnitsDB
        }
        return mapping[AospyObj.__class__.__name__]

    def add(self, AospyObj):
        """Adds an aospy core object to the database if tracking is enabled
        for the object and its parents.

        Parameters
        ----------
        AospyObj
            Aospy core object.

        Raises
        ------
        RuntimeError
            If AospyObj.track() is False.
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
        """Deletes an aospy object from the database if it exists.

        Parameters
        ----------
        AospyObj
            Aospy core object.
        """
        with self._session_scope() as session:
            q = session.query(self._db_cls_from_aospy_cls(AospyObj))
            db_obj = q.filter_by(hashcode=hash(AospyObj)).first()
            if db_obj:
                session.delete(db_obj)

    def query():
        raise NotImplementedError()

    @classmethod
    def _get_db_obj_query(cls, session, AospyObj):
        """Returns a sqlalchemy query result for a single aospy core object.

        Parameters
        ----------
        session : Session
            Active sqlalchemy session connected to the database.
        AospyObj
            Aospy core object.

        Returns
        -------
        Query
            Query result for a single aospy core object.
        """
        db_cls = cls._db_cls_from_aospy_cls(AospyObj)
        q = session.query(db_cls)
        return q.filter_by(hashcode=hash(AospyObj))

    # Define hidden testing methods
    def _assertNoDuplicates(self, *AospyObjs):
        """Tests if there are single entries in the database for the given
        aospy core objects.

        Parameters
        ----------
        *AospyObjs
            Aospy core object(s) to test.

        Raises
        ------
        AssertionError
            If there are zero or more than one instances of the objects in the
            database.
        """
        with self._session_scope() as session:
            for AospyObj in AospyObjs:
                num_objs = self._get_db_obj_query(session, AospyObj).count()
                assert num_objs == 1

    def _assertNotInDB(self, *AospyObjs):
        """Tests if entries do not exist in the database for the given aospy
        core objects.

        Parameters
        ----------
        *AospyObjs
            Aospy core object(s) to test.

        Raises
        ------
        AssertionError
            If there are any instances of the aospy core object(s) in the
            database.
        """
        with self._session_scope() as session:
            for AospyObj in AospyObjs:
                num_objs = self._get_db_obj_query(session, AospyObj).count()
                assert num_objs == 0

    def _assertDBAttrMatches(self, AospyObj, attr):
        """Tests if a given database attribute matches the corresponding
        attribute in a given aospy core object.

        Parameters
        ----------
        AospyObj
            Aospy core object.
        attr : str
            Attribute name within the corresponding database object.

        Raises
        ------
        AssertionError
            If the attribute values between the aospy core object and database
            object do not match.
        """
        with self._session_scope() as session:
            db_obj = self._get_db_obj_query(session, AospyObj).first()
            self._checkAttrMatches(db_obj, AospyObj, attr)

    @staticmethod
    def _checkAttrMatches(db_obj, AospyObj, attr):
        """Tests that an attribute value in a database object matches its
        corresponding attribute in an aospy core object.

        Parameters
        ----------
        db_obj
            Database row instance.
        AospyObj
            Aospy core object.
        attr : str
            Attribute name in database row instance.

        Raises
        ------
        AssertionError
            If corresponding attribute values do not match
        """
        actual = getattr(db_obj, attr)
        expected = getattr(AospyObj, db_obj._metadata_attrs[attr])
        assert actual == expected

    @classmethod
    def _checkAllMetadataAttrsMatch(cls, db_obj, AospyObj):
        """Tests if all tracked attributes between a database row object
        and an aospy core object match.

        Parameters
        ----------
        db_obj
            Database row instance.
        AospyObj
            Aospy core object.

        Raises
        ------
        AssertionError
            If any corresponding attributes do not match.
        """
        for attr in db_obj._metadata_attrs:
            cls._checkAttrMatches(db_obj, AospyObj, attr)

    @classmethod
    def _checkAllDBAttrsMatchRecursive(cls, db_obj, AospyObj):
        """Recursively traverse the object tree and test if database object
        attributes match the corresponding aospy core object attributes.

        Parameters
        ----------
        db_obj
            Database row object.
        AospyObj
            Aospy core object.

        Raises
        ------
        AssertionError
            If there is a mismatch between any database attributes and
            corresponding aospy core object attributes.
        """
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
                # If one is present, getattr raises an error.
                cls._checkAllDBAttrsMatchRecursive(
                    parent_db_obj,
                    parent_aospy_obj
                )

    def _assertEqualAttrsRecursive(self, AospyObj):
        """Recursively test to make sure all attributes of the
        object in question and all its parents', grandparents', etc.
        attributes were all faithfully added to the DB.

        Parameters
        ----------
        AospyObj
            aospy core object

        Raises
        ------
        AssertionError
            If any attributes in the aospy core object, or any of those in that
            object's ancestors, do not match their corresponding attributes
            in the database
        """
        with self._session_scope() as session:
            db_obj = self._get_db_obj_query(session, AospyObj).first()
            self._checkAllDBAttrsMatchRecursive(db_obj, AospyObj)
