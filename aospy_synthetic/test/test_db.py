"""Test suite for the aospy_synthetic db features."""

import unittest
import os

from test_objs import (runs, models, projects, variables,
                       regions, calc_objs)
from aospy_synthetic.db.sqlalchemy.sqlalchemy_db import SQLAlchemyDB
from aospy_synthetic.db.sqlalchemy.sqlalchemy_config import (ProjDB, ModelDB,
                                                             RunDB, VarDB,
                                                             RegionDB, CalcDB)


class SharedDBTests(object):
    def recursive_check_attrs(self, db_obj, AospyObj):
        """Recursively check to make sure all attributes of the
        object in question and all its parents', grandparents', etc.
        attributes were all faithfully added to the DB.
        """
        for attr, aospy_obj_attr in db_obj._metadata_attrs.iteritems():
            actual = getattr(db_obj, attr)
            expected = getattr(
                AospyObj,
                aospy_obj_attr
            )
            self.assertEqual(actual, expected)

        for attr in db_obj._db_attrs:
            parent_db_obj = getattr(db_obj, attr)
            parent_aospy_obj = getattr(
                AospyObj,
                db_obj._db_attrs[attr]['aospy_obj_attr']
            )
            if (parent_db_obj or parent_aospy_obj):
                # Recursive check will fail if only parent_db_obj or
                # parent_aospy_obj don't exist (either both need to be present
                # or neither need to be present).
                self.recursive_check_attrs(parent_db_obj, parent_aospy_obj)

    def tearDown(self):
        os.remove('test.db')

    def test_add(self):
        self.db.add(self.AospyObj)
        with self.db._session_scope() as session:
            q = session.query(self.db_cls)
            db_obj = q.filter_by(hash=hash(self.AospyObj)).first()
            self.recursive_check_attrs(db_obj, self.AospyObj)

    def test_uniqueness_checking(self):
        self.db.add(self.AospyObj)
        self.db.add(self.AospyObj)  # Call add on a duplicate object
        with self.db._session_scope() as session:
            q = session.query(self.db_cls)
            db_objs = q.filter_by(hash=hash(self.AospyObj)).all()
            self.assertEqual(len(db_objs), 1)

    def test_update_attr(self):
        self.db.add(self.AospyObj)
        setattr(self.AospyObj, self.ex_str_attr, 'updated')
        self.db.add(self.AospyObj)
        with self.db._session_scope() as session:
            q = session.query(self.db_cls)
            db_objs = q.filter_by(hash=hash(self.AospyObj)).all()
            self.assertEqual(len(db_objs), 1)  # No duplicates

            db_obj = db_objs[0]
            actual = getattr(db_obj, self.ex_str_attr)
            expected = 'updated'
            self.assertEqual(actual, expected)


class TestProjDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = projects.p
        self.db_cls = ProjDB
        self.ex_str_attr = 'direc_out'


class TestModelDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = models.m
        self.db_cls = ModelDB
        self.ex_str_attr = 'description'


class TestRunDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = runs.r
        self.db_cls = RunDB
        self.ex_str_attr = 'description'


class TestVarDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = variables.mse
        self.db_cls = VarDB
        self.ex_str_attr = 'description'


class TestRegDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = regions.nh
        self.db_cls = RegionDB
        self.ex_str_attr = 'description'


class TestCalcDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = calc_objs.c
        self.db_cls = CalcDB
        self.ex_str_attr = 'dtype_out_time'


if __name__ == '__main__':
    unittest.main()
