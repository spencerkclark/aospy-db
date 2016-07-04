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
    def setUp(self):
        raise NotImplementedError

    def tearDown(self):
        os.remove('test.db')

    def test_add(self):
        self.db.add(self.AospyObj)
        self.db._assertEqualAttrsRecursive(self.AospyObj)

    def test_uniqueness_checking(self):
        self.db.add(self.AospyObj)
        self.db.add(self.AospyObj)

        self.db._assertNoDuplicates(self.AospyObj)

    def test_update_attr(self):
        self.db.add(self.AospyObj)
        setattr(self.AospyObj, self.ex_str_attr, 'updated')
        self.db.add(self.AospyObj)

        self.db._assertNoDuplicates(self.AospyObj)
        self.db._assertDBAttrMatches(self.AospyObj, self.ex_str_attr)

    def test_delete(self):
        self.db.add(self.AospyObj)
        self.db.delete(self.AospyObj)

        self.db._assertNotInDB(self.AospyObj)


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

    def tearDown(self):
        os.remove('test.db')

    def test_delete_parent(self):
        self.db.add(self.calc)
        self.db.delete(self.proj)

        self.db._assertNotInDB(self.calc)
        self.db._assertNotInDB(self.run)
        self.db._assertNotInDB(self.model)
        self.db._assertNotInDB(self.proj)

    def test_delete_child(self):
        self.db.add(self.calc)
        self.db.delete(self.calc)

        self.db._assertNotInDB(self.calc)
        self.db._assertNoDuplicates(self.run)
        self.db._assertNoDuplicates(self.model)
        self.db._assertNoDuplicates(self.proj)


class TestDBTrackingToggle(unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.proj = projects.p
        self.calc = calc_objs.c

    def tearDown(self):
        os.remove('test.db')

    @unittest.expectedFailure  # Feature not implemented yet
    def test_dont_track(self):
        self.proj.db_tracking = False
        self.db.add(self.proj)
        with self.db._session_scope() as session:
            q = session.query(ProjDB)
            num_objs = q.filter_by(hash=hash(self.proj)).count()
            self.assertEqual(num_objs, 0)

if __name__ == '__main__':
    unittest.main()
