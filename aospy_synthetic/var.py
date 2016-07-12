"""var.py: Var class for representing a physical variable in aospy."""

from .units import Units


class Var(object):
    """Physical variables."""
    def __init__(self, name, alt_names=False, func=False, variables=False,
                 units=False, plot_units='', plot_units_conv=1, domain='atmos',
                 description='', def_time=False, def_vert=False, def_lat=False,
                 def_lon=False, in_nc_grid=False, math_str=False,
                 colormap='RdBu_r', valid_range=False,
                 func_input_dtype='DataArray', db_tracking=True):
        """Create Var object."""
        self.name = name
        if alt_names:
            self.alt_names = alt_names
            self.names = tuple([name] + list(alt_names))
        else:
            self.names = tuple([name])

        if not func:
            self.func = lambda x: x
            self.variables = False
            self.func_input_dtype = None
        else:
            self.func = func
            self.variables = variables
        self.func_input_dtype = func_input_dtype

        if not isinstance(units, Units):
            self.units = Units(units=units)
        else:
            self.units = units

        if not description:
            try:
                self.description = self.func.func_doc
            except AttributeError:
                self.description = description
        else:
            self.description = description
        self.__doc__ = self.description

        self.domain = domain
        self.def_time = def_time
        self.def_vert = def_vert
        self.def_lat = def_lat
        self.def_lon = def_lon
        self.in_nc_grid = in_nc_grid
        self.math_str = math_str
        self.colormap = colormap
        self.valid_range = valid_range
        self.db_tracking = db_tracking

    def __hash__(self):
        return hash((str(type(self)), self.name, self.units))

    def __str__(self):
        return 'Var instance "' + self.name + '"'

    def track(self):
        """Returns True if this object and all of its parent objects
        have db_tracking set to True.
        """
        return all([self.db_tracking, self.units.track()])

    __repr__ = __str__
