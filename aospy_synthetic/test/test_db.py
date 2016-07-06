"""Test suite for the aospy_synthetic db features."""

import unittest
import os

from test_objs import (runs, models, projects, variables,
                       regions, calc_objs, units)
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


class TestRegionDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = regions.nh
        self.ex_str_attr = 'description'


class TestCalcDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = calc_objs.c
        self.ex_str_attr = 'dtype_out_time'


class TestUnitsDB(SharedDBTests, unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = units.J_kg1
        self.ex_str_attr = 'plot_units'


class TestDeleteCascade(unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.calc = calc_objs.c
        self.run = self.calc.run
        self.model = self.run.model
        self.proj = self.model.proj
        self.var = self.calc.var
        self.units = self.var.units
        self.region = self.calc.region

        self.db.add(self.calc)

    def tearDown(self):
        os.remove('test.db')

    def test_delete_proj(self):
        self.db.delete(self.proj)
        self.db._assertNotInDB(self.calc, self.run, self.model, self.proj)
        self.db._assertNoDuplicates(self.var, self.units, self.region)

    def test_delete_model(self):
        self.db.delete(self.model)
        self.db._assertNotInDB(self.calc, self.run, self.model)
        self.db._assertNoDuplicates(
            self.var, self.proj, self.units, self.region
        )

    def test_delete_run(self):
        self.db.delete(self.run)
        self.db._assertNotInDB(self.calc, self.run)
        self.db._assertNoDuplicates(
            self.var, self.proj, self.model, self.units, self.region
        )

    def test_delete_calc(self):
        self.db.delete(self.calc)
        self.db._assertNotInDB(self.calc)
        self.db._assertNoDuplicates(
            self.run, self.model, self.proj, self.var, self.units, self.region
        )

    def test_delete_var(self):
        self.db.delete(self.var)
        self.db._assertNotInDB(self.calc, self.var)
        self.db._assertNoDuplicates(
            self.run, self.model, self.proj, self.units, self.region
        )

    def test_delete_units(self):
        self.db.delete(self.units)
        self.db._assertNotInDB(self.units, self.var, self.calc)
        self.db._assertNoDuplicates(
            self.proj, self.model, self.run, self.region
        )

    def test_delete_region(self):
        self.db.delete(self.region)
        self.db._assertNotInDB(self.calc, self.region)
        self.db._assertNoDuplicates(
            self.proj, self.model, self.run, self.var, self.units
        )


class TestDBTrackingToggle(unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.calc = calc_objs.c
        self.var = self.calc.var
        self.run = self.calc.run
        self.model = self.run.model
        self.proj = self.model.proj
        self.units = self.var.units

    def tearDown(self):
        self.calc.db_tracking = True
        self.run.db_tracking = True
        self.model.db_tracking = True
        self.proj.db_tracking = True
        self.var.db_tracking = True
        self.units.db_tracking = True
        os.remove('test.db')

    def test_tracking_flag_proj(self):
        self.assertEqual(self.proj.track(), True)
        self.proj.db_tracking = False
        self.assertEqual(self.proj.track(), False)
        self.assertEqual(self.model.track(), False)
        self.assertEqual(self.run.track(), False)
        self.assertEqual(self.calc.track(), False)
        self.assertEqual(self.units.track(), True)

    def test_tracking_flag_units(self):
        self.assertEqual(self.units.track(), True)
        self.units.db_tracking = False
        self.assertEqual(self.units.track(), False)
        self.assertEqual(self.proj.track(), True)
        self.assertEqual(self.model.track(), True)
        self.assertEqual(self.run.track(), True)
        self.assertEqual(self.calc.track(), False)
        self.assertEqual(self.var.track(), False)

    def test_dont_track(self):
        self.proj.db_tracking = False
        self.assertRaises(RuntimeError, self.db.add, self.proj)


if __name__ == '__main__':
    unittest.main()
