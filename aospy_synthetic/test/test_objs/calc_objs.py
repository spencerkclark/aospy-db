import projects
import models
import runs
import variables
import regions
from aospy_synthetic.calc import CalcInterface, Calc

c = Calc(
    CalcInterface(proj=projects.p,
                  model=models.m,
                  run=runs.r,
                  var=variables.mse,
                  date_range=('0021-01-01', '0080-12-31'),
                  intvl_in='monthly',
                  intvl_out='son',
                  dtype_in_time='ts',
                  dtype_in_vert='sigma',
                  dtype_out_time='avg',
                  dtype_out_vert=False,
                  region=regions.nh,
                  level=False)
)
