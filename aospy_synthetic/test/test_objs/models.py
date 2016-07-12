from aospy_synthetic.model import Model
from . import runs

m = Model(
    name='a',
    runs=[runs.r],
    default_runs=[runs.r]
)
