"""Test suite for the aospy_synthetic db features."""

import unittest
import os

from test_objs import (
    runs, models, projects, variables, regions, calc_objs, units
)
import heirarchical_test_objs as hto
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


class SharedDBTrackTests(object):
    ancestors = []
    aospy_cls = ''

    def _assertProperTrackingFlag(self, test_cls):
        self.assertEqual(self.objects[test_cls].db_tracking, True)
        self.objects[test_cls].db_tracking = False

        aospy_obj = self.objects[self.aospy_cls]
        if test_cls in self.ancestors:
            self.assertEqual(aospy_obj.track(), False)
        else:
            self.assertEqual(aospy_obj.track(), True)

    def setUp(self):
        self.db = SQLAlchemyDB()
        self.objects = {
            'Calc': calc_objs.c,
            'Run': calc_objs.c.run,
            'Model': calc_objs.c.run.model,
            'Proj': calc_objs.c.run.model.proj,
            'Var': calc_objs.c.var,
            'Units': calc_objs.c.var.units,
            'Region': calc_objs.c.region
        }

    def tearDown(self):
        for aospy_cls, aospy_obj in self.objects.iteritems():
            aospy_obj.db_tracking = True
        os.remove('test.db')

    def test_tracking_set_proj_false(self):
        test_cls = 'Proj'
        self._assertProperTrackingFlag(test_cls)

    def test_tracking_set_model_false(self):
        test_cls = 'Model'
        self._assertProperTrackingFlag(test_cls)

    def test_tracking_set_run_false(self):
        test_cls = 'Run'
        self._assertProperTrackingFlag(test_cls)

    def test_dont_track(self):
        aospy_obj = self.objects[self.aospy_cls]
        aospy_obj.db_tracking = False
        self.assertRaises(RuntimeError, self.db.add, aospy_obj)


class TestProjTrack(hto.TestProj, SharedDBTrackTests, unittest.TestCase):
    pass


class TestModelTrack(hto.TestModel, SharedDBTrackTests, unittest.TestCase):
    pass


class TestRunTrack(hto.TestRun, SharedDBTrackTests, unittest.TestCase):
    pass


class TestCalcTrack(hto.TestCalc, SharedDBTrackTests, unittest.TestCase):
    pass


class TestVarTrack(hto.TestVar, SharedDBTrackTests, unittest.TestCase):
    pass


class TestUnitsTrack(hto.TestUnits, SharedDBTrackTests, unittest.TestCase):
    pass


class TestRegionTrack(hto.TestRegion, SharedDBTrackTests, unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
