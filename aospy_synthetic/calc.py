"""calc.py: classes for performing specified calculations on aospy data"""
from __future__ import print_function
import os
import time

from .io import _data_in_label, _data_out_label, _ens_label, _yr_label
from .timedate import TimeManager
from .utils import get_parent_attr


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
            attr_val = tuple([get_parent_attr(self.run, attr, strict=False)])
            setattr(self, attr, attr_val)

    def __init__(self, proj=None, model=None, run=None, ens_mem=None, var=None,
                 date_range=None, region=None, intvl_in=None, intvl_out=None,
                 dtype_in_time=None, dtype_in_vert=None, dtype_out_time=None,
                 dtype_out_vert=None, level=None, chunk_len=False,
                 verbose=True, backend=None, db_tracking=True):
        """Create the CalcInterface object with the given parameters."""
        if run not in model.runs.values():
            raise AttributeError("Model '{}' has no run '{}'.  Calc object "
                                 "will not be generated.".format(model, run))

        self.proj = proj
        self.model = model
        self.run = run

        self._set_data_in_attrs()

        self.proj_str = str(proj)
        self.model_str = str(model)

        self.run_str = run.name
        self.run_str_full = run.name

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

        # For now we'll change to make Calc one to one -- testing already works
        # this way.  (It doesn't use the CalcInterface -- CalcInterface may be
        # all we need to change to change Calc to one to one in reality).
        self.dtype_out_time = dtype_out_time
        self.dtype_out_vert = dtype_out_vert
        self.region = region

        self.months = TimeManager.month_indices(intvl_out)
        self.start_date = TimeManager.str_to_datetime(date_range[0])
        self.end_date = TimeManager.str_to_datetime(date_range[-1])
        tm = TimeManager(self.start_date, self.end_date, intvl_out)
        self.date_range = tm.create_time_array()

        self.start_date_xray = tm.apply_year_offset(self.start_date)
        self.end_date_xray = tm.apply_year_offset(self.end_date)

        self.backend = backend
        self.db_tracking = db_tracking


class Calc(object):
    """Class for executing, saving, and loading a single computation."""

    def __hash__(self):
        self.file_name = self._file_name(self.dtype_out_time)
        if self.region:
            return hash((str(type(self)), self.file_name,
                         self.region.name, self.run, self.var))
        else:
            return hash((str(type(self)), self.file_name, self.run, self.var))

    def track(self):
        """Returns True if this object and all of its parent objects
        have db_tracking set to True.
        """
        if self.region:
            return all(
                [
                    self.run.track(),
                    self.var.track(),
                    self.region.track(),
                    self.db_tracking
                ]
            )
        else:
            return all([self.run.track(), self.var.track(), self.db_tracking])

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
        return os.path.join(self.dir_scratch, self.file_name)

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

        if isinstance(calc_interface.ens_mem, int):
            self.data_in_direc = self.data_in_direc[calc_interface.ens_mem]

        self.dt_set = False

        self.dir_scratch = self._dir_scratch()
        self.dir_archive = self._dir_archive()
        self.file_name = self._file_name(self.dtype_out_time)
        self.path_scratch = self._path_scratch(self.dtype_out_time)
        self.path_archive = self._path_archive()

        self.data_out = {}
