"""`Run` class; for storing attributes of a model run or obs product."""

from .timedate import TimeManager
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
                 idealized=False, backend=None, db_on=True):
        """Instantiate a `Run` object."""
        self.backend = backend
        self.db_on = db_on
        self.name = name
        self.description = description
        self.proj = proj

        self.model = None
        self._parent = None

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

    def __hash__(self):
        return hash((str(type(self)), self.name, self._parent))

    def __str__(self):
        return 'Run instance "%s"' % self.name

    __repr__ = __str__

#    def get_db_entry(self, session):
#        db_entry, isin = get_or_create(session, dbRun, defaults=None,
#                                       name=self.name)
#        return db_entry

#    def get_calcs(self, **kwargs):
#        """Returns all Calc rows that match all the keyword
#        arguments provided for this particular Run.

    #     Example:
    #     >>> rn.get_calcs(intvl_in='monthly', intvl_out='djf')

    #     Parameters
    #     ----------
    #     **kwargs : dict
    #         Conditions to be met by the returned Calcs

    #     Returns
    #     -------
    #     cs : list
    #         List of Calc rows that meet the keyword argument conditions
    #     """
    #     session = create_session()
    #     rn = self.get_db_entry(session)
    #     params = dict((k, v) for k, v in kwargs.iteritems()
    #                   if not isinstance(v, ClauseElement))
    #     cs = session.query(dbCalc).filter_by(run=rn, **params).all()
    #     session.close()
    #     return cs

    # def get_vars(self, **kwargs):
    #     """Returns all Var rows from this run for which Calcs that
    #     meet the provided conditions exist.

    #     Parameters
    #     ----------
    #     **kwargs : dict
    #         Conditions that Calcs must meet

    #     Returns
    #     -------
    #     cs : list
    #         List of Var rows for which Calcs with the given properties
    #         exist
    #     """
    #     session = create_session()
    #     rn = self.get_db_entry(session)
    #     params = dict((k, v) for k, v in kwargs.iteritems()
    #                   if not isinstance(v, ClauseElement))
    #     sub = session.query(dbCalc).filter_by(run=rn,
    #                                           **params).subquery('sub')
    #     cs = session.query(dbVar).filter(sub.c.var_id == dbVar.id).all()
    #     session.close()
    #     return cs
