"""Test suite for the aospy_synthetic db features."""

import unittest
import os

from test_objs import (runs, models, projects, variables,
                       regions, calc_objs)
from aospy_synthetic.db.sqlalchemy.sqlalchemy_db import SQLAlchemyDB


class SharedDBTests(object):
    def setUp(self):
        raise NotImplementedError()

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
        self.ex_str_attr = 'direc_out'


class TestModelDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = models.m
        self.ex_str_attr = 'description'


class TestRunDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = runs.r
        self.ex_str_attr = 'description'


class TestVarDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = variables.mse
        self.ex_str_attr = 'description'


class TestRegDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = regions.nh
        self.ex_str_attr = 'description'


class TestCalcDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = calc_objs.c
        self.ex_str_attr = 'dtype_out_time'


class TestDeleteCascade(unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.calc = calc_objs.c
        self.run = self.calc.run
        self.model = self.run.model
        self.proj = self.model.proj
        self.var = self.calc.var

    def tearDown(self):
        os.remove('test.db')

    def test_delete_proj(self):
        self.db.add(self.calc)
        self.db.delete(self.proj)

        self.db._assertNotInDB(self.calc)
        self.db._assertNotInDB(self.run)
        self.db._assertNotInDB(self.model)
        self.db._assertNotInDB(self.proj)
        self.db._assertNoDuplicates(self.var)

    def test_delete_calc(self):
        self.db.add(self.calc)
        self.db.delete(self.calc)

        self.db._assertNotInDB(self.calc)
        self.db._assertNoDuplicates(self.run)
        self.db._assertNoDuplicates(self.model)
        self.db._assertNoDuplicates(self.proj)
        self.db._assertNoDuplicates(self.var)


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

        self.db._assertNotInDB(self.proj)

if __name__ == '__main__':
    unittest.main()
