"""Test suite for the aospy_synthetic hash functions."""

import unittest
from copy import deepcopy

from test_objs import calc_objs


class SharedHashTests(object):
    ancestors = []
    descendents = []
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
            'Units': calc_objs.c.var.units
        }

        copy = deepcopy(calc_objs.c)
        self.copies = {
            'Calc': copy,
            'Run': copy.run,
            'Model': copy.run.model,
            'Proj': copy.run.model.proj,
            'Var': copy.var,
            'Units': copy.var.units
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


class TestProjHash(SharedHashTests, unittest.TestCase):
    ancestors = ['Proj']
    descendents = ['Model', 'Run', 'Calc']
    aospy_cls = 'Proj'


class TestModelHash(SharedHashTests, unittest.TestCase):
    ancestors = ['Proj', 'Model']
    descendents = ['Run', 'Calc']
    aospy_cls = 'Model'


class TestRunHash(SharedHashTests, unittest.TestCase):
    ancestors = ['Proj', 'Model', 'Run']
    descendents = ['Calc']
    aospy_cls = 'Run'


class TestCalcHash(SharedHashTests, unittest.TestCase):
    ancestors = ['Proj', 'Model', 'Run', 'Calc', 'Var', 'Units']
    descendents = []
    aospy_cls = 'Calc'


class TestVarHash(SharedHashTests, unittest.TestCase):
    ancestors = ['Var', 'Units']
    descendents = ['Calc']
    aospy_cls = 'Var'


class TestUnitsHash(SharedHashTests, unittest.TestCase):
    ancestors = ['Units']
    descendents = ['Var', 'Calc']
    aospy_cls = 'Units'


if __name__ == '__main__':
    unittest.main()
