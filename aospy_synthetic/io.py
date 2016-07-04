"""io.py: utility methods used internally by aospy for input/output, etc."""
import numpy as np


def _data_in_label(intvl_in, dtype_in_time, dtype_in_vert=False):
    """Create string label specifying the input data of a calculation."""
    intvl_lbl = intvl_in
    time_lbl = dtype_in_time
    lbl = '_'.join(['from', intvl_lbl, time_lbl]).replace('__', '_')
    vert_lbl = dtype_in_vert if dtype_in_vert else False
    if vert_lbl:
        lbl = '_'.join([lbl, vert_lbl]).replace('__', '_')
    return lbl


def _data_out_label(time_intvl, dtype_time, dtype_vert=False):
    intvl_lbl = _time_label(time_intvl, return_val=False)
    time_lbl = dtype_time
    lbl = '.'.join([intvl_lbl, time_lbl]).replace('..', '.')
    vert_lbl = dtype_vert if dtype_vert else False
    if vert_lbl:
        lbl = '.'.join([lbl, vert_lbl]).replace('..', '.')
    return lbl


def _ens_label(ens_mem):
    """Create label of the ensemble member for aospy data I/O."""
    if ens_mem in (None, False):
        return ''
    elif ens_mem == 'avg':
        return 'ens_mean'
    else:
        return 'mem' + str(ens_mem + 1)


def _yr_label(yr_range):
    """Create label of start and end years for aospy data I/O."""
    assert yr_range is not None, "yr_range is None"
    if yr_range[0] == yr_range[1]:
        return '{:04d}'.format(yr_range[0])
    else:
        return '{:04d}-{:04d}'.format(*yr_range)


def _time_label(intvl, return_val=True):
    """Create time interval label for aospy data I/O."""
    # Monthly labels are 2 digit integers: '01' for jan, '02' for feb, etc.
    if type(intvl) in [list, tuple, np.ndarray] and len(intvl) == 1:
        label = '{:02}'.format(intvl[0])
        value = np.array(intvl)
    elif type(intvl) == int and intvl in range(1, 13):
        label = '{:02}'.format(intvl)
        value = np.array([intvl])
    # Seasonal and annual time labels are short strings.
    else:
        labels = {'jfm': (1, 2, 3), 'fma': (2, 3, 4), 'mam': (3,  4,  5),
                  'amj': (4, 5, 6), 'mjj': (5, 6, 7), 'jja': (6,  7,  8),
                  'jas': (7, 8, 9), 'aso': (8, 9,10), 'son': (9, 10, 11),
                  'ond':(10,11,12), 'ndj': (11,12,1), 'djf': (1,  2, 12),
                  'jjas': (6,7,8,9), 'djfm': (12, 1, 2, 3),
                  'ann': range(1,13)}
        for lbl, vals in labels.items():
            if intvl == lbl or set(intvl) == set(vals):
                label = lbl
                value = np.array(vals)
                break
    if return_val:
        return label, value
    else:
        return label
