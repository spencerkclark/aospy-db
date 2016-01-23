from aospy_synthetic.run import Run
# import numpy as np
# import pandas as pd
from datetime import datetime, timedelta

# S. Clark 10-30-2015: Contrary to what idealized model runs suggest,
# we start at year 1 NOT 0.
# Also note that it throws things into a 365 day no-leap calendar.
# So if you want the last 360 days you need to be smarter about things.

varia = ['olr', 'temp', 'sphum', 'ps', 'vcomp', 'swdn_sfc', 'olr', 'lwdn_sfc',
         'lwup_sfc', 'flux_t', 'flux_lhe',
         'convection_rain', 'condensation_rain',
         'ucomp', 'omega', 'umse', 'vmse', 'omega_mse', 'mse', 'umse_vint',
         'vmse_vint', 'omega_mse_vint']

# If we run more than four years we'll have to think about leap years,
# but for now this is OK.
model_start = datetime(1, 1, 1)
length = timedelta(days=720)
end = model_start + length
analysis_length = timedelta(days=360)
a_start = str(end - analysis_length)
a_end = str(end)

control_T85 = Run(
    name='control_T85',
    description=(
        'A test case for using aospy + an idealized simulation.'
    ),
    data_in_direc='/archive/skc/idealized_moist_T85/control_T85/'
                  'gfdl.ncrc2-default-prod/1x0m720d_32pe/history',
    default_date_range=(a_start, a_end),
    data_in_dir_struc='one_dir',
    data_in_files={'20-day': {v: '00000.1x20days.nc' for v in varia},
                   'daily': {v: '00000.1xday.nc' for v in varia},
                   '6-hourly': {v: '00000.4xday.nc' for v in varia}},
    idealized=False
)

extratropics_15_T85 = Run(
    name='extratropics_0.15_T85',
    description=(
        'Solar absorption decreased by 15% from 30N to 90N'
    ),
    data_in_direc='/archive/skc/idealized_moist_alb_T85/extratropics_0.15_T85/'
                  'gfdl.ncrc2-default-prod/1x0m720d_32pe/history',
    default_date_range=(a_start, a_end),
    data_in_dir_struc='one_dir',
    data_in_files={'20-day': {v: '00000.1x20days.nc' for v in varia},
                   'daily': {v: '00000.1xday.nc' for v in varia},
                   '6-hourly': {v: '00000.4xday.nc' for v in varia}},
    idealized=False
)

extratropics_037_T85 = Run(
    name='extratropics_0.037_T85',
    description=(
        'Solar absorption decreased by 3.7% from 30N to 90N'
    ),
    data_in_direc='/archive/skc/idealized_moist_alb_T85/extratropics_0.037_T85'
                  '/gfdl.ncrc2-default-prod/1x0m720d_32pe/history',
    default_date_range=(a_start, a_end),
    data_in_dir_struc='one_dir',
    data_in_files={'20-day': {v: '00000.1x20days.nc' for v in varia},
                   'daily': {v: '00000.1xday.nc' for v in varia},
                   '6-hourly': {v: '00000.4xday.nc' for v in varia}},
    idealized=False
)

tropics_10_T85 = Run(
    name='tropics_0.1_T85',
    description=(
        'Solar absorption decreased by 10% from EQ to 30N'
    ),
    data_in_direc='/archive/skc/idealized_moist_alb_T85/tropics_0.1_T85/'
                  'gfdl.ncrc2-default-prod/1x0m720d_32pe/history',
    default_date_range=(a_start, a_end),
    data_in_dir_struc='one_dir',
    data_in_files={'20-day': {v: '00000.1x20days.nc' for v in varia},
                   'daily': {v: '00000.1xday.nc' for v in varia},
                   '6-hourly': {v: '00000.4xday.nc' for v in varia}},
    idealized=False
)

tropics_025_T85 = Run(
    name='tropics_0.025_T85',
    description=(
        'Solar absorption decreased by 2.5% from EQ to 30N'
    ),
    data_in_direc='/archive/skc/idealized_moist_alb_T85/tropics_0.025_T85/'
                  'gfdl.ncrc2-default-prod/1x0m720d_32pe/history',
    default_date_range=(a_start, a_end),
    data_in_dir_struc='one_dir',
    data_in_files={'20-day': {v: '00000.1x20days.nc' for v in varia},
                   'daily': {v: '00000.1xday.nc' for v in varia},
                   '6-hourly': {v: '00000.4xday.nc' for v in varia}},
    idealized=False
)

control_alb_T42 = Run(
    name='control_alb_T42',
    description=(
        'Control case at T42 spectral resolution'
    ),
    data_in_direc='/archive/skc/idealized_moist_alb_T42/control_alb_T42/'
                  'gfdl.ncrc2-default-prod/1x0m720d_32pe/history',
    default_date_range=(a_start, a_end),
    data_in_dir_struc='one_dir',
    data_in_files={'20-day': {v: '00000.1x20days.nc' for v in varia},
                   'daily': {v: '00000.1xday.nc' for v in varia},
                   '3-hourly': {v: '{}.8xday.nc'.format(v) for v in varia}},
    idealized=False
)
