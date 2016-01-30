"""Test library of functions for use in aospy.
"""

from aospy.constants import (c_p, L_v, R_a)
from aospy.utils import (to_pascal, dp_from_ps, vert_coord_name)
from aospy_synthetic.__config__ import PFULL_STR


def dp(ps, bk, pk, arr):
    """Pressure thickness of hybrid coordinate levels from surface pressure."""
    return dp_from_ps(bk, pk, ps, arr[PFULL_STR])


def net_sw_toa(swdn_toa, swup_toa):
    """Net shortwave radiation at TOA"""
    return swdn_toa - swup_toa


def pfull(p):
    """Returns the pressure at level midpoints"""
    return to_pascal(p)


def gz(temp, sphum, dp, p):
    """Geopotential calculated from hydrostatic relation."""
    integrand = (R_a.value * (1.0 + 0.608 * sphum) * temp) / p
    integrand = integrand * dp
    gz = integrand.copy(deep=True)
    v = vert_coord_name(dp)
    print(v)
    for k in range(len(dp[v])):
        gz[{v: k}] = integrand.isel(**{v: slice(k, None)}).sum(dim=v)
    return gz


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
