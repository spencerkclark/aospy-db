"""SQLAlchemy DB Setup: UniqueMixin design pattern adapted from:
https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/UniqueObject"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import relationship

DB_PATH = 'sqlite:///test.db'
engine = create_engine(DB_PATH)
Base = declarative_base()


def _unique(session, cls, hashfunc, queryfunc, constructor, args, kwargs):
    cache = getattr(session, '_unique_cache', None)
    if cache is None:
        session._unique_cache = cache = {}

    key = (cls, hashfunc(*args, **kwargs))

    # First check to see if the row was added to the session
    if key in cache:
        return cache[key]

    # Then check if row is already in the DB
    else:
        with session.no_autoflush:
            q = session.query(cls)
            q = queryfunc(q, *args, **kwargs)
            obj = q.first()

            # If it is not in the DB or session cache, create a new row
            if not obj:
                obj = constructor(session, *args, **kwargs)
                session.add(obj)
        cache[key] = obj
    return obj


class UniqueMixin(object):

    _parent_cls = None
    _parent_attr = None
    hash = Column(String)

    @classmethod
    def unique_hash(cls, AospyObj):
        return hash(AospyObj)

    @classmethod
    def unique_filter(cls, query, AospyObj):
        return query.filter_by(hash=hash(AospyObj))

    @classmethod
    def as_unique(cls, session, *args, **kwargs):
        return _unique(
            session,
            cls,
            cls.unique_hash,
            cls.unique_filter,
            cls,
            args,
            kwargs
        )

    @classmethod
    def _get_parent(cls, session, AospyObj):
        cls._parent_cls.as_unique(session, AospyObj._parent)

    def __init__(self, session, AospyObj):
        self.hash = hash(AospyObj)
        if self._parent_cls:
            setattr(self, self._parent_attr, self._get_parent(session,
                                                              AospyObj))


class ProjDB(UniqueMixin, Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    models = relationship('ModelDB', back_populates='project')


class ModelDB(UniqueMixin, Base):
    __tablename__ = 'models'
    _parent_cls = ProjDB
    _parent_attr = 'project'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('ProjDB', back_populates='models')

    runs = relationship('RunDB', back_populates='model')


class RunDB(UniqueMixin, Base):
    __tablename__ = 'runs'
    _parent_cls = ModelDB
    _parent_attr = 'model'

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    model = relationship('ModelDB', back_populates='runs')

    calcs = relationship('CalcDB', back_populates='run')


class CalcDB(UniqueMixin, Base):
    __tablename__ = 'calcs'
    _parent_cls = RunDB
    _parent_attr = 'run'

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('runs.id'))
    run = relationship('RunDB', back_populates='calcs')

    var_id = Column(Integer, ForeignKey('vars.id'))
    var = relationship('VarDB', back_populates='calcs')

    reg_id = Column(Integer, ForeignKey('regs.id'))
    reg = relationship('RegDB', back_populates='calcs')


class VarDB(Base):
    __tablename__ = 'vars'
    id = Column(Integer, primary_key=True)
    calcs = relationship('CalcDB', back_populates='var')


class RegDB(Base):
    __tablename__ = 'regs'
    id = Column(Integer, primary_key=True)
    calcs = relationship('CalcDB', back_populates='reg')

Base.metadata.create_all(engine)
