from aospy_synthetic.proj import Proj
import variables
import models
from aospy_synthetic.db.sql.sql_backend import SQLBackend

example = Proj(
    'example',
    vars=variables.master_vars_list,
    direc_out='/archive/skc/example/',
    models=(
        models.am2,
    ),
    backend=SQLBackend('path')
)
