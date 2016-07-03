"""SQLAlchemy DB Setup: UniqueMixin design pattern adapted from:
https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/UniqueObject"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


def initialize_db(DB_PATH):
    engine = create_engine(DB_PATH)
    Base.metadata.create_all(engine)


def _set_metadata_attrs(db_obj, AospyObj):
    for key in db_obj._metadata_attrs:
        if hasattr(AospyObj, db_obj._metadata_attrs[key]):
            setattr(
                db_obj, key, getattr(
                    AospyObj,
                    db_obj._metadata_attrs[key]
                )
            )


def _unique(session, cls, hashfunc, queryfunc, constructor, args, kwargs):
    cache = getattr(session, '_unique_cache', None)
    if cache is None:
        session._unique_cache = cache = {}

    key = (cls, hashfunc(*args, **kwargs))

    # First check to see if the row was added to the session
    if key in cache:
        _set_metadata_attrs(cache[key], *args)
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
            else:
                _set_metadata_attrs(obj, *args)
        cache[key] = obj
    return obj


class UniqueMixin(object):

    _metadata_attrs = {}
    _db_attrs = {}
    hash = Column(String)

    @staticmethod
    def unique_hash(AospyObj):
        return hash(AospyObj)

    @staticmethod
    def unique_filter(query, AospyObj):
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

    @staticmethod
    def _get_db_obj(db_cls, session, AospyObj):
        return db_cls.as_unique(session, AospyObj)

    def __init__(self, session, AospyObj):
        self.hash = hash(AospyObj)

        _set_metadata_attrs(self, AospyObj)

        for key in self._db_attrs:
            if hasattr(AospyObj, self._db_attrs[key]['aospy_obj_attr']):
                sub_obj = getattr(
                    AospyObj,
                    self._db_attrs[key]['aospy_obj_attr']
                )
                if sub_obj:
                    setattr(
                        self, key,
                        self._get_db_obj(
                            self._db_attrs[key]['db_cls'],
                            session,
                            sub_obj
                        )
                    )

    def __repr__(self):
        repr = ''
        for attr in self.__class__._metadata_attrs:
            repr += '{}: {}\n'.format(attr, getattr(self, attr))
        return repr

    def __str__(self):
        return self.__repr__()


class ProjDB(UniqueMixin, Base):
    __tablename__ = 'projects'
    _metadata_attrs = {
        'name': 'name',
        'direc_out': 'direc_out'
    }
    id = Column(Integer, primary_key=True)
    models = relationship('ModelDB', back_populates='project')

    # _metadata_attrs
    name = Column(String)
    direc_out = Column(String)


class ModelDB(UniqueMixin, Base):
    __tablename__ = 'models'
    _metadata_attrs = {
        'name': 'name',
        'description': 'description'
    }
    _db_attrs = {
        'project': {
            'db_cls': ProjDB,
            'aospy_obj_attr': 'project'
        }
    }

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('ProjDB', back_populates='models')

    runs = relationship('RunDB', back_populates='model')

    # _metadata_attrs
    name = Column(String)
    description = Column(String)


class RunDB(UniqueMixin, Base):
    __tablename__ = 'runs'
    _metadata_attrs = {
        'name': 'name',
        'description': 'description',
        'data_in_start_date': 'data_in_start_date',
        'data_in_end_date': 'data_in_end_date',
        'data_in_dur': 'data_in_dur',
        'data_in_direc': 'data_in_direc'
    }
    _db_attrs = {
        'model': {
            'db_cls': ModelDB,
            'aospy_obj_attr': 'model'
        }
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


class RegionDB(UniqueMixin, Base):
    __tablename__ = 'regions'
    _metadata_attrs = {
        'name': 'name',
        'description': 'description'
    }
    id = Column(Integer, primary_key=True)
    calcs = relationship('CalcDB', back_populates='region')

    # _metadata_attrs
    name = Column(String)
    description = Column(String)


class CalcDB(UniqueMixin, Base):
    __tablename__ = 'calcs'
    _metadata_attrs = {
        'intvl_in': 'intvl_in',
        'intvl_out': 'intvl_out',
        'dtype_out_time': 'dtype_out_time',
        'start_date': 'start_date',
        'end_date': 'end_date',
        'dtype_in_vert': 'dtype_in_vert'
    }
    _db_attrs = {
        'run': {
            'db_cls': RunDB,
            'aospy_obj_attr': 'run'
        },
        'var': {
            'db_cls': VarDB,
            'aospy_obj_attr': 'var'
        },
        'region': {
            'db_cls': RegionDB,
            'aospy_obj_attr': 'region'
        }
    }

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('runs.id'))
    run = relationship('RunDB', back_populates='calcs')

    var_id = Column(Integer, ForeignKey('vars.id'))
    var = relationship('VarDB', back_populates='calcs')

    region_id = Column(Integer, ForeignKey('regions.id'))
    region = relationship('RegionDB', back_populates='calcs')

    # _metadata_attrs
    intvl_in = Column(String)
    intvl_out = Column(String)
    dtype_out_time = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    dtype_in_vert = Column(String)
