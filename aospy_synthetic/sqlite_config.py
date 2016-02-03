from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import relationship

from aospy.proj import Proj
from aospy.model import Model
from aospy.run import Run
from aospy.var import Var
from aospy.calc import Calc

DB_PATH = 'sqlite:///test.db'
engine = create_engine(DB_PATH)
Base = declarative_base()


class AospyDBEntry(object):
    """A generic aospy object that enters the database."""

    def __init__(self, AospyObj, **kwargs):
        """Instantiates a database object from an aospy object based on the
        object's overlapping attributes with the database columns.

        Essentially, if we track the attributes in the database, they will
        enter the database automatically.
        """
        print AospyObj
        for attr, value in AospyObj.__dict__.iteritems():
            if hasattr(type(self), attr) and (attr not in ['runs',
                                                           'models',
                                                           'projects',
                                                           'calcs']):
                setattr(self, attr, getattr(AospyObj, attr))
        for attr in kwargs:
            if hasattr(type(self), attr):
                setattr(self, attr, kwargs[attr])


class ProjDB(AospyDBEntry, Base):
    """A table containing pointers to aospy Proj objects."""
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    direc_out = Column(String)

    def __repr__(self):
        return "<ProjDB(name='%s')>" % self.name


class ModelDB(AospyDBEntry, Base):
    """A table containing pointers to Model objects."""
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    proj_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("ProjDB", back_populates="models")

    def __repr__(self):
        return "<ModelDB(name='%s')>" % self.name


class RunDB(AospyDBEntry, Base):
    """A table containing pointers to Run objects."""
    __tablename__ = 'runs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    model_id = Column(Integer, ForeignKey('models.id'))
    model = relationship("ModelDB", back_populates="runs")
    data_in_start_date = Column(DateTime)
    data_in_end_date = Column(DateTime)
    data_in_dur = Column(Integer)
    data_in_direc = Column(String)

    def __repr__(self):
        return "<RunDB(name='%s', description='%s', model=%d)>" % (self.name,
                                                                   self.description,
                                                                   self.model_id)


class VarDB(AospyDBEntry, Base):
    """A table containing pointers to Var objects."""
    __tablename__ = 'variables'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return "<VarDB(name='%s', description='%s')>" % (self.name,
                                                         self.description)


class CalcDB(AospyDBEntry, Base):
    """A table containing pointers to Var objects."""
    __tablename__ = 'calculations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    filepath = Column(String)
    var_id = Column(Integer, ForeignKey('variables.id'))
    var = relationship("VarDB", back_populates="calculations")
    run_id = Column(Integer, ForeignKey('runs.id'))
    run = relationship("RunDB", back_populates="calculations")
    intvl_in = Column(String)
    intvl_out = Column(String)
    dtype_out_time = Column(String)
    units = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    pressure_type = Column(String)

    def __repr__(self):
        r = ('<aospy.CalcDB(var: %s)>\n'
             'Attributes:\n'
             '  * filepath:\t\t%s\n'
             '  * description:\t%s\n'
             '  * intvl_in:\t\t%s\n'
             '  * intvl_out:\t\t%s\n'
             '  * dtype_out_time:\t\t%s\n'
             % (self.name, self.filepath, self.description,
                self.intvl_in, self.intvl_out, self.dtype_out_time))
        return r

# Set up the relationships.
ProjDB.models = relationship("ModelDB",
                             order_by=ModelDB.id,
                             back_populates="project")
ModelDB.runs = relationship("RunDB",
                            order_by=RunDB.id,
                            back_populates="model")
RunDB.calculations = relationship("CalcDB",
                                  order_by=CalcDB.id,
                                  back_populates="run")
VarDB.calculations = relationship("CalcDB",
                                  order_by=CalcDB.id,
                                  back_populates="var")


Base.metadata.create_all(engine)
