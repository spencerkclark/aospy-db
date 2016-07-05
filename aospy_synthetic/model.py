"""model.py: Model class of aospy for storing attributes of a GCM."""
from .utils import dict_name_keys


class Model(object):
    """Parameters of local data associated with a single climate model."""
    def __init__(self, name='', description='', proj=False, grid_file_paths=(),
                 data_in_direc=False, data_in_dir_struc=False,
                 data_in_dur=False, data_in_start_date=False,
                 data_in_end_date=False, default_date_range=False, runs={},
                 default_runs={}, load_grid_data=False, repo_version=False,
                 backend=None, db_tracking=True):
        self.backend = backend
        self.name = name
        self.db_tracking = db_tracking
        self.description = description
        self.proj = proj

        self.grid_file_paths = grid_file_paths
        self.repo_version = repo_version

        self.data_in_direc = data_in_direc
        self.data_in_dir_struc = data_in_dir_struc
        self.data_in_dur = data_in_dur
        self.data_in_start_date = data_in_start_date
        self.data_in_end_date = data_in_end_date
        self.default_date_range = default_date_range

        self.runs = dict_name_keys(runs)

        if runs:
            for run in runs:
                run.model = self

        if default_runs:
            self.default_runs = dict_name_keys(default_runs)
        else:
            self.default_runs = {}

        self.grid_data_is_set = False

    def __str__(self):
        return 'Model instance "' + self.name + '"'

    def __hash__(self):
        return hash((str(type(self)), self.name, self.proj))

    def track(self):
        return all([self.proj.track(), self.db_tracking])

    __repr__ = __str__
