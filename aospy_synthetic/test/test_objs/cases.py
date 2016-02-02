from aospy_synthetic.run import Run
from aospy_synthetic.SQLAlchemyDB import SQLBackend

am2_control = Run(
    name='am2_control',
    description=(
        'Preindustrial control simulation.'
    ),
    data_in_direc=('/archive/Yi.Ming/sm2.1_fixed/'
                   'SM2.1U_Control-1860_lm2_aie_rerun6.YIM/pp'),
    data_in_dur=5,
    data_in_start_date='0001-01-01',
    data_in_end_date='0080-12-31',
    default_date_range=('0021-01-01', '0080-12-31'),
    idealized=False,
    backend=SQLBackend('path')
)

am2_tropics = Run(
    name='am2_tropics',
    description=(
        'Anthropogenic sulfate aerosol forcing only in the'
        ' Northern Hemisphere tropics (EQ to 30N)'
    ),
    data_in_direc=('/archive/Yi.Ming/sm2.1_fixed/'
                   'SM2.1U_Control-1860_lm2_aie2_tropical_rerun6.YIM/pp'),
    data_in_dur=5,
    data_in_start_date='0001-01-01',
    data_in_end_date='0080-12-31',
    default_date_range=('0021-01-01', '0080-12-31'),
    idealized=False,
    backend=SQLBackend('path')
)

am2_extratropics = Run(
    name='am2_extratropics',
    description=(
        'Anthropogenic sulfate aerosol forcing only in the'
        ' Northern Hemisphere extratropics (30N to Pole)'
    ),
    data_in_direc=('/archive/Yi.Ming/sm2.1_fixed/'
                   'SM2.1U_Control-1860_lm2_aie2_extropical_rerun6.YIM/pp'),
    data_in_dur=5,
    data_in_start_date='0001-01-01',
    data_in_end_date='0080-12-31',
    default_date_range=('0021-01-01', '0080-12-31'),
    idealized=False,
    backend=SQLBackend('path')
)

am2_tropics_and_extratropics = Run(
    name='am2_tropics+extratropics',
    description=(
        'Anthropogenic sulfate aerosol forcing everywhere'
    ),
    data_in_direc=('/archive/Yi.Ming/sm2.1_fixed/'
                   'SM2.1U_Control-1860_lm2_aie2_rerun6.YIM/pp'),
    data_in_dur=5,
    data_in_start_date='0001-01-01',
    data_in_end_date='0080-12-31',
    default_date_range=('0021-01-01', '0080-12-31'),
    idealized=False,
    backend=SQLBackend('path')
)

# REYOI Runs - First year is 1982; we throw that out as spinup;
# start analysis in 1983.
# am2_HadISST_control = Run(
#     name='am2_HadISST_control',
#     description=(
#         '1981-2000 HadISST climatological annual cycle of SSTs and sea '
#         'ice repeated annually, with PD atmospheric composition.'
#     ),
#     data_in_direc=('/archive/yim/siena_201203/m45_am2p14_1990/'
#                    'gfdl.ncrc2-intel-prod/pp'),
#     data_in_dur=16,
#     data_in_start_date='1983-01-01',
#     data_in_end_date='1998-12-31',
#     default_date_range=('1983-01-01', '1998-12-31'),
#     idealized=False
# )

# am2_reyoi_control = Run(
#     name='am2_reyoi_control',
#     tags=['reyoi', 'cont'],
#     description='PI atmos and Reynolds OI climatological SSTs',
#     data_in_direc=('/archive/Spencer.Hill/am2/am2clim_reyoi/'
#                    'gfdl.ncrc2-default-prod/pp'),
#     data_in_dur=1,
#     data_in_start_date='1982-01-01',
#     data_in_end_date='1998-12-31',
#     default_date_range=('1983-01-01', '1998-12-31'),
#     idealized=False
# )

# am2_reyoi_extratropics_full = Run(
#     name='am2_reyoi_extratropics_full',
#     description=(
#         'Full SST anomaly pattern applied to REYOI fixed SST climatology.'),
#     data_in_direc=('/archive/Spencer.Clark/am2/'
#                    'am2clim_reyoi_extratropics_full/'
#                    'gfdl.ncrc2-default-prod/pp'),
#     data_in_dur=17,
#     data_in_start_date='1982-01-01',
#     data_in_end_date='1998-12-31',
#     default_date_range=('1983-01-01', '1998-12-31'),
#     idealized=False
# )

# am2_reyoi_extratropics_sp = Run(
#     name='am2_reyoi_extratropics_sp',
#     description=(
#         'Spatial Pattern SST anomaly pattern applied to'
#         ' REYOI fixed SST climatology.'),
#     data_in_direc=('/archive/Spencer.Clark/am2/'
#                    'am2clim_reyoi_extratropics_sp/gfdl.ncrc2-default-prod/pp'),
#     data_in_dur=17,
#     data_in_start_date='1982-01-01',
#     data_in_end_date='1998-12-31',
#     default_date_range=('1983-01-01', '1998-12-31'),
#     idealized=False
# )

# am2_reyoi_tropics_sp_SI = Run(
#     name='am2_reyoi_tropics_sp_SI',
#     description=(
#         'Spatial Pattern SST anomaly pattern applied to REYOI fixed SST'
#         ' climatology.'),
#     data_in_direc=('/archive/Spencer.Clark/am2/'
#                    'am2clim_reyoi_tropics_sp_SI/gfdl.ncrc2-default-prod/pp'),
#     data_in_dur=17,
#     data_in_start_date='1982-01-01',
#     data_in_end_date='1998-12-31',
#     default_date_range=('1983-01-01', '1998-12-31'),
#     idealized=False
# )

# am2_reyoi_tropics_full = Run(
#     name='am2_reyoi_tropics_full',
#     description=(
#         'Full SST anomaly pattern applied to REYOI fixed SST climatology.'),
#     data_in_direc=('/archive/Spencer.Clark/am2/'
#                    'am2clim_reyoi_tropics_full/gfdl.ncrc2-default-prod/pp'),
#     data_in_dur=17,
#     data_in_start_date='1982-01-01',
#     data_in_end_date='1998-12-31',
#     default_date_range=('1983-01-01', '1998-12-31'),
#     idealized=False
# )

# am2_reyoi_extratropics_sp_SI = Run(
#     name='am2_reyoi_extratropics_sp_SI',
#     description=(
#         'Spatial Pattern SST anomaly pattern applied to REYOI fixed'
#         ' SST climatology. Fixed sea-ice.'),
#     data_in_direc=('/archive/Spencer.Clark/am2/'
#                    'am2clim_reyoi_extratropics_sp_SI/'
#                    'gfdl.ncrc2-default-prod/pp'),
#     data_in_dur=17,
#     data_in_start_date='1982-01-01',
#     data_in_end_date='1998-12-31',
#     default_date_range=('1983-01-01', '1998-12-31'),
#     idealized=False
# )

# am2_reyoi_extratropics_u = Run(
#     name='am2_reyoi_extratropics_u',
#     description=(
#         'Uniform SST anomaly pattern applied to REYOI fixed SST climatology.'),
#     data_in_direc=('/archive/Spencer.Clark/am2/'
#                    'am2clim_reyoi_extratropics_u/gfdl.ncrc2-default-prod/pp'),
#     data_in_dur=17,
#     data_in_start_date='1982-01-01',
#     data_in_end_date='1998-12-31',
#     default_date_range=('1983-01-01', '1998-12-31'),
#     idealized=False
# )

# am2_reyoi_tropics_u = Run(
#     name='am2_reyoi_tropics_u',
#     description=(
#         'Uniform SST anomaly pattern applied to REYOI fixed SST climatology.'),
#     data_in_direc=('/archive/Spencer.Clark/am2/'
#                    'am2clim_reyoi_tropics_u/gfdl.ncrc2-default-prod/pp'),
#     data_in_dur=17,
#     data_in_start_date='1982-01-01',
#     data_in_end_date='1998-12-31',
#     default_date_range=('1983-01-01', '1998-12-31'),
#     idealized=False
# )
