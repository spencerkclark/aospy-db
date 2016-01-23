"""proj.py: aospy.Proj class for organizing work in single project."""
import time

from aospy_db import create_session, get_or_create
from aospy_db import Proj as dbProj
from .utils import dict_name_keys


class Proj(object):
    """Project parameters: models, regions, directories, etc."""
    def __init__(self, name, vars={}, models={}, default_models={}, regions={},
                 direc_out='', nc_dir_struc=False, verbose=True):
        self.verbose = verbose
        if self.verbose:
            print ("Initializing Project instance: %s (%s)"
                   % (name, time.ctime()))
        self.name = name
        self.direc_out = direc_out
        self.nc_dir_struc = nc_dir_struc

        if models:
            self.models = dict_name_keys(models)
        else:
            self.models = {}
        if default_models == 'all':
            self.default_models = self.models
        elif default_models:
            self.default_models = dict_name_keys(default_models)
        else:
            self.default_models = {}
        if regions:
            self.regions = dict_name_keys(regions)
        else:
            self.regions = {}

        for obj_dict in (self.models, self.regions):
            for obj in obj_dict.values():
                setattr(obj, 'proj', self)

        db_models = [m.db_entry for m in models]
        # Add row to database.
        session = create_session()
        self.db_entry, isin = get_or_create(session, dbProj, defaults=None,
                                            name=self.name,
                                            direc_out=self.direc_out)
        if not self.db_entry.models:
            self.db_entry.models = db_models
        session.commit()
        session.close()

    def __str__(self):
        return 'Project instance "' + self.name + '"'

    __repr__ = __str__
