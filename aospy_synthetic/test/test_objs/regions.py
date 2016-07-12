from aospy_synthetic.region import Region

nh = Region(
    name='nh',
    description='Northern Hemisphere',
    lat_bounds=(0, 90),
    lon_bounds=(0, 360),
    do_land_mask=False
)

np = Region(
    name='np',
    description='North Pole',
    lat_bounds=(60, 90),
    lon_bounds=(0, 360),
    do_land_mask=False
)
