"""Test suite for the aospy_synthetic db features."""

import unittest
from subprocess import call

from test_objs import (runs, models, projects, variables,
                       regions, calc_objs)
from aospy_synthetic.db.sqlalchemy.sqlalchemy_db import SQLAlchemyDB
from aospy_synthetic.db.sqlalchemy.sqlalchemy_config import (ProjDB, ModelDB,
                                                             RunDB, VarDB,
                                                             RegionDB, CalcDB)


class TestProjDB(unittest.TestCase):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = projects.p
        self.db_cls = ProjDB
        self.ex_str_attr = 'direc_out'

    def tearDown(self):
        call(['rm', 'test.db'])

    def test_add(self):
        self.db.add(self.AospyObj)
        with self.db.session_scope() as session:
            q = session.query(self.db_cls)
            db_obj = q.filter_by(hash=hash(self.AospyObj)).first()

            for attr in self.db_cls._metadata_attrs:
                actual = getattr(db_obj, attr)
                expected = getattr(self.AospyObj,
                                   self.db_cls._metadata_attrs[attr])
                self.assertEqual(actual, expected)

    def test_uniqueness_checking(self):
        self.db.add(self.AospyObj)
        self.db.add(self.AospyObj)  # Call add on a duplicate object
        with self.db.session_scope() as session:
            q = session.query(self.db_cls)
            db_objs = q.filter_by(hash=hash(self.AospyObj)).all()
            self.assertEqual(len(db_objs), 1)

    @unittest.expectedFailure
    def test_update_attr(self):
        self.db.add(self.AospyObj)
        setattr(self.AospyObj, self.ex_str_attr, 'updated')
        self.db.add(self.AospyObj)
        with self.db.session_scope() as session:
            q = session.query(self.db_cls)
            db_objs = q.filter_by(hash=hash(self.AospyObj)).all()
            self.assertEqual(len(db_objs), 1)  # No duplicates

            db_obj = db_objs[0]
            actual = getattr(db_obj, self.ex_str_attr)
            expected = 'updated'
            self.assertEqual(actual, expected)


class TestModelDB(TestProjDB):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = models.m
        self.db_cls = ModelDB
        self.ex_str_attr = 'description'


class TestRunDB(TestProjDB):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = runs.r
        self.db_cls = RunDB
        self.ex_str_attr = 'description'


class TestVarDB(TestProjDB):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = variables.mse
        self.db_cls = VarDB
        self.ex_str_attr = 'description'


class TestRegDB(TestProjDB):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = regions.nh
        self.db_cls = RegionDB
        self.ex_str_attr = 'description'


class TestCalcDB(TestProjDB):
    def setUp(self):
        self.db = SQLAlchemyDB()
        self.AospyObj = calc_objs.c
        self.db_cls = CalcDB
        self.ex_str_attr = 'dtype_out_time'


if __name__ == '__main__':
    unittest.main()
