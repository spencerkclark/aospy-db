from aospy_synthetic.units import Units

specific_mass = Units(
    units='',
    plot_units=r'g kg$^{-1}$',
    plot_units_conv=1e3,
    vert_int_plot_units='kg m$^{-2}$',
    vert_int_plot_units_conv=1.
)
K = Units(units='K')
W_m2 = Units(
    units=r'W m$^{-2}$',
    vert_int_units=r''
)
J_kg1 = Units(
    units=r'J kg$^{-1}$',
    plot_units='K',
    vert_int_units='J m$^{-2}$',
    vert_int_plot_units='10$^6$ J m$^{-2}$',
    vert_int_plot_units_conv=1e-6
)
Pa = Units(
    units=r'Pa',
    plot_units=r'hPa',
    plot_units_conv=1e-2
)
hPa = Units(
    units=r'hPa',
)
