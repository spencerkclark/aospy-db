"""region.py: Region class and region_inst()."""


class Region(object):
    """Geographical region."""
    def __init__(self, name='', description='', lon_bounds=[], lat_bounds=[],
                 mask_bounds=[], do_land_mask=False, db_tracking=True):
        """Instantiate a Region object."""
        self.name = name
        self.description = description
        if lon_bounds and lat_bounds and not mask_bounds:
            self.mask_bounds = [(lat_bounds, lon_bounds)]
        else:
            self.mask_bounds = mask_bounds
        self.do_land_mask = do_land_mask
        self.db_tracking = db_tracking

    def track(self):
        return self.db_tracking

    def __str__(self):
        return 'Geographical region "' + self.name + '"'

    __repr__ = __str__
