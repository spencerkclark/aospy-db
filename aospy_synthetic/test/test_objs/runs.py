from aospy_synthetic.run import Run

r = Run(
    name='a',
    description='b',
    data_in_direc='c',
    data_in_dur=1,
    data_in_start_date='0001-01-01',
    data_in_end_date='0080-12-31',
    default_date_range=('0021-01-01', '0080-12-31'),
)
