"""My library of functions for use in aospy.

Except for helper functions, all assume input variables with the first axis
denoting time and the subsequent axes either (pressure, lat, lon) or, if not
vertically defined, (lat, lon).
"""
import numpy as np
import xray

from aospy.constants import (c_p, grav, kappa, L_f, L_v, r_e, Omega, p_trip,
                             T_trip, c_va, c_vv, c_vl, c_vs, R_a, R_v,
                             E_0v, E_0s, s_0v, s_0s)
from aospy.utils import (level_thickness, to_pascal, to_radians,
                         integrate, int_dp_g, dp_from_ps, vert_coord_name)


def dp(ps, bk, pk, arr):
    """Pressure thickness of hybrid coordinate levels from surface pressure."""
    return dp_from_ps(bk, pk, ps, arr[PFULL_STR])

# Take advantage of Spencer Hill's numerical functions.
from numerics import (
    fwd_diff1,
    fwd_diff2,
    # cen_diff2,
    # cen_diff4,
    upwind_scheme,
    latlon_deriv_prefactor,
    wraparound_lon,
    d_dx_from_latlon,
    d_dy_from_lat,
    d_dx_at_const_p_from_eta,
    d_dy_at_const_p_from_eta,
    d_dx_of_vert_int,
    d_dy_of_vert_int,
    d_dp_from_p,
    d_dp_from_eta
)

from interpolation import (
    zeros_xray,
    interp1d_pt_xray,
    interp1d_xray
)


def dp_sigma(temp, dp):
    return dp

def net_sw(swdn_toa, swup_toa):
    """Net shortwave radiation at TOA"""
    return swdn_toa - swup_toa


def pfull(p):
    """ Returns the pressure at the level midpoints."""
    return to_pascal(p)


def gz(temp, sphum, dp, p):
    integrand = (R_a.value * (1.0 + 0.608 * sphum) * temp) / p
    integrand = integrand * dp
    gz = integrand.copy(deep=True)
    v = vert_coord_name(dp)
    print(v)
    for k in range(len(dp[v])):
        gz[{v: k}] = integrand.isel(**{v: slice(k, None)}).sum(dim=v)
    return gz


def vert_avg_temp(temp, dp):
    ones = np.ones(temp.values.shape)
    copy = temp.copy(deep=True)
    copy.values = ones
    return int_dp_g(temp, dp) / int_dp_g(copy, dp)


def dse(temp, sphum, dp, p):
    """ Returns the dry static energy at each gridbox.

    $s = c_p T + gz$
    """
    return (c_p.value * temp + gz(temp, sphum, dp, p))


def mse(temp, sphum, dp, p):
    """ Returns the moist static energy at each gridbox.

    $m = c_p T + L_v q + gz$

    Parameters
    ----------
    temp : array
        temperature
    sphum : array
        specific humidity
    p : array
        pressure at sigma levels
    dp : array
        thickness of pressure levels

    Returns
    -------
    mse : array
        moist static energy
    """
    return (dse(temp, sphum, dp, p) + L_v.value * sphum)


def tdt_moist_diabatic(tdt_lw, tdt_sw, tdt_vdif):
    """Net moist diabatic heating rate."""
    return tdt_lw + tdt_sw + tdt_vdif


def mse_tendency(tdt_lw, tdt_sw, tdt_vdif, qdt_vdif):
    """Net MSE forcing."""
    return ((c_p.value * tdt_moist_diabatic(tdt_lw, tdt_sw, tdt_vdif)) +
            (L_v.value * qdt_vdif))


def hb(temp, sphum, dp, p):
    """Average MSE between 20 and 40 hPa from surface.
    From Shekhar and Boos (2016).

    Parameters
    ----------
    temp : array
        temperature
    sphum : array
        specific humidity
    p : array
        pressure at sigma levels
    dp : array
        thickness of pressure levels

    Returns
    -------
    mse : array
        moist static energy
    """
    p = to_pascal(p)
    dp = to_pascal(dp)
    dp_sfc = p.isel(pfull=-1) - p
    mask = (dp_sfc >= 2000.0) & (dp_sfc < 4000.0)
    mse_ = mse(temp, sphum, dp, p)
    return (mse_ * dp).where(mask).sum('pfull') / dp.where(mask).sum('pfull')


def h_lower_trop(temp, sphum, dp, p):
    """Average MSE between 20 and 500 hPa from surface.
    From Shekhar and Boos (2016).

    Parameters
    ----------
    temp : array
        temperature
    sphum : array
        specific humidity
    p : array
        pressure at sigma levels
    dp : array
        thickness of pressure levels

    Returns
    -------
    mse : array
        moist static energy
    """
    p = to_pascal(p)
    dp = to_pascal(dp)
    dp_sfc = p.isel(pfull=-1) - p
    mask = (dp_sfc >= 2000.0) & (dp_sfc < 50000.0)
    mse_ = mse(temp, sphum, dp, p)
    return (mse_ * dp).where(mask).sum('pfull') / dp.where(mask).sum('pfull')


def msf(vcomp, dp):
    """ Returns the mean meridional mass streamfunction. We take
    the zonal mean first and then take the time mean.
    """
    try:
        dp = dp.mean('lon')
    except:
        pass
    dp = to_pascal(dp)
    v = vert_coord_name(dp)

    msf_ = vcomp.mean('lon').copy(deep=True)
    integrand = dp * vcomp.mean('lon')
    for k in range(len(dp[v])):
        msf_[{v: k}] = integrand.isel(**{v: slice(k, None)}).sum(dim=v)
    msf_ *= 2. * r_e.value * np.pi * np.cos(np.deg2rad(vcomp.lat)) / grav.value
    return msf_


def msf_at_500_hPa(vcomp, dp, p):
    """ Returns the time mean meridional mass streamfunction at 500 hPa.
    Use this only in post-processing.
    """
    def eval_at_index(x, axis, indices=None):
        """
        Parameters
        ----------
        x : array
            full numpy array to apply function to
        axis : int
            axis to collapse
        indices : array
            array containing indices in each column you would like to
            evaluate at (to collapse the array)
        """
        collapse_dim_len = x.shape[axis]
        x = np.swapaxes(x, -1, axis)
        reduced_shape = x.shape[:-1]
        x = np.reshape(x, (-1, collapse_dim_len))
        inds = np.reshape(indices.values, (-1,))
        rows = np.array(np.arange(x.shape[0]), dtype=np.intp)
        cols = inds.astype(np.intp)
        return np.reshape(x[rows, cols], reduced_shape)

    v = vert_coord_name(dp)
    try:
        p = p.mean('lon')
    except:
        pass

    p = to_pascal(p)
    to_min = np.abs(p/100. - 500)
    try:
        to_min = to_min.mean('time')
    except ValueError:
        pass
    inds = to_min.argmin(v)
    msf_ = msf(vcomp, dp)
    msf_ = msf_.mean('time') # Take the time mean beforehand.
    return msf_.reduce(eval_at_index, dim=v, indices=inds)


def correct_vcomp(vcomp, dp):
    """
    Applies the SH 2015 correction to the meridional velocity to ensure mass
    balance in the MSE flux.
    """
    vcomp = vcomp.mean('lon')
    vplus = vcomp.copy(deep=True)
    vminus = vcomp.copy(deep=True)
    vplus.values[vcomp.values < 0] = 0.
    vminus.values[vcomp.values > 0] = 0.

    try:
        dp = dp.mean('lon')
    except:
        pass
    factor = -1. * int_dp_g(vplus, dp) / int_dp_g(vminus, dp)
    return (vplus + factor * vminus)


def total_mse_flux_im(temp, sphum, vcomp, dp, p):
    """
    Computes the full mse transport in the zonal mean sense for a specific
    timestep in the idealized moist model.
    """
    # Take the zonal mean of the mse.
    mse_ = (c_p.value * temp) + (L_v.value * sphum) + gz(temp, sphum, dp, p)
    mse_ = mse_.mean('lon')
    return 2.*np.pi*r_e.value*np.cos(np.deg2rad(mse_.lat))*int_dp_g(mse_ * correct_vcomp(vcomp, dp), dp.mean('lon'))


# Deprecated.
def mmc_mse_flux(temp, sphum, vcomp, dp, p):
    """
    Computes the mean meridional circulation component of the MSE flux.
    This should again be a post-processing step.
    """
    mse_ = mse(temp, sphum, dp, p).mean('lon').mean('time')
    v = correct_vcomp(vcomp, dp).mean('time')
    try:
        dp = dp.mean('lon')
    except:
        pass
    return 2. * np.pi * r_e.value * np.cos(np.deg2rad(temp.lat)) * int_dp_g(mse_*v, dp)


# Deprecated.
def signed_max(data, dim):
    """
    Returns the signed maximum value along a given axis.
    """
    def max_(x, axis):
        """
        Returns the signed maximum value along a given axis.
        """
        bools = (-1. * x).max(axis=axis) > x.max(axis=axis)
        return (bools * x.min(axis=axis) + np.invert(bools) * x.max(axis=axis))
    return data.reduce(max_, dim=dim)


# Deprecated.
def gms(lat, temp, sphum, vcomp, dp, p):
    """
    Returns the gross moist stability as defined in SH 2015.
    """
    v = vert_coord_name(dp)
    return mmc_mse_flux(lat, temp, sphum, vcomp, dp, p) / (c_p.value * signed_max(msf(vcomp, dp), v))


# Deprecated.
def msf_500_zeros(vcomp, dp, p):
    """
    Returns the linearly interpolated zeros of the 500 mb meridional mass
    streamfunction. These can later be interpreted as Hadley Cell boundaries
    (but there will sometimes be more than three).
    This is more easily accomplished with the new interpolation module.
    """
    # Find the streamfunction at 500 mb.
    msf_ = msf_at_500_hPa(vcomp, dp, p)

    # Now find the zeros.
    signs = msf_.copy(deep=True)
    msf_val = np.array(msf_.values)
    signs.values = np.sign(msf_val)

    # Take two diffs, one preserving lower, the other preserving upper for the lat coord.
    # This leaves everything but the values surrounding the zero masked.
    mask = signs.diff('lat', label='lower') != 0
    mask = mask.diff('lat', label='upper')

    # Initialize the mask as all False's.
    mask_full = msf_.copy(deep=True)
    mask_full.values = np.zeros(msf_.values.shape).astype(bool)
    mask_full[dict(lat=slice(1,-1))] = mask

    # Mask msf_ appropriately.
    msf_.values= np.ma.masked_array(msf_.values, np.invert(mask_full))

    # For whatever reason you cannot do a diff on a coordinate. Thus we create
    # a DataArray with the lat values renamed as a new variable.
    lat_diff = xray.DataArray(msf_['lat'].values, coords=[msf_['lat'].values],
                                      dims=['lat'])
    b = msf_.diff('lat', label='lower') / lat_diff.diff('lat', label='lower')
    return (msf_['lat'][dict(lat=slice(None,-1))] * b - msf_[dict(lat=slice(None,-1))])/ b


def Q_toa_im(swdn_sfc, olr):
    """
    Heat flux at the top of atmosphere in the idealized moist model.
    """
    return swdn_sfc - olr


def Q_sfc_im(swdn_sfc, lwdn_sfc, lwup_sfc, flux_t, flux_lhe):
    """
    Heat flux at the surface.
    """
    return swdn_sfc + lwdn_sfc - lwup_sfc - flux_t - flux_lhe


def aht(swdn_sfc, olr, lwdn_sfc, lwup_sfc, flux_t, flux_lhe, sfc_area):
    """
    Atmospheric heat transport. Computed from radiative fluxes.
    Procedure adapted from SH's library.
    Parameters
    ----------
    """
    Q_diff_ = Q_toa_im(swdn_sfc, olr) - Q_sfc_im(swdn_sfc,
                                                 lwdn_sfc,
                                                 lwup_sfc,
                                                 flux_t,
                                                 flux_lhe)
    global_mean = (sfc_area * Q_diff_).sum('lat').sum('lon') / sfc_area.sum('lat').sum('lon')
    zonal_integral = (sfc_area * (Q_diff_ - global_mean)).sum('lon')
    # Now do a cumulative sum in the latitude dimension.
    aht_ = zonal_integral.copy(deep=True)
    for j in range(zonal_integral['lat'].values.shape[0]):
        aht_[dict(lat=j)] = zonal_integral.isel(lat=slice(None, j)).sum('lat')
    return aht_


def eddy_mse_flux(temp, sphum, vcomp, swdn_sfc, olr,
                  lwdn_sfc, lwup_sfc, flux_t, flux_lhe, sfc_area, dp, p):
    """Eddy contribution to the northward MSE flux.
    Defined as a residual from the aht.
    """
    return aht(swdn_sfc,
               olr,
               lwdn_sfc,
               lwup_sfc,
               flux_t,
               flux_lhe,
               sfc_area).mean('time') - mmc_mse_flux(temp, sphum, vcomp, dp, p)


def precip_extrema(condensation_rain, convection_rain):
    """Find the locations of precipitation extrema in the zonal mean using an
    interpolation method.
    """
    # Take the zonal and time mean of the total.
    total_rain = (condensation_rain + convection_rain).mean('lon').mean('time')
    return zeros_xray(d_dy_from_lat(total_rain, r_e, vec_field=False),
                      'lat')


def precip_extrema_gcm(precip):
    """Find the locations of precipitation extrema in the zonal mean using an
    interpolation method.
    """
    # NOTE THIS FUNCTION IS BAD. It takes the mean in time to early.
    total_rain = precip.mean('lon').mean('time')
    return zeros_xray(d_dy_from_lat(total_rain, r_e, vec_field=False),
                      'lat', 360)


def total_precip(condensation_rain, convection_rain):
    """
    Returns the total precipitation rate at a gridbox.
    """
    return condensation_rain + convection_rain


def d_dtheta(field, div=False):
    """
    Computes the theta derivative using the central difference method.
    Theta is the latitude angle in spherical coordinates.
    """
    if div:
        field *= np.cos(np.deg2rad(field.lat))

    upper_bound = field.isel(lat=slice(2,None))
    upper_bound['lat'] = field['lat'].isel(lat=slice(1,-1))
    lower_bound = field.isel(lat=slice(None,-2))
    lower_bound['lat'] = field['lat'].isel(lat=slice(1,-1))

    dtheta_v = field['lat'].isel(lat=slice(2,None)) - field.lat.isel(lat=slice(None,-2)).values
    dtheta = xray.DataArray(np.deg2rad(dtheta_v), {'lat' : field.lat.isel(lat=slice(1,-1)).values})

    dfield = field.copy(deep=True) # Make a copy for easy dimension preservation.
    dfield[dict(lat=slice(1,-1))] = upper_bound - lower_bound
    #dfield[dict(lat=0)] =

    return (1./(r_e.value * np.cos(np.deg2rad(field.lat.isel(lat=slice(1,-1)))))) * (dfield / dtheta)


def d_dphi(field):
    """
    Computes the longitude derivative using the central difference method.
    """
    upper_bound = field.isel(lon=slice(2,None))
    upper_bound['lon'] = field['lon'].isel(lon=slice(1,-1))
    lower_bound = field.isel(lon=slice(None,-2))
    lower_bound['lon'] = field['lon'].isel(lon=slice(1,-1))

    dphi_v = field['lon'].isel(lon=slice(2,None)).values - field['lon'].isel(lon=slice(None,-2)).values
    dphi = xray.DataArray(dphi_v, {'lon' : field['lon'].isel(lon=slice(1,-1)).values}) * np.pi / 180.0

    dfield = upper_bound - lower_bound
    return (1.0 / r_e.value) * dfield / dphi


def d_dp(field, pf):
    """ Computes the pressure derivative of a quantity using a central difference.
    """
    # Centered difference in the middle.
    lower_bound = field.isel(pfull=slice(2, None))
    lower_bound['pfull'] = field['pfull'].isel(pfull=slice(1,-1))
    upper_bound = field.isel(pfull=slice(None, -2))
    upper_bound['pfull'] = field['pfull'].isel(pfull=slice(1,-1))

    dp_u = pf.isel(pfull=slice(None, -2))
    dp_u['pfull'] = field['pfull'].isel(pfull=slice(1,-1))
    dp_l = pf.isel(pfull=slice(2, None))
    dp_l['pfull'] = field['pfull'].isel(pfull=slice(1,-1))

    dp = dp_u - dp_l

    dfield = field.copy(deep=True)
    dfield[dict(pfull=slice(1,-1))] = (upper_bound - lower_bound) / dp

    #print(dp)
    dfield[dict(pfull=0)].values = (field[dict(pfull=1)].values - field[dict(pfull=0)].values) /\
                                    (pf[dict(pfull=1)].values - pf[dict(pfull=0)].values)
    dfield[dict(pfull=-1)].values = (field[dict(pfull=-1)].values - field[dict(pfull=-2)].values) /\
                                    (pf[dict(pfull=-1)].values - pf[dict(pfull=-2)].values)

    return dfield


def div_v(ucomp, vcomp, omega, p):
    """
    Computes the divergence of the velocity field in spherical coords.
    """
    return d_dphi(ucomp) + d_dtheta(vcomp, div=True) + d_dp(omega, p)


def field_merid_flux_divg(arr, v, radius):
    """
    Meridional flux divergence of a field.
    """
    return d_dy_from_lat(v * arr, radius, vec_field=True)


def field_zonal_flux_divg(arr, u, radius):
    """
    Zonal flux divergence of a field.
    """
    return d_dx_from_latlon(u * arr, radius)


def field_vert_flux_divg(arr, omega, p):
    """
    Vertical flux divergence of a field.
    """
    return d_dp_from_p(omega * arr, p)


def mse_zonal_flux_divg(u, temp, sphum, dp, p):
    mse_ = mse(temp, sphum, dp, p)
    return field_zonal_flux_divg(mse_, u, r_e.value)


def mse_merid_flux_divg(v, temp, sphum, dp, p):
    mse_ = mse(temp, sphum, dp, p)
    return field_merid_flux_divg(mse_, v, r_e.value)


def mse_zonal_flux_divg_im(umse):
    return d_dx_from_latlon(umse, r_e.value)


def mse_merid_flux_divg_im(vmse):
    return d_dy_from_lat(vmse, r_e.value, vec_field=True)


def mse_zonal_flux_divg_v_im(umse_vint):
    return d_dx_from_latlon(umse_vint, r_e.value)


def mse_merid_flux_divg_v_im(vmse_vint):
    return d_dy_from_lat(vmse_vint, r_e.value, vec_field=True)


def Q_diff(swdn_toa, olr, swup_toa, swdn_sfc, lwdn_sfc, swup_sfc, lwup_sfc,
           shflx, evap):
    """Net radiation at TOA"""
    return (swdn_toa - olr - swup_toa - (swdn_sfc + lwdn_sfc - swup_sfc -
                                         lwup_sfc - shflx - (L_v * evap)))


def aht_gcm(swdn_toa, olr, swup_toa, swdn_sfc, lwdn_sfc, swup_sfc, lwup_sfc,
            shflx, evap):
    """
    Atmospheric heat transport. Computed from radiative fluxes.
    Procedure adapted from SH's library.
    Parameters
    ----------
    """
    Q_diff_ = Q_diff(swdn_toa, olr, swup_toa, swdn_sfc, lwdn_sfc, swup_sfc,
                     lwup_sfc, shflx, evap)
    sfc_area = swdn_toa.sfc_area
    global_mean = (sfc_area * Q_diff_).sum('lat').sum('lon') /\
        sfc_area.sum('lat').sum('lon')
    zonal_integral = (sfc_area * (Q_diff_ - global_mean)).sum('lon')
    # Now do a cumulative sum in the latitude dimension.
    aht_ = zonal_integral.copy(deep=True)
    for j in range(zonal_integral['lat'].values.shape[0]):
        aht_[dict(lat=j)] = zonal_integral.isel(lat=slice(None, j)).sum('lat')
    return aht_


def aht_gcm_tend(swdn_toa, olr, swup_toa, swdn_sfc, lwdn_sfc, swup_sfc, lwup_sfc,
            shflx, evap, tdt_lw, tdt_sw, tdt_vdif, qdt_vdif, dp):
    """
    Atmospheric heat transport. Computed from radiative fluxes.
    Procedure adapted from SH's library.
    Parameters
    ----------
    """
    Q_diff_ = Q_diff(swdn_toa, olr, swup_toa, swdn_sfc, lwdn_sfc, swup_sfc,
                     lwup_sfc, shflx, evap)
    mse_tendency_ = int_dp_g(mse_tendency(tdt_lw, tdt_sw, tdt_vdif, qdt_vdif), dp)
    Q_diff = Q_diff - mse_tendency
    sfc_area = swdn_toa.sfc_area
    global_mean = (sfc_area * Q_diff_).sum('lat').sum('lon') /\
        sfc_area.sum('lat').sum('lon')
    zonal_integral = (sfc_area * (Q_diff_ - global_mean)).sum('lon')
    # Now do a cumulative sum in the latitude dimension.
    aht_ = zonal_integral.copy(deep=True)
    for j in range(zonal_integral['lat'].values.shape[0]):
        aht_[dict(lat=j)] = zonal_integral.isel(lat=slice(None, j)).sum('lat')
    return aht_


def S_net(swdn_toa, swup_toa, swdn_sfc, swup_sfc):
    """Net shortwave radiation in full GCM"""
    return swdn_toa + swup_sfc - swup_toa - swdn_sfc


def L_net(olr, lwdn_sfc, lwup_sfc):
    """Net longwave radiation in full GCM"""
    return lwup_sfc - olr - lwdn_sfc
