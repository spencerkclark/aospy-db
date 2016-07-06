class TestProj(object):
    ancestors = ['Proj']
    aospy_cls = 'Proj'


class TestModel(object):
    ancestors = ['Proj', 'Model']
    aospy_cls = 'Model'


class TestRun(object):
    ancestors = ['Proj', 'Model', 'Run']
    aospy_cls = 'Run'


class TestCalc(object):
    ancestors = ['Proj', 'Model', 'Run', 'Calc', 'Var', 'Units', 'Region']
    aospy_cls = 'Calc'


class TestVar(object):
    ancestors = ['Var', 'Units']
    aospy_cls = 'Var'


class TestUnits(object):
    ancestors = ['Units']
    aospy_cls = 'Units'


class TestRegion(object):
    ancestors = ['Region']
    aospy_cls = 'Region'
