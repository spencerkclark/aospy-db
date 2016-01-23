"""Collection of aospy.Var objects for use in my research."""
from aospy.constants import c_p, r_e
from aospy.var import Var
from aospy_user import calcs, units

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

alb_sfc = Var(
    name='alb_sfc',
    units=units.unitless,
    domain='atmos',
    description='Surface albedo.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
cld_amt = Var(
    name='cld_amt',
    alt_names=('cl',),
    units=units.unitless,
    domain='atmos',
    description='Cloud fraction at each level.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

divg = Var(
    name='divg',
    math_str=r"\nabla\cdot\vec{v}",
    units=units.s1,
    domain='atmos',
    description='Divergence.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False,
    colormap='RdBu'
)
esf = Var(
    name='esf',
    units=units.kg_s1,
    domain='atmos',
    description='Eddy streamfunction',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

evap = Var(
    name='evap',
    alt_names=('ET_mean', 'evspsbl'),
    math_str=r"$E$",
    units=units.kg_m2_s1,
    domain='atmos',
    description='Surface evaporation',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

high_cld_amt = Var(
    name='high_cld_amt',
    units=units.unitless,
    domain='atmos',
    description='High cloud fraction.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

lai = Var(
    name='lai',
    alt_names=('LAI',),
    units=units.unitless,
    domain='land',
    description='Leaf area index.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
low_cld_amt = Var(
    name='low_cld_amt',
    units=units.unitless,
    domain='atmos',
    description='Low cloud fraction.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
lwdn_sfc = Var(
    name='lwdn_sfc',
    alt_names=('rlds',),
    math_str="$R^{LW\downarrow_{sfc}$",
    description='All-sky downwelling longwave radiation at the surface.',
    domain='atmos',
    units=units.W_m2,
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
lwdn_sfc_clr = Var(
    name='lwdn_sfc_clr',
    alt_names=('rldscs',),
    units=units.W_m2,
    domain='atmos',
    description='Clear-sky downwelling longwave radiation at the surface.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
lwup_sfc = Var(
    name='lwup_sfc',
    alt_names=('rlus',),
    units=units.W_m2,
    domain='atmos',
    description='All-sky upwelling longwave radiation at the surface.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
lwup_sfc_clr = Var(
    name='lwup_sfc_clr',
    alt_names=('rluscs',),
    units=units.W_m2,
    domain='atmos',
    description='Clear-sky upwelling longwave radiation at the surface.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
hght = Var(
    name='hght',
    alt_names=('zg','height_half'),
    units=units.m,
    domain='atmos',
    description='Geopotential height.',
    def_time=True,
    def_vert='phalf',
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

hfull = Var(
    name='height_full',
    units=units.m,
    domain='atmos',
    description=('Geopotential height on full levels'),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

ice_wat = Var(
    name='ice_wat',
    units=units.specific_mass,
    domain='atmos',
    description='Cloud ice water specific humidity.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
liq_wat = Var(
    name='liq_wat',
    units=units.specific_mass,
    domain='atmos',
    description='Cloud liquid water specific humidity.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
mc = Var(
    name='mc',
    units=units.kg_m2_s1_mass,
    domain='atmos',
    description='Convective mass flux.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
mc_full = Var(
    name='mc_full',
    units=units.kg_m2_s1_mass,
    domain='atmos',
    description='Convective mass flux at full levels.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
mc_half = Var(
    name='mc_half',
    units=units.kg_m2_s1_mass,
    domain='atmos',
    description='Convective mass flux at half levels.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
mid_cld_amt = Var(
    name='mid_cld_amt',
    units=units.unitless,
    domain='atmos',
    description='Mid-level cloud fraction.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
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
olr_clr = Var(
    name='olr_clr',
    alt_names=('rlutcs',),
    units=units.W_m2,
    domain='atmos',
    description='Clear-sky outgoing longwave radiation at TOA.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
omega = Var(
    name='omega',
    alt_names=('wap',),
    units=units.Pa_s1,
    domain='atmos',
    description='Pressure vertical velocity.',
    def_time=True,
    def_vert='pfull',
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
precip = Var(
    name='precip',
    alt_names=('pr', 'pre'),
    units=units.kg_m2_s1,
    domain='atmos',
    description='Liquid precipitation reaching surface.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False,
    colormap='BrBG'
)
prec_conv = Var(
    name='prec_conv',
    alt_names=('prc',),
    units=units.kg_m2_s1,
    domain='atmos',
    description='Liquid precip reaching surface from convection scheme.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False,
    colormap='BrBG'
)
prec_ls = Var(
    name='prec_ls',
    units=units.kg_m2_s1,
    domain='atmos',
    description='Liquid precip reaching surface from large scale ascent.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False,
    colormap='BrBG'
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
pv = Var(
    name='pv',
    units=units.s1,
    domain='atmos',
    description='Potential vorticity',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
rh = Var(
    name='rh',
    alt_names=('hur',),
    units=units.unitless,
    domain='atmos',
    description='Relative humidity',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
rh_ref = Var(
    name='rh_ref',
    units=units.unitless,
    domain='atmos',
    description='Relative humidity at 2m above surface',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
shflx = Var(
    name='shflx',
    alt_names=('hfss',),
    units=units.W_m2,
    domain='atmos',
    description='Surface sensible heat flux into the atmosphere.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
slp = Var(
    name='slp',
    alt_names=('psl',),
    units=units.hPa,
    domain='atmos',
    description='Sea level pressure.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
snow_conv = Var(
    name='snow_conv',
    units=units.kg_m2_s1,
    domain='atmos',
    description='Snow reaching surface from convection scheme.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
snow_ls = Var(
    name='snow_ls',
    units=units.kg_m2_s1,
    domain='atmos',
    description='Snow reaching surface from large scale ascent.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
soil_liq = Var(
    name='soil_liq',
    units=units.kg_m2,
    domain='land',
    description='Soil liquid in each level of land model',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
soil_moisture = Var(
    name='soil_moisture',
    alt_names=('water', 'water_soil',),
    units=units.kg_m2,
    domain='land',
    description='Mass of water in land bucket',
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
sst = Var(
    name='sst',
    alt_names=('ts', 'SST'),
    units=units.K,
    domain='ocean',
    description='Sea surface temperature.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
swdn_sfc = Var(
    name='swdn_sfc',
    alt_names=('rsds',),
    units=units.W_m2,
    domain='atmos',
    description='All-sky downwelling shortwave radiation at the surface.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
swdn_sfc_clr = Var(
    name='swdn_sfc_clr',
    alt_names=('rsdscs',),
    units=units.W_m2,
    domain='atmos',
    description='Clear-sky downwelling shortwave radiation at the surface.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
swup_sfc = Var(
    name='swup_sfc',
    alt_names=('rsus',),
    units=units.W_m2,
    domain='atmos',
    description='All-sky upwelling shortwave radiation at the surface.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
swup_sfc_clr = Var(
    name='swup_sfc_clr',
    alt_names=('rsuscs',),
    units=units.W_m2,
    domain='atmos',
    description='Clear-sky upwelling shortwave radiation at the surface.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
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
swdn_toa_clr = Var(
    name='swdn_toa_clr',
    alt_names=('rsdtcs',),
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
swup_toa_clr = Var(
    name='swup_toa_clr',
    alt_names=('rsutcs',),
    units=units.W_m2,
    domain='atmos',
    description='Clear-sky upwelling shortwave radiation at TOA.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
t_surf = Var(
    name='t_surf',
    alt_names=('tas', 'tmp'),
    units=units.K,
    domain='atmos',
    description='Surface air temperature.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
tdt_conv = Var(
    name='tdt_conv',
    units=units.K_s1,
    domain='atmos',
    description='Convective heating rate.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False,
    valid_range=(-20, 20)
)
qdt_vdif = Var(
    name='qdt_vdif',
    units=units.kg_kg1_s1,
    domain='atmos',
    description='Time tendency of specific humidity',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
tdt_ls = Var(
    name='tdt_ls',
    units=units.K_s1,
    domain='atmos',
    description='Large-scale heating rate.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
tdt_lw = Var(
    name='tdt_lw',
    units=units.K_s1,
    domain='atmos',
    description='All-sky longwave heating rate.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
tdt_lw_clr = Var(
    name='tdt_lw_clr',
    units=units.K_s1,
    domain='atmos',
    description='Clear-sky longwave heating rate.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
tdt_sw = Var(
    name='tdt_sw',
    units=units.K_s1,
    domain='atmos',
    description='All-sky shortwave heating rate.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
tdt_sw_clr = Var(
    name='tdt_sw_clr',
    units=units.K_s1,
    domain='atmos',
    description='Clear-sky shortwave heating rate.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
tdt_vdif = Var(
    name='tdt_vdif',
    units=units.K_s1,
    domain='atmos',
    description='Temperature tendency from vertical diffusion.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
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
tot_cld_amt = Var(
    name='tot_cld_amt',
    alt_names=('clt',),
    units=units.unitless,
    domain='atmos',
    description='Total cloud fraction.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
ucomp = Var(
    name='ucomp',
    alt_names=('ua',),
    units=units.m_s1,
    domain='atmos',
    description='Eastward velocity.',
    def_time=True,
    def_vert='pfull',
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
u_ref = Var(
    name='u_ref',
    units=units.m_s1,
    domain='atmos',
    description='Eastward velocity at 2 meters above ground.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
vcomp = Var(
    name='vcomp',
    alt_names=('va',),
    units=units.m_s1,
    domain='atmos',
    description='Northward velocity.',
    def_time=True,
    def_vert='pfull',
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
v_ref = Var(
    name='v_ref',
    units=units.m_s1,
    domain='atmos',
    description='Northward velocity at 2 meters above ground.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
vort = Var(
    name='vort',
    units=units.s1_vort,
    domain='atmos',
    description='Vorticity',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)
wvp = Var(
    name='wvp',
    alt_names=('WVP', 'prw'),
    units=units.kg_m2,
    domain='atmos',
    description='Water vapor path',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False,
    colormap='Greys'
)
# Grid variables.
lat = Var(
    name='lat',
    units=units.latlon,
    description='Latitude',
    def_time=False,
    def_vert=False,
    def_lat=True,
    def_lon=False,
    in_nc_grid=True
)
lon = Var(
    name='lon',
    units=units.latlon,
    description='Longitude.',
    def_time=False,
    def_vert=False,
    def_lat=False,
    def_lon=True,
    in_nc_grid=True
)
level = Var(
    name='level',
    units=units.hPa,
    domain='atmos',
    description='Pressure level.',
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
sfc_area = Var(
    name='sfc_area',
    units=units.m2,
    domain=None,
    description='Grid surface area.',
    def_time=False,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

flux_t = Var(
    name='flux_t',
    units=units.W_m2,
    domain='atmos',
    description='Sensible heat flux from idealized model',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

flux_lhe = Var(
    name='flux_lhe',
    units=units.W_m2,
    domain='atmos',
    description='Latent heat flux',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=False,
    in_nc_grid=False
)

umse_vint = Var(
    name='umse_vint',
    domain='atmos',
    description=('u*mse integrated vertically in the idealized model'),
    units=units.m3_s3_v,
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

vmse_vint = Var(
    name='vmse_vint',
    domain='atmos',
    description=('v*mse integrated vertically in the idealized model'),
    units=units.m3_s3_v,
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

omega_mse_vint = Var(
    name='omega_mse_vint',
    domain='atmos',
    description=('omega*mse integrated vertically in the idealized model'),
    units=units.J_Pa_kg_s_v,
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)


umse = Var(
    name='umse',
    domain='atmos',
    description=('u*mse in idealized model'),
    units=units.m3_s3,
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

vmse = Var(
    name='vmse',
    domain='atmos',
    description=('v*mse in idealized model'),
    units=units.m3_s3,
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

omega_mse = Var(
    name='omega_mse',
    domain='atmos',
    description=('omega*mse in idealized model'),
    units=units.J_Pa_kg_s,
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)

# Calculations involving one or more model-native variables.

vert_avg_temp = Var(
    name='vert_avg_temp',
    domain='atmos',
    description=('vertical average temperature'),
    variables=(temp, dp),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.vert_avg_temp,
    units=units.K
)

dp_sigma = Var(
    name='dp_sigma',
    domain='atmos',
    description=('dp_sigma'),
    variables=(temp, dp),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    func=calcs.dp_sigma,
    units=units.Pa
)

net_sw = Var(
    name='net_sw',
    domain='atmos',
    description=('Net SW radiation at TOA'),
    variables=(swdn_toa, swup_toa),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.net_sw,
    units=units.W_m2
)

vcomp_mb = Var(
    name='vcomp_mb',
    domain='atmos',
    description=('vcomp mass balance'),
    variables=(vcomp, dp),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=False,
    func=calcs.correct_vcomp,
    units=units.m_s1,
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
mse_tendency = Var(
    name='mse_tendency',
    domain='atmos',
    description=('Moist Static Energy Tendency (dm/dt)'),
    variables=(tdt_lw, tdt_sw, tdt_vdif, qdt_vdif),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    func=calcs.mse,
    units=units.J_kg1_s1
)
msf = Var(
    name='msf',
    domain='atmos',
    description=('Eulerian meridional mass streamfunction'),
    variables=(vcomp, dp),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=False,
    func=calcs.msf,
    units=units.kg_s1
)

total_mse_flux_im = Var(
    name='total_mse_flux_im',
    domain='atmos',
    description=('Total MSE flux computed from inst data'),
    variables=(temp, sphum, vcomp, dp, p),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=False,
    func=calcs.total_mse_flux_im,
    units=units.W
)

msf_at_500_hPa = Var(
    name='msf_500',
    domain='atmos',
    description=('Eulerian meridional mass streamfunction evaluated at 500 hPa'),
    variables=(vcomp, dp, p),
    def_time=False,
    def_vert=False,
    def_lat=True,
    def_lon=False,
    func=calcs.msf_at_500_hPa,
    units=units.kg_s1
)

mmc_mse_flux = Var(
    name='msef_mmc',
    domain='atmos',
    description=('Mean meridional circulation component of the moist static energy flux.'),
    variables=(temp, sphum, vcomp, dp, p),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=False,
    func=calcs.mmc_mse_flux,
    units=units.W
)

gms = Var(
    name='gms',
    domain='atmos',
    description=('Gross Moist Stability as defined in SH 2015.'),
    variables=(temp, sphum, vcomp, dp, p),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=False,
    func=calcs.gms,
    units=units.K
)

msf_500_zeros = Var(
    name='msf_500_zeros',
    domain='atmos',
    description=('Zeros of the 500 hPa streamfunction'),
    variables=(vcomp, dp, p),
    def_time=False,
    def_vert=False,
    def_lat=True,
    def_lon=False,
    func=calcs.msf_500_zeros,
    units=units.latlon
)

pfull = Var(
    name='pfull',
    domain='atmos',
    description=('pressure at the level midpoints'),
    variables=(p),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    func=calcs.pfull,
    units=units.Pa
)

aht = Var(
    name='aht',
    domain='atmos',
    description=('atmospheric heat transport'),
    variables=(swdn_sfc, olr, lwdn_sfc, lwup_sfc, flux_t, flux_lhe, sfc_area),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=False,
    func=calcs.aht,
    units=units.W
)


eddy_mse_flux = Var(
    name='eddy_mse_flux',
    domain='atmos',
    description=('eddy mse flux'),
    variables=(temp, sphum, vcomp, swdn_sfc, olr, lwdn_sfc, lwup_sfc, flux_t, flux_lhe, sfc_area, dp, p),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=False,
    func=calcs.eddy_mse_flux,
    units=units.W
)

condensation_rain = Var(
    name='condensation_rain',
    domain='atmos',
    description=('condensation rain in idealized moist model'),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    units=units.kg_m2_s1
)

convection_rain = Var(
    name='convection_rain',
    domain='atmos',
    description=('convection rain in idealized moist model'),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    units=units.kg_m2_s1
)

precip_extrema = Var(
    name='precip_extrema',
    domain='atmos',
    description=('Locations of extreme zonal mean precipitation values'),
    variables=(condensation_rain, convection_rain),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=False,
    func=calcs.precip_extrema,
    units=units.latlon
)

precip_extrema_gcm = Var(
    name='precip_extrema_gcm',
    domain='atmos',
    description=('Locations of extreme zonal mean precipitation values'),
    variables=(precip,),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=False,
    func=calcs.precip_extrema_gcm,
    units=units.latlon
)

precip_im = Var(
    name='precip_im',
    domain='atmos',
    description=('Total precipitation rate (convective + condensation'),
    variables=(condensation_rain, convection_rain),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.total_precip,
    units=units.kg_m2_s1
)

dmv_dx_im = Var(
    name='dmv_dx_im',
    domain='atmos',
    description=('Zonal flux divergence of mse.'),
    variables=(umse,),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    func=calcs.mse_zonal_flux_divg_im,
    units=units.W
)

dmv_dx_v_im = Var(
    name='dmv_dx_v_im',
    domain='atmos',
    description=('Vertical integral of zonal flux divergence of mse.'),
    variables=(umse_vint,),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.mse_zonal_flux_divg_v_im,
    units=units.W
)

dmv_dy_v_im = Var(
    name='dmv_dy_v_im',
    domain='atmos',
    description=('Vertical integral of meridional flux divergence of mse.'),
    variables=(vmse_vint,),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.mse_merid_flux_divg_v_im,
    units=units.W
)

dmv_dy_im = Var(
    name='dmv_dy_im',
    domain='atmos',
    description=('Meridional flux divergence of mse.'),
    variables=(vmse,),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    func=calcs.mse_merid_flux_divg_im,
    units=units.W
)

dmv_dx = Var(
    name='dmv_dx',
    domain='atmos',
    description=('Zonal flux divergence of mse.'),
    variables=(ucomp, temp, sphum, dp, p),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    func=calcs.mse_zonal_flux_divg,
    units=units.W
)

dmv_dy = Var(
    name='dmv_dy',
    domain='atmos',
    description=('Meridional flux divergence of mse.'),
    variables=(vcomp, temp, sphum, dp, p),
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    func=calcs.mse_merid_flux_divg,
    units=units.W
)

Q_sfc_im = Var(
    name='Q_sfc_im',
    domain='atmos',
    description=('Heat flux at the surface in idealized model.'),
    variables=(swdn_sfc, lwdn_sfc, lwup_sfc, flux_t, flux_lhe),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.Q_sfc_im,
    units=units.W_m2
)

Q_toa_im = Var(
    name='Q_toa_im',
    domain='atmos',
    description=('Heat flux at the TOA in idealized model.'),
    variables=(swdn_sfc, olr),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.Q_toa_im,
    units=units.W_m2
)

Q_diff = Var(
    name='Q_diff',
    domain='atmos',
    description=('Net column heating'),
    variables=(swdn_toa, olr, swup_toa, swdn_sfc, lwdn_sfc, swup_sfc,
               lwup_sfc, shflx, evap),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.Q_diff,
    units=units.W_m2
)

aht_gcm = Var(
    name='aht_gcm',
    domain='atmos',
    description=('Meridional total atmospheric heat transport.'),
    variables=(swdn_toa, olr, swup_toa, swdn_sfc, lwdn_sfc, swup_sfc,
               lwup_sfc, shflx, evap),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.aht_gcm,
    units=units.W
)

aht_gcm_tend = Var(
    name='aht_gcm_tend',
    domain='atmos',
    description=('Meridional total atmospheric heat transport.'),
    variables=(swdn_toa, olr, swup_toa, swdn_sfc, lwdn_sfc, swup_sfc,
               lwup_sfc, shflx, evap, tdt_lw, tdt_sw, tdt_vdif, qdt_vdif, dp),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.aht_gcm_tend,
    units=units.W
)

S_net = Var(
    name='S_net',
    domain='atmos',
    description=('Net shortwave radiation.'),
    variables=(swdn_toa, swup_toa, swdn_sfc, swup_sfc),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.S_net,
    units=units.W_m2
)

L_net = Var(
    name='L_net',
    domain='atmos',
    description=('Net longwave radiation.'),
    variables=(olr, lwdn_sfc, lwup_sfc),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    func=calcs.L_net,
    units=units.W_m2
)

hb = Var(
    name='hb',
    domain='atmos',
    description=('Average moist static energy 20 to 40 hPa from sfc.'),
    variables=(temp, sphum, dp, p),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    units=units.J_kg1,
    func=calcs.hb
)

h_lower_trop = Var(
    name='h_lower_trop',
    domain='atmos',
    description=('Average moist static energy 20 to 500 hPa from sfc.'),
    variables=(temp, sphum, dp, p),
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    units=units.J_kg1,
    func=calcs.h_lower_trop
)

master_vars_list = [
    alb_sfc, cld_amt, divg, esf, evap, hght, high_cld_amt, ice_wat, liq_wat,
    low_cld_amt, lwdn_sfc, lwdn_sfc_clr, lwup_sfc, lwup_sfc_clr, mc, mc_full,
    mc_half, mid_cld_amt, olr, olr_clr, omega, precip, prec_conv, prec_ls, ps,
    pv, rh, rh_ref, shflx, slp, snow_conv, snow_ls, soil_liq, soil_moisture,
    sphum, sst, swdn_sfc, swdn_sfc_clr, swup_sfc, swup_sfc_clr, swdn_toa,
    swdn_toa_clr, swup_toa, swup_toa_clr, t_surf, tdt_conv, tdt_ls, tdt_lw,
    tdt_lw_clr, tdt_sw, tdt_sw_clr, tdt_vdif, temp, tot_cld_amt, ucomp, u_ref,
    v_ref, vcomp, vort, wvp, lat, lon, level, pk, bk, sfc_area, gz, dse, mse, msf, pfull,
    msf_at_500_hPa, mmc_mse_flux, gms, msf_500_zeros, aht, eddy_mse_flux, condensation_rain, convection_rain,
    precip_extrema, precip_im, precip_extrema_gcm, hb, h_lower_trop
]

class variables(object):
    def __init__(self, vars_list):
        for var in vars_list:
            setattr(self, var.name, var)
