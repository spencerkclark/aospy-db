from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import ClauseElement

engine = create_engine('sqlite:///test.db')
Base = declarative_base()


def create_session(path='sqlite:///test.db'):
    """Generates a session to interface with the database

    Parameters
    ----------
    path : str
        path to database

    Returns
    -------
    session : sqlalchemy session
        current session
    """
    engine = create_engine(path)
    Session = sessionmaker(bind=engine)
    return Session()


def get_or_create(session, obj, defaults=None, **kwargs):
    """Either creates a new row in the database within the current session
    or returns an existing one.  Adapted from SO question: 2546207, accepted
    answer.

    Parameters
    ----------
    session : Session
        current sqlalchemy session
    obj : sqlalchemy object
        row object being added
    defaults : dict
        default parameters in constructor for obj
    **kwargs : dict
        parameters used to construct obj

    Returns
    -------
    instance : sqlalchemy obj
        instance of created or retrieved row object
    """
    instance = session.query(obj).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems()
                      if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = obj(**params)
        session.add(instance)
        return instance, True


class AospyDBEntry(Base):
    """A generic aospy object that enters the database."""

    def __init__(self, AospyObj):
        """Instantiates a database object from an aospy object based on the
        object's overlapping attributes with the database columns.

        Essentially, if we track the attributes in the database, they will
        enter the database automatically.
        """
        for attr in AospyObj.attrs:
            if hasattr(type(self), attr):
                setattr(self, attr, getattr(AospyObj, attr))


class Proj(AospyDBEntry):
    """A table containing pointers to aospy Proj objects."""
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    direc_out = Column(String)

    def __repr__(self):
        return "<Proj(name='%s')>" % self.name


class Model(AospyDBEntry):
    """A table containing pointers to Model objects."""
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    proj_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Proj", back_populates="models")

    def __repr__(self):
        return "<Model(name='%s')>" % self.name


class Run(AospyDBEntry):
    """A table containing pointers to Run objects."""
    __tablename__ = 'runs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    model_id = Column(Integer, ForeignKey('models.id'))
    model = relationship("Model", back_populates="runs")
    data_in_start_date = Column(String)
    data_in_end_date = Column(String)
    data_in_dur = Column(Integer)
    data_in_direc = Column(String)

    def __repr__(self):
        return "<Run(name='%s', description='%s', model=%d)>" % (self.name,
                                                                 self.description,
                                                                 self.model_id)


class Var(AospyDBEntry):
    """A table containing pointers to Var objects."""
    __tablename__ = 'variables'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return "<Var(name='%s', description='%s')>" % (self.name,
                                                       self.description)


class Calc(AospyDBEntry):
    """A table containing pointers to Var objects."""
    __tablename__ = 'calculations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    filepath = Column(String)
    var_id = Column(Integer, ForeignKey('variables.id'))
    var = relationship("Var", back_populates="calculations")
    run_id = Column(Integer, ForeignKey('runs.id'))
    run = relationship("Run", back_populates="calculations")
    intvl_in = Column(String)
    intvl_out = Column(String)
    dtype_out_time = Column(String)
    units = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    pressure_type = Column(String)

    def __repr__(self):
        r = ('<aospy.Calc(var: %s)>\n'
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
Proj.models = relationship("Model",
                           order_by=Model.id,
                           back_populates="project")
Model.runs = relationship("Run",
                          order_by=Run.id,
                          back_populates="model")
Run.calculations = relationship("Calc",
                                order_by=Calc.id,
                                back_populates="run")
Var.calculations = relationship("Calc",
                                order_by=Calc.id,
                                back_populates="var")


Base.metadata.create_all(engine)

if __name__ == '__main__':
    pass
