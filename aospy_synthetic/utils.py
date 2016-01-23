"""aospy.utils: utility functions for the aospy module."""
import logging
import warnings

from infinite_diff import FiniteDiff
import numpy as np
import pandas as pd
import xray

from .__config__ import (PHALF_STR, PFULL_STR, PLEVEL_STR, TIME_STR,
                         LAT_STR, LON_STR, user_path)


def coord_to_new_dataarray(arr, dim):
    """Create a DataArray comprising the coord for the specified dim.

    Useful, for example, when wanting to resample in time, because at least
    for xray 0.6.0 and prior, the `resample` method doesn't work when applied
    to coords.  The DataArray returned by this method lacks that limitation.
    """
    return xray.DataArray(arr[dim].values, coords=[arr[dim].values],
                          dims=[dim])


def apply_time_offset(time, months=0, days=0, hours=0):
    """Apply the given offset to the given time array.

    This is useful for GFDL model output of instantaneous values.  For example,
    3 hourly data postprocessed to netCDF files spanning 1 year each will
    actually have time values that are offset by 3 hours, such that the first
    value is for 1 Jan 03:00 and the last value is 1 Jan 00:00 of the
    subsequent year.  This causes problems in xray, e.g. when trying to group
    by month.  It is resolved by manually subtracting off those three hours,
    such that the dates span from 1 Jan 00:00 to 31 Dec 21:00 as desired.
    """
    return (pd.to_datetime(time.values) +
            pd.tseries.offsets.DateOffset(months=months, days=days,
                                          hours=hours))


def monthly_mean_ts(arr):
    """Convert a sub-monthly time-series into one of monthly means."""
    if isinstance(arr, (float, int, Constant)):
        return arr
    try:
        return arr.resample('1M', TIME_STR, how='mean')
    except KeyError:
        raise KeyError("`{}` lacks time dimension with "
                       "label `{}`.".format(arr, TIME_STR))


def monthly_mean_at_each_ind(arr_mon, arr_sub):
    """Copy monthly mean over each time index in that month."""
    time = arr_mon[TIME_STR]
    start = time.indexes[TIME_STR][0].replace(day=1, hour=0)
    end = time.indexes[TIME_STR][-1]
    new_indices = pd.DatetimeIndex(start=start, end=end, freq='MS')
    arr_new = arr_mon.reindex(time=new_indices, method='backfill')
    return arr_new.reindex_like(arr_sub, method='pad')


def load_user_data(name):
    """Load user data from aospy_path for given module name.

    File must be located in the `aospy_path` directory and be the same name
    as the desired aospy module subpackage, namely one of `regions`, `calcs`,
    `variables`, and `projects`.
    """
    import imp
    return imp.load_source(
        name, '/'.join([user_path, name, '__init__.py']).replace('//', '/')
    )


def robust_bool(obj):
    try:
        return bool(obj)
    except ValueError:
        return obj.any()


def get_parent_attr(obj, attr, strict=False):
    """
    Check if the object has the given attribute and it is non-empty.  If not,
    check each parent object for the attribute and use the first one found.
    """
    attr_val = getattr(obj, attr, False)
    if robust_bool(attr_val):
        return attr_val

    else:
        for parent in ('parent', 'var', 'run', 'model', 'proj'):
            parent_obj = getattr(obj, parent, False)
            if parent_obj:
                return get_parent_attr(parent_obj, attr, strict=strict)

        if strict:
            raise AttributeError('Attribute %s not found in parent of %s'
                                 % (attr, obj))
        else:
            return None


def dict_name_keys(objs):
    """Create dict whose keys are the 'name' attr of the objects."""
    assert isinstance(objs, (tuple, list, dict, set))
    if isinstance(objs, (tuple, list, set)):
        try:
            return {obj.name: obj for obj in objs}
        except AttributeError as e:
            raise AttributeError(e)
    return objs
