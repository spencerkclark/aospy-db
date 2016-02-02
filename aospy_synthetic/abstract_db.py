"""Abstract class defining which methods a backend should be expected to
implement.
"""
from abc import ABCMeta, abstractmethod


class AbstractBackend(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """Initializes the backend object for aospy.  Input arguments may be
        backend-dependent.
        """
        pass

    @abstractmethod
    def add(self, aospy_obj, *args, **kwargs):
        """Adds an instance of the given aospy_obj to the backend"""
        pass

    @abstractmethod
    def delete(self, aospy_obj, *args, **kwargs):
        """Deletes an instance of the given aospy_obj from the backend"""
        pass

    @abstractmethod
    def query(self, aospy_obj, *args, **kwargs):
        """Returns a list of all aospy objects of type aospy_obj that fit
        the provided criteria in *args and **kwargs.
        """
        pass

    class Proj(object):
        __metaclass__ = ABCMeta
        pass

    class Model(object):
        __metaclass__ = ABCMeta
        pass

    class Run(object):
        __metaclass__ = ABCMeta
        pass

    class Var(object):
        __metaclass__ = ABCMeta
        pass

    class Calc(object):
        __metaclass__ = ABCMeta
        pass
