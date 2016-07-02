from aospy_synthetic.proj import Proj
import variables
import models
from aospy_synthetic.db.sqlalchemy.sqlalchemy_db import SQLAlchemyDB

example = Proj(
    'example',
    vars=variables.master_vars_list,
    direc_out='/archive/skc/example/',
    models=(
        models.am2,
    ),
    backend=SQLAlchemyDB('path')
)
