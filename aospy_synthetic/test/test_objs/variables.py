"""Collection of aospy.Var objects for use in my research."""
from aospy_synthetic.var import Var
import calcs
import units

p = Var(
    name='p',
    units=units.Pa,
    domain='atmos',
    description='Pressure of model half levels.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
ps = Var(
    name='ps',
    units=units.Pa,
    domain='atmos',
    description='Surface pressure.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
bk = Var(
    name='bk',
    units=units.Pa,
    domain='atmos_level',
    description='Sigma part of hybrid sigma coordinate.',
    def_time=False,
    def_vert=True,
    def_lat=False,
    def_lon=False,
    in_nc_grid=True
)
pk = Var(
    name='pk',
    units=units.Pa,
    domain='atmos_level',
    description='Pressure part of hybrid sigma coordinate.',
    def_time=False,
    def_vert=True,
    def_lat=False,
    def_lon=False,
    in_nc_grid=True
)
temp = Var(
    name='temp',
    alt_names=('ta',),
    units=units.K,
    domain='atmos',
    description='Air temperature.',
    def_time=True,
    def_vert='pfull',
    def_lat=True,
    def_lon=True,
    in_nc_grid=False,
    colormap='RdBu_r'
)
dp = Var(
    name='dp',
    domain='atmos',
    description=('Pressure thickness of model levels.  For data interpolated '
                 'to uniform pressure levels, this does not vary in time or '
                 'space.  For data on model native coordinates, this varies '
                 'in space and time due to the spatiotemporal variations in '
                 'surface pressure.'),
    variables=(ps, bk, pk, temp),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False,
    func=calcs.dp,
    units=units.Pa,
)
olr = Var(
    name='olr',
    alt_names=('rlut',),
    units=units.W_m2,
    domain='atmos',
    description='All-sky outgoing longwave radiation at TOA.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
sphum = Var(
    name='sphum',
    alt_names=('hus',),
    units=units.specific_mass,
    domain='atmos',
    description='Specific humidity.',
    def_time=True,
    def_vert='pfull',
    def_lat=True,
    def_lon=True,
    in_nc_grid=False,
    colormap='Greys'
)
swdn_toa = Var(
    name='swdn_toa',
    alt_names=('rsdt',),
    units=units.W_m2,
    domain='atmos',
    description='Downwelling shortwave radiation at TOA.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
swup_toa = Var(
    name='swup_toa',
    alt_names=('rsut',),
    units=units.W_m2,
    domain='atmos',
    description='All-sky Upwelling shortwave radiation at TOA.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
gz = Var(
    name='gz',
    domain='atmos',
    description=('Atmospheric Geopotential'),
    variables=(temp, sphum, dp, p),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    func=calcs.gz,
    units=units.J_kg1
)
dse = Var(
    name='dse',
    domain='atmos',
    description=('Dry Static Energy'),
    variables=(temp, sphum, dp, p),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    func=calcs.dse,
    units=units.J_kg1
)
mse = Var(
    name='mse',
    domain='atmos',
    description=('Moist Static Energy'),
    variables=(temp, sphum, dp, p),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    func=calcs.mse,
    units=units.J_kg1
)
net_sw_toa = Var(
    name='net_sw_toa',
    domain='atmos',
    description=('Net shortwave radiation at the top of atmosphere'),
    variables=(swdn_toa, swup_toa),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.net_sw_toa,
    units=units.W_m2
)
master_vars_list = [
    p, ps, dp, bk, pk, temp, sphum, olr, swdn_toa, swup_toa, gz, dse, mse,
    net_sw_toa
]


class variables(object):
    def __init__(self, vars_list):
        for var in vars_list:
            setattr(self, var.name, var)
