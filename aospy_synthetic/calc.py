"""calc.py: classes for performing specified calculations on aospy data"""
from __future__ import print_function
import os
import time

from .var import Var
from .io import _data_in_label, _data_out_label, _ens_label, _yr_label
from .timedate import TimeManager
from .utils import get_parent_attr
#from aospy_db import create_session, get_or_create
#from aospy_db import Calc as dbCalc
#from aospy_db import Var as dbVar


dp = Var(
    name='dp',
    units='Pa',
    domain='atmos',
    description='Pressure thickness of model levels.',
    def_time=True,
    def_vert=True,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False,
)
ps = Var(
    name='ps',
    units='Pa',
    domain='atmos',
    description='Surface pressure.',
    def_time=True,
    def_vert=False,
    def_lat=True,
    def_lon=True,
    in_nc_grid=False
)


class CalcInterface(object):
    """Interface to Calc class."""
    def _set_data_in_attrs(self):
        for attr in ('data_in_start_date',
                     'data_in_end_date',
                     'default_date_range',
                     'data_in_dur',
                     'data_in_direc',
                     'data_in_files',
                     'data_in_dir_struc',
                     'ens_mem_prefix',
                     'ens_mem_ext',
                     'idealized'):
            attr_val = tuple([get_parent_attr(rn, attr, strict=False)
                              for rn in self.run])
            setattr(self, attr, attr_val)

    def __init__(self, proj=None, model=None, run=None, ens_mem=None, var=None,
                 date_range=None, region=None, intvl_in=None, intvl_out=None,
                 dtype_in_time=None, dtype_in_vert=None, dtype_out_time=None,
                 dtype_out_vert=None, level=None, chunk_len=False,
                 verbose=True):
        """Create the CalcInterface object with the given parameters."""
        if run not in model.runs.values():
            raise AttributeError("Model '{}' has no run '{}'.  Calc object "
                                 "will not be generated.".format(model, run))
        # 2015-10-13 S. Hill: This tuple-izing is for support of calculations
        # where variables come from different runs.  However, this is a very
        # fragile way of implementing that functionality.  Eventually it will
        # be replaced with something better.
        proj = tuple([proj])
        model = tuple([model])
        if not isinstance(run, (list, tuple)):
            run = tuple([run])
        # Make tuples the same length.
        if len(proj) == 1 and (len(model) > 1 or len(run) > 1):
            proj = tuple(list(proj)*len(run))
        if len(model) == 1 and len(run) > 1:
            model = tuple(list(model)*len(run))

        self.proj = proj
        self.model = model
        self.run = run

        self._set_data_in_attrs()

        self.proj_str = '_'.join(set([p.name for p in self.proj]))
        self.model_str = '_'.join(set([m.name for m in self.model]))
        run_names = [r.name for r in self.run]
        self.run_str = '_'.join(set(run_names))
        self.run_str_full = '_'.join(run_names)

        self.var = var
        self.name = self.var.name
        self.domain = self.var.domain
        self.def_time = self.var.def_time
        self.def_vert = self.var.def_vert
        self.verbose = verbose

        try:
            self.function = self.var.func
        except AttributeError:
            self.function = lambda x: x
        if getattr(self.var, 'variables', False):
            self.variables = self.var.variables
        else:
            self.variables = (self.var,)

        self.ens_mem = ens_mem
        self.level = level
        self.intvl_in = intvl_in
        self.intvl_out = intvl_out
        self.dtype_in_time = dtype_in_time
        self.dtype_in_vert = dtype_in_vert
        self.ps = ps
        if isinstance(dtype_out_time, (list, tuple)):
            self.dtype_out_time = tuple(dtype_out_time)
        else:
            self.dtype_out_time = tuple([dtype_out_time])
        self.dtype_out_vert = dtype_out_vert
        self.region = region

        self.months = TimeManager.month_indices(intvl_out)
        self.start_date = TimeManager.str_to_datetime(date_range[0])
        self.end_date = TimeManager.str_to_datetime(date_range[-1])
        tm = TimeManager(self.start_date, self.end_date, intvl_out)
        self.date_range = tm.create_time_array()

        self.start_date_xray = tm.apply_year_offset(self.start_date)
        self.end_date_xray = tm.apply_year_offset(self.end_date)


class Calc(object):
    """Class for executing, saving, and loading a single computation."""

    ARR_XRAY_NAME = 'aospy_result'

    def __str__(self):
        """String representation of the object."""
        return "Calc object: " + ', '.join(
            (self.name, self.proj_str, self.model_str, self.run_str_full)
        )

    __repr__ = __str__

    def _dir_scratch(self):
        """Create string of the data directory on the scratch filesystem."""
        ens_label = _ens_label(self.ens_mem)
        return os.path.join('/work', os.getenv('USER'), self.proj_str,
                            self.model_str, self.run_str, ens_label,
                            self.name)

    def _dir_archive(self):
        """Create string of the data directory on the archive filesystem."""
        ens_label = _ens_label(self.ens_mem)
        return os.path.join('/archive', os.getenv('USER'),
                            self.proj_str, 'data', self.model_str,
                            self.run_str, ens_label)

    def _file_name(self, dtype_out_time, extension='nc'):
        """Create the name of the aospy file."""
        out_lbl = _data_out_label(self.intvl_out, dtype_out_time,
                                  dtype_vert=self.dtype_out_vert)
        in_lbl = _data_in_label(self.intvl_in, self.dtype_in_time,
                                self.dtype_in_vert)
        ens_lbl = _ens_label(self.ens_mem)
        yr_lbl = _yr_label((self.start_date.year,
                            self.end_date.year))
        return '.'.join(
            [self.name, out_lbl, in_lbl, self.model_str, self.run_str_full,
             ens_lbl, yr_lbl, extension]
        ).replace('..', '.')

    def _path_scratch(self, dtype_out_time):
        return os.path.join(self.dir_scratch, self.file_name[dtype_out_time])

    def _path_archive(self):
        return os.path.join(self.dir_archive, 'data.tar')

    def _print_verbose(self, *args):
        """Print diagnostic message."""
        if not self.verbose:
            pass
        else:
            try:
                print('{} {}'.format(args[0], args[1]),
                      '({})'.format(time.ctime()))
            except IndexError:
                print('{}'.format(args[0]), '({})'.format(time.ctime()))

    def __init__(self, calc_interface):
        self.__dict__ = vars(calc_interface)
        self._print_verbose('Initializing Calc instance:', self.__str__())

        #[mod.set_grid_data() for mod in self.model]

        if isinstance(calc_interface.ens_mem, int):
            self.data_in_direc = self.data_in_direc[calc_interface.ens_mem]

        self.dt_set = False

        self.dir_scratch = self._dir_scratch()
        self.dir_archive = self._dir_archive()
        self.file_name = {d: self._file_name(d) for d in self.dtype_out_time}
        self.path_scratch = {d: self._path_scratch(d)
                             for d in self.dtype_out_time}
        self.path_archive = self._path_archive()

        self.data_out = {}

    def compute(self):
        """Perform all desired calculations on the data and save externally."""
        # Load the input data from disk.
        data_in = None
        # Compute only the needed timeseries.
        self._print_verbose('\n', 'Computing desired timeseries for '
                            '{} -- {}.'.format(self.start_date, self.end_date))
        bool_monthly = (['monthly_from' in self.dtype_in_time] +
                        ['time-mean' in dout for dout in self.dtype_out_time])
        bool_eddy = ['eddy' in dout for dout in self.dtype_out_time]
        if not all(bool_monthly):
            full_ts, full_dt = (1, 1)
        else:
            full_ts = False
        if any(bool_eddy) or any(bool_monthly):
            monthly_ts, monthly_dt = (1, 1)
        else:
            monthly_ts = False
        if any(bool_eddy):
            eddy_ts = 1
        else:
            eddy_ts = False

        # Average within each year.
        if not all(bool_monthly):
            full_ts = 1
        if any(bool_monthly):
            monthly_ts = 1
        if any(bool_eddy):
            eddy_ts = 1
        # Apply time reduction methods.
        if self.def_time:
            self._print_verbose("Applying desired time-reduction methods.")
            # Determine which are regional, eddy, time-mean.
            reduc_specs = [r.split('.') for r in self.dtype_out_time]
            reduced = {}
            for reduc, specs in zip(self.dtype_out_time, reduc_specs):
                if 'eddy' in specs:
                    data = eddy_ts
                elif 'time-mean' in specs:
                    data = monthly_ts
                else:
                    data = full_ts
                if 'reg' in specs:
                    reduced.update({reduc: 1})
                else:
                    reduced.update({reduc: 1})
        else:
            reduced = {'': full_ts}

        # Save to disk.
        self._print_verbose("Writing desired gridded outputs to disk.")
        for dtype_time, data in reduced.items():
            self.save(data, dtype_time, dtype_out_vert=self.dtype_out_vert)

    def _save_to_scratch(self, data, dtype_out_time):
        """Save the data to the scratch filesystem."""
        path = self.path_scratch[dtype_out_time]
        ##### SKC ADD TO DATABASE HERE #####

    def _update_data_out(self, data, dtype):
        """Append the data of the given dtype_out to the data_out attr."""
        try:
            self.data_out.update({dtype: data})
        except AttributeError:
            self.data_out = {dtype: data}

    def save(self, data, dtype_out_time, dtype_out_vert=False,
             scratch=True, archive=False):
        """Save aospy data to data_out attr and to an external file."""
        self._update_data_out(data, dtype_out_time)
        if scratch:
            self._save_to_scratch(data, dtype_out_time)
        print('\t', '{}'.format(self.path_scratch[dtype_out_time]))
