from aospy_synthetic.proj import Proj
import variables
import models

example = Proj(
    'example',
    vars=variables.master_vars_list,
    direc_out='/archive/skc/example/',
    models=(
        models.am2,
        models.am2_reyoi,
        models.dargan_T42,
        models.dargan
    )
)
