"""Test suite for the aospy_synthetic hash functions."""

import unittest
from copy import deepcopy

from test_objs import calc_objs
import heirarchical_test_objs as hto


class SharedHashTests(object):
    ancestors = []
    aospy_cls = ''

    def _assertHashUniqueness(self, test_cls):
        test_obj = self.originals[self.aospy_cls]
        test_obj_copy = self.copies[self.aospy_cls]
        if test_cls in self.ancestors:
            self.assertNotEqual(hash(test_obj), hash(test_obj_copy))
        else:
            self.assertEqual(hash(test_obj), hash(test_obj_copy))

    def setUp(self):
        self.originals = {
            'Calc': calc_objs.c,
            'Run': calc_objs.c.run,
            'Model': calc_objs.c.run.model,
            'Proj': calc_objs.c.run.model.proj,
            'Var': calc_objs.c.var,
            'Units': calc_objs.c.var.units,
            'Region': calc_objs.c.region
        }

        copy = deepcopy(calc_objs.c)
        self.copies = {
            'Calc': copy,
            'Run': copy.run,
            'Model': copy.run.model,
            'Proj': copy.run.model.proj,
            'Var': copy.var,
            'Units': copy.var.units,
            'Region': copy.region
        }

    def tearDown(self):
        pass

    def test_change_proj(self):
        test_cls = 'Proj'
        self.copies[test_cls].name = 'changed'
        self._assertHashUniqueness(test_cls)

    def test_change_model(self):
        test_cls = 'Model'
        self.copies[test_cls].name = 'changed'
        self._assertHashUniqueness(test_cls)

    def test_change_run(self):
        test_cls = 'Run'
        self.copies[test_cls].name = 'changed'
        self._assertHashUniqueness(test_cls)

    def test_change_calc(self):
        test_cls = 'Calc'
        self.copies[test_cls].dtype_out_time = 'changed'
        self._assertHashUniqueness(test_cls)

    def test_change_var(self):
        test_cls = 'Var'
        self.copies[test_cls].name = 'changed'
        self._assertHashUniqueness(test_cls)

    def test_change_units(self):
        test_cls = 'Units'
        self.copies[test_cls].units = 'changed'
        self._assertHashUniqueness(test_cls)

    def test_change_region(self):
        test_cls = 'Region'
        self.copies[test_cls].name = 'changed'
        self._assertHashUniqueness(test_cls)


class TestProjHash(hto.TestProj, SharedHashTests, unittest.TestCase):
    pass


class TestModelHash(hto.TestModel, SharedHashTests, unittest.TestCase):
    pass


class TestRunHash(hto.TestRun, SharedHashTests, unittest.TestCase):
    pass


class TestCalcHash(hto.TestCalc, SharedHashTests, unittest.TestCase):
    pass


class TestVarHash(hto.TestVar, SharedHashTests, unittest.TestCase):
    pass


class TestUnitsHash(hto.TestUnits, SharedHashTests, unittest.TestCase):
    pass


class TestRegionHash(hto.TestRegion, SharedHashTests, unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
