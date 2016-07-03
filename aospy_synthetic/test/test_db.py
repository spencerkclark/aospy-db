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
    def assertNoDuplicates(self, query_obj, AospyObj):
        num_objs = query_obj.filter_by(hash=hash(self.AospyObj)).count()
        self.assertEqual(num_objs, 1)

    def assertEqualMetadataAttrs(self, db_obj, AospyObj):
        for attr, aospy_obj_attr in db_obj._metadata_attrs.iteritems():
            actual = getattr(db_obj, attr)
            expected = getattr(
                AospyObj,
                aospy_obj_attr
            )
            self.assertEqual(actual, expected)

    def assertEqualAttrsRecursive(self, db_obj, AospyObj):
        """Recursively check to make sure all attributes of the
        object in question and all its parents', grandparents', etc.
        attributes were all faithfully added to the DB.
        """
        self.assertEqualMetadataAttrs(db_obj, AospyObj)

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
                self.assertEqualAttrsRecursive(parent_db_obj, parent_aospy_obj)

    def tearDown(self):
        os.remove('test.db')

    def test_add(self):
        self.db.add(self.AospyObj)
        with self.db._session_scope() as session:
            q = session.query(self.db_cls)
            db_obj = q.filter_by(hash=hash(self.AospyObj)).first()
            self.assertEqualAttrsRecursive(db_obj, self.AospyObj)

    def test_uniqueness_checking(self):
        self.db.add(self.AospyObj)
        self.db.add(self.AospyObj)
        with self.db._session_scope() as session:
            q = session.query(self.db_cls)
            self.assertNoDuplicates(q, self.AospyObj)

    def test_update_attr(self):
        self.db.add(self.AospyObj)
        setattr(self.AospyObj, self.ex_str_attr, 'updated')
        self.db.add(self.AospyObj)
        with self.db._session_scope() as session:
            q = session.query(self.db_cls)
            self.assertNoDuplicates(q, self.AospyObj)

            db_obj = q.filter_by(hash=hash(self.AospyObj)).first()
            actual = getattr(db_obj, self.ex_str_attr)
            expected = 'updated'
            self.assertEqual(actual, expected)

    def test_delete(self):
        self.db.add(self.AospyObj)
        self.db.delete(self.AospyObj)
        with self.db._session_scope() as session:
            q = session.query(self.db_cls)
            num_objs = q.filter_by(hash=hash(self.AospyObj)).count()
            self.assertEqual(num_objs, 0)


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


class TestDeleteCascade(unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.proj = projects.p
        self.model = models.m
        self.run = runs.r
        self.calc = calc_objs.c

    def test_delete_parent(self):
        self.db.add(self.calc)
        self.db.delete(self.run)
        with self.db._session_scope() as session:
            q = session.query(CalcDB)
            num_objs = q.filter_by(hash=hash(self.calc)).count()
            self.assertEqual(num_objs, 0)

            q = session.query(RunDB)
            num_objs = q.filter_by(hash=hash(self.run)).count()
            self.assertEqual(num_objs, 0)


if __name__ == '__main__':
    unittest.main()
