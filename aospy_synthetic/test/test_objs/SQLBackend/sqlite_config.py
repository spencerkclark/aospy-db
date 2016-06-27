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
    _metadata_attrs = {}
    _db_attrs = {}
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
        return cls._parent_cls.as_unique(session, AospyObj._parent)

    @staticmethod
    def _get_db_obj(cls, session, AospyObj):
        return cls.as_unique(session, AospyObj)

    def __init__(self, session, AospyObj):
        self.hash = hash(AospyObj)
        if self._parent_cls:
            setattr(self, self._parent_attr, self._get_parent(session,
                                                              AospyObj))
        for key in self._metadata_attrs:
            if hasattr(AospyObj, self._metadata_attrs[key]):
                setattr(self, key, getattr(AospyObj,
                                           self._metadata_attrs[key]))

        for key in self._db_attrs:
            if hasattr(AospyObj, self._db_attrs[key]['obj']):
                sub_obj = getattr(AospyObj, self._db_attrs[key]['obj'])
                if sub_obj:
                    setattr(self, key,
                            self._get_db_obj(self._db_attrs[key]['db_cls'],
                                             session,
                                             getattr(AospyObj,
                                                     self._db_attrs[key]['obj'])))


class ProjDB(UniqueMixin, Base):
    __tablename__ = 'projects'
    _metadata_attrs = {
        'name': 'name',
        'description': 'description',
        'direc_out': 'direc_out'
    }
    id = Column(Integer, primary_key=True)
    models = relationship('ModelDB', back_populates='project')

    # _metadata_attrs
    name = Column(String)
    description = Column(String)
    direc_out = Column(String)


class ModelDB(UniqueMixin, Base):
    __tablename__ = 'models'
    _parent_cls = ProjDB
    _parent_attr = 'project'
    _metadata_attrs = {
        'name': 'name'
    }

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('ProjDB', back_populates='models')

    runs = relationship('RunDB', back_populates='model')

    # _metadata_attrs
    name = Column(String)


class RunDB(UniqueMixin, Base):
    __tablename__ = 'runs'
    _parent_cls = ModelDB
    _parent_attr = 'model'
    _metadata_attrs = {
        'name': 'name',
        'description': 'description',
        'data_in_start_date': 'data_in_start_date',
        'data_in_end_date': 'data_in_end_date',
        'data_in_dur': 'data_in_dur',
        'data_in_direc': 'data_in_direc'
    }

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    model = relationship('ModelDB', back_populates='runs')

    calcs = relationship('CalcDB', back_populates='run')

    # _metadata_attrs
    name = Column(String)
    description = Column(String)
    data_in_start_date = Column(DateTime)
    data_in_end_date = Column(DateTime)
    data_in_dur = Column(Integer)
    data_in_direc = Column(String)


class VarDB(UniqueMixin, Base):
    __tablename__ = 'vars'
    _metadata_attrs = {
        'name': 'name',
        'description': 'description',
    }
    id = Column(Integer, primary_key=True)
    calcs = relationship('CalcDB', back_populates='var')

    # _metadata_attrs
    name = Column(String)
    description = Column(String)

    # TODO properly handle aospy Units objects (they should probably be another
    # table)


class RegDB(UniqueMixin, Base):
    __tablename__ = 'regs'
    _metadata_attrs = {
        'name': 'name',
        'description': 'description'
    }
    id = Column(Integer, primary_key=True)
    calcs = relationship('CalcDB', back_populates='reg')

    # _metadata_attrs
    name = Column(String)
    description = Column(String)


class CalcDB(UniqueMixin, Base):
    __tablename__ = 'calcs'
    _parent_cls = RunDB
    _parent_attr = 'run'
    _metadata_attrs = {
        'intvl_in': 'intvl_in',
        'intvl_out': 'intvl_out',
        'dtype_out_time': 'dtype_out_time',
        'start_date': 'start_date',
        'end_date': 'end_date',
        'pressure_type': 'pressure_type'
    }
    _db_attrs = {
        'var': {
            'db_cls': VarDB,
            'obj': 'var'
        },
        'reg': {
            'db_cls': RegDB,
            'obj': 'region'
        }
    }

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('runs.id'))
    run = relationship('RunDB', back_populates='calcs')

    var_id = Column(Integer, ForeignKey('vars.id'))
    var = relationship('VarDB', back_populates='calcs')

    reg_id = Column(Integer, ForeignKey('regs.id'))
    reg = relationship('RegDB', back_populates='calcs')

    # _metadata_attrs
    intvl_in = Column(String)
    intvl_out = Column(String)
    dtype_out_time = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    pressure_type = Column(String)


Base.metadata.create_all(engine)
