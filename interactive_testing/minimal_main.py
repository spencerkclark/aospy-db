from aospy_synthetic.calc import Calc, CalcInterface

import cases
import models
import example_projects
import variables

test = CalcInterface(proj=example_projects.example,
                     model=models.am2,
                     run=cases.am2_control,
                     var=variables.mse,
                     date_range=('0021-01-01', '0080-12-31'),
                     intvl_in='monthly',
                     intvl_out='son',
                     dtype_in_time='ts',
                     dtype_in_vert='sigma',
                     dtype_out_time='avg',
                     dtype_out_vert=False,
                     level=False)
calc = Calc(test)
calc.compute()
