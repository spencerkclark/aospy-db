from aospy_synthetic.model import Model
import cases as runs
#import idealized
from aospy_synthetic.SQLAlchemyDB import SQLBackend


am2 = Model(
    name='am2',
    grid_file_paths=(
        ('/archive/Yi.Ming/sm2.1_fixed/SM2.1U_Control-1860_lm2_aie_rerun6.YIM/'
         'pp/atmos/atmos.static.nc'),
        ('/archive/Yi.Ming/sm2.1_fixed/SM2.1U_Control-1860_lm2_aie_rerun6.YIM/'
         'pp/atmos_level/atmos_level.static.nc'),
        ('/archive/Yi.Ming/sm2.1_fixed/SM2.1U_Control-1860_lm2_aie_rerun6.YIM/'
         'pp/atmos_level/ts/monthly/5yr/atmos_level.011601-012012.vcomp.nc'),
        ('/archive/Yi.Ming/sm2.1_fixed/SM2.1U_Control-1860_lm2_aie_rerun6.YIM/'
         'pp/atmos/ts/monthly/100yr/atmos.000101-010012.temp.nc')
    ),
    runs=[runs.am2_control, runs.am2_tropics, runs.am2_extratropics,
          runs.am2_tropics_and_extratropics],
    default_runs=[runs.am2_control, runs.am2_tropics, runs.am2_extratropics,
                  runs.am2_tropics_and_extratropics],
    backend=SQLBackend('path')
)

# am2_reyoi = Model(
#     name='am2_reyoi',
#     grid_file_paths=(
#         ('/archive/yim/siena_201203/m45_am2p14_1990/gfdl.ncrc2-intel-prod/'
#          'pp/atmos/atmos.static.nc',
#          '/archive/yim/siena_201203/m45_am2p14_1990/gfdl.ncrc2-intel-prod/'
#          'pp/atmos_level/atmos_level.static.nc',
#          '/archive/yim/siena_201203/m45_am2p14_1990/gfdl.ncrc2-intel-prod/'
#          'pp/atmos/ts/annual/16yr/atmos.1983-1998.temp.nc',
#          '/archive/yim/siena_201203/m45_am2p14_1990/gfdl.ncrc2-intel-prod/'
#          'pp/atmos_level/ts/monthly/16yr/atmos_level.198301-199812.temp.nc')
#     ),
#     runs=[runs.am2_HadISST_control, runs.am2_reyoi_extratropics_full,
#           runs.am2_reyoi_extratropics_sp, runs.am2_reyoi_extratropics_u,
#           runs.am2_reyoi_extratropics_sp_SI,
#           runs.am2_reyoi_tropics_sp_SI, runs.am2_reyoi_tropics_full,
#           runs.am2_reyoi_tropics_u],
#     default_runs=[runs.am2_HadISST_control, runs.am2_reyoi_extratropics_full,
#                   runs.am2_reyoi_extratropics_sp,
#                   runs.am2_reyoi_extratropics_u,
#                   runs.am2_reyoi_extratropics_sp_SI,
#                   runs.am2_reyoi_tropics_sp_SI, runs.am2_reyoi_tropics_full,
#                   runs.am2_reyoi_tropics_u],
#     backend=SQLAlchemyDB('path')
# )

# dargan = Model(
#     name='dargan',
#     grid_file_paths=(
#         ('/archive/skc/idealized_moist_T85/control_T85/'
#          'gfdl.ncrc2-default-prod/'
#          '1x0m720d_32pe/history/00000.1x20days.nc'),
#     ),
#     runs=[idealized.control_T85, idealized.extratropics_15_T85,
#           idealized.extratropics_037_T85,
#           idealized.tropics_10_T85, idealized.tropics_025_T85],
#     default_runs=[idealized.control_T85, idealized.extratropics_15_T85,
#                   idealized.extratropics_037_T85,
#                   idealized.tropics_10_T85, idealized.tropics_025_T85],
#     backend=SQLAlchemyDB('path')
# )

# dargan_T42 = Model(
#     name='dargan_T42',
#     grid_file_paths=(
#         ('/archive/skc/idealized_moist_alb_T42/control_alb_T42/'
#          'gfdl.ncrc2-default-prod/1x0m720d_32pe/history/00000.1x20days.nc'),
#     ),
#     runs=[idealized.control_alb_T42],
#     default_runs=[idealized.control_alb_T42],
#     backend=SQLAlchemyDB('path')
# )
