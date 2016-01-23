"""`Run` class; for storing attributes of a model run or obs product."""

from .timedate import TimeManager
from aospy_db import create_session, get_or_create
from aospy_db import Run as dbRun
from aospy_db import Calc as dbCalc
from sqlalchemy.sql import ClauseElement


class Run(object):
    """Model run parameters."""
    def _set_direc(self, data_in_direc, ens_mem_prefix, ens_mem_ext,
                   ens_mem_suffix):
        """Set the list of paths containing the Run's netCDF data."""
        if all((ens_mem_prefix, ens_mem_ext, ens_mem_suffix)):
            return [ens_mem_prefix + ext + ens_mem_suffix
                    for ext in ens_mem_ext]
        return data_in_direc

    def __init__(self, name='', description='', proj=False,
                 data_in_direc=False,
                 data_in_dur=False, data_in_start_date=False,
                 data_in_end_date=False, data_in_dir_struc='gfdl',
                 data_in_suffix=False, data_in_files={},
                 default_date_range=False, ens_mem_prefix=False,
                 ens_mem_ext=False, ens_mem_suffix=False, tags=(),
                 idealized=False):
        """Instantiate a `Run` object."""
        self.name = name
        self.description = description
        self.proj = proj

        self.data_in_dur = data_in_dur
        self.data_in_dir_struc = data_in_dir_struc
        self.data_in_suffix = data_in_suffix
        self.data_in_files = data_in_files
        self.data_in_start_date = TimeManager.to_datetime(data_in_start_date)
        self.data_in_end_date = TimeManager.to_datetime(data_in_end_date)
        try:
            self.default_date_range = tuple([TimeManager.to_datetime(d)
                                             for d in default_date_range])
        except:
            self.default_date_range = (self.data_in_start_date,
                                       self.data_in_end_date)

        self.tags = tags
        self.idealized = idealized
        self.ens_mem_prefix = ens_mem_prefix
        self.ens_mem_ext = ens_mem_ext
        self.ens_mem_suffix = ens_mem_suffix
        self.data_in_direc = self._set_direc(data_in_direc, ens_mem_prefix,
                                             ens_mem_ext, ens_mem_suffix)

        # Add row to database.
        session = create_session()
        self.db_entry, isin = get_or_create(session, dbRun, defaults=None,
                                            name=self.name,
                                            description=self.description)
        session.commit()
        session.close()

    def __str__(self):
        return 'Run instance "%s"' % self.name

    __repr__ = __str__

    def get_db_entry(self, session):
        db_entry, isin = get_or_create(session, dbRun, defaults=None,
                                       name=self.name)
        return db_entry

    def get_calcs(self, **kwargs):
        session = create_session()
        rn = self.get_db_entry(session)
        params = dict((k, v) for k, v in kwargs.iteritems()
                      if not isinstance(v, ClauseElement))
        cs = session.query(dbCalc).filter_by(run=rn, **params).all()
        session.close()
        return cs

    def get_vars(self, **kwargs):
        session = create_session()
        rn = self.get_db_entry(session)
        params = dict((k, v) for k, v in kwargs.iteritems()
                      if not isinstance(v, ClauseElement))
        cs = session.query(dbCalc.var).filter_by(run=rn, **params).all()
        session.close()
        return cs
