from aospy_synthetic.proj import Proj
from . import models

p = Proj(
    name='a',
    direc_out='b',
    models=(
        models.m,
    )
)
