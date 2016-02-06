"""Test suite for the aospy_synthetic db features."""

import unittest
from subprocess import call

from test_objs import cases, models, example_projects, variables
from aospy_synthetic.calc import Calc, CalcInterface
from aospy_synthetic.SQLAlchemyDB import SQLBackend


class AospySyntheticTestCase(unittest.TestCase):
    def setUp(self):
        self.proj = example_projects.example
        self.model = models.am2
        self.run = cases.am2_control
        self.variable = variables.mse

    def tearDown(self):
#        call(['rm', 'test.db'])
        pass


class TestDB(AospySyntheticTestCase):
    def test_calc(self):
        test_calc = CalcInterface(proj=self.proj,
                                  model=self.model,
                                  run=self.run,
                                  var=self.variable,
                                  date_range=('0021-01-01', '0080-12-31'),
                                  intvl_in='monthly',
                                  intvl_out='son',
                                  dtype_in_time='ts',
                                  dtype_in_vert='sigma',
                                  dtype_out_time='avg',
                                  dtype_out_vert=False,
                                  level=False, backend=SQLBackend())
        calc = Calc(test_calc)
        calc.compute()
        self.assertEqual(calc.intvl_in, 'monthly')


if __name__ == '__main__':
    unittest.main()
