#! /usr/bin/env python
"""Main script for automating computations using aospy."""
import itertools

import colorama

from aospy_synthetic.var import Var
from aospy_synthetic.proj import Proj
from aospy_synthetic.model import Model
from aospy_synthetic.run import Run
from aospy_synthetic.calc import Calc, CalcInterface
import aospy_synthetic.io as io
import aospy_synthetic.utils as utils

# import aospy_synthetic
# import aospy_user

import units
import calcs
import variables
from cases import *
from idealized import *
from models import *
from example_projects import *
import obj_from_name as aospy_user


class MainParams(object):
    """Container for parameters specified in main routine."""
    pass


class MainParamsParser(object):
    """Interface between specified parameters and resulting CalcSuite."""
    def str_to_aospy_obj(self, proj, model, var, region):
        proj_out = aospy_user.to_proj(proj)
        model_out = aospy_user.to_model(model, proj_out)
        var_out = aospy_user.to_var(var)
        region_out = None
#        region_out = aospy_user.to_region(region, proj=proj_out)
        return proj_out, model_out, var_out, region_out

    def aospy_obj_to_iterable(self, proj, model, var, region):
        return [aospy_user.to_iterable(obj)
                for obj in (proj, model, var, region)]

    def str_to_aospy_iterable(self, proj, model, var, region):
        projo, modelo, varo, regiono = self.str_to_aospy_obj(proj, model,
                                                             var, region)
        return self.aospy_obj_to_iterable(projo, modelo, varo, regiono)

    def create_child_run_obj(self, models, runs, proj):
        """Create child Run object(s) for each Model object."""
        run_objs = []
        for model in models:
            for run in runs:
                try:
                    run_objs.append(aospy_user.to_run(run, model, proj))
                except AttributeError as ae:
                    print(ae)
        # If flat list, return the list.  If nested, then flatten it.
        if all([isinstance(r, Run) for r in run_objs]):
            return [run_objs[0]]
        else:
            return list(itertools.chain.from_iterable(run_objs))

    def __init__(self, main_params):
        """Turn all inputs into aospy-ready objects."""
        self.__dict__ = vars(main_params)
        self.proj, self.model, self.var, self.region = (
            self.str_to_aospy_iterable(main_params.proj, main_params.model,
                                       main_params.var, [False])
            )
        self.run = self.create_child_run_obj(self.model, self.run, self.proj)
        self.region = [False]


class CalcSuite(object):
    """Creates suite of Calc objects based on inputted specifications. """
    def __init__(self, calc_suite_interface):
        self.__dict__ = vars(calc_suite_interface)

    def print_params(self):
        pairs = (
            ('Project', self.proj),
            ('Models', self.model),
            ('Runs', self.run),
            ('Ensemble members', self.ens_mem),
            ('Variables', self.var),
            ('Year ranges', self.date_range),
            ('Geographical regions', [self.region]),
            ('Time interval of input data', self.intvl_in),
            ('Time interval for averaging', self.intvl_out),
            ('Input data time type', self.dtype_in_time),
            ('Input data vertical type', self.dtype_in_vert),
            ('Output data time type', self.dtype_out_time),
            ('Output data vertical type', self.dtype_out_vert),
            ('Vertical levels', self.level),
            ('Year chunks', self.chunk_len),
            ('Compute this data', self.compute),
            ('Print this data', self.print_table)
        )
        print('')
        colorama.init()
        color_left = colorama.Fore.BLUE
        color_right = colorama.Fore.RESET
        for left, right in pairs:
            print(color_left, left, ':', color_right, right)
        print(colorama.Style.RESET_ALL)

    def prompt_user_verify(self):
        if not raw_input("Proceed using these parameters? ").lower() == 'y':
            raise IOError('\nExecution cancelled by user.')

    def create_params_all_calcs(self):
        attr_names = ('proj',
                      'model',
                      'run',
                      'ens_mem',
                      'var',
                      'date_range',
                      'level',
                      'region',
                      'intvl_in',
                      'intvl_out',
                      'dtype_in_time',
                      'dtype_out_time',
                      'dtype_in_vert',
                      'dtype_out_vert',
                      'verbose',
                      'chunk_len')
        attrs = tuple([getattr(self, name) for name in attr_names])

        # Each permutation becomes a dictionary, with the keys being the attr
        # names and the values being the corresponding value for that
        # permutation.  These dicts can then be directly passed to the
        # CalcInterface class to make the Calc objects.
        permuter = itertools.product(*attrs)
        param_combos = []
        for permutation in permuter:
            param_combos.append(dict(zip(attr_names, permutation)))
        return param_combos

    def create_calcs(self, param_combos, exec_calcs=False, print_table=False):
        """Iterate through given parameter combos, creating needed Calcs."""
        calcs = []
        for params in param_combos:
            try:
                calc_int = CalcInterface(**params)
            # except AttributeError as ae:
                # print('aospy warning:', ae)
            except:
                raise
            else:
                calc = Calc(calc_int)
                if exec_calcs:
                    try:
                        calc.compute()
                    except:
                        raise
                        # print('Calc %s failed.  Skipping.' % calc)
                    else:
                        if print_table:
                            pass
                            #print("%.1f" % calc.load('reg.av', False,
                            #                         calc_int.region['sahel'],
                            #                         plot_units=False))

                calcs.append(calc)
        return calcs

    def exec_calcs(self, calcs):
        return [calc.compute() for calc in calcs]

    def print_results(self, calcs):
        for calc in calcs:
            for region in calc.region.values():
                print([calc.load(self.dtype_out_time[0],
                                 # dtype_out_vert=params[-2],
                                 region=region, plot_units=True)])


def main(main_params):
    """Main script for interfacing with aospy."""
    # Instantiate objects and load default/all models, runs, and regions.
    cs = CalcSuite(MainParamsParser(main_params))
    cs.print_params()
    cs.prompt_user_verify()
    param_combos = cs.create_params_all_calcs()
    calcs = cs.create_calcs(param_combos, exec_calcs=True, print_table=True)
    print('\n\tVariable time averages and statistics:')
    # if main_params.compute:
        # cs.exec_calcs(calcs)
    # if main_params.print_table:
        # cs.print_results(calcs)
    print("Calculations finished.")
    return calcs

if __name__ == '__main__':

    mp = MainParams()
    mp.proj = 'example'
#    mp.proj = 'dargan_test'
    mp.model = ['am2']
#    mp.model = ['am2_reyoi']
#    mp.model = ['dargan']
    mp.run = [('am2_control','am2_tropics', 'am2_extratropics','am2_tropics+extratropics')]
#    mp.run = [('am2_HadISST_control', 'am2_reyoi_extratropics_sp_SI', 'am2_reyoi_tropics_sp_SI')]
#    mp.run = ['control_T85']
#    mp.run = ['control_alb_T42']
    mp.ens_mem = [False]
#    mp.var = ['Q_diff']
#    mp.var = ['mse']
#    mp.var = ['msf']
#    mp.var = ['mse']
#    mp.var = ['precip', 't_surf', 'Q_diff', 'ucomp', 'vcomp', 'mse']
#    mp.var = ['dp_sigma', 'ucomp', 'vcomp', 'mse']
#    mp.var = ['net_sw']
    mp.var = ['tdt_sw', 'tdt_lw', 'tdt_vdif', 'qdt_vdif']#, 'vcomp_mb', 'mse']
#    mp.var = ['olr']
#    mp.var = ['dp_sigma']
#    mp.var = ['olr','t_surf','swdn_toa','lwdn_sfc','swdn_sfc','lwup_sfc','evap','precip',
#              'swup_toa','swup_toa_clr','swdn_sfc_clr','lwup_sfc_clr','lwdn_sfc_clr',
#              ]#, 'mse_vert_advec_upwind']
    #mp.date_range = [('1983-01-01', '2012-12-31')]
    mp.date_range = [('0021-01-01', '0080-12-31')]
#    mp.date_range = [('1983-01-01', '1998-12-31')]
#    mp.date_range = [('0001-12-27', '0002-12-22')]
    mp.region = []
#    mp.region = ['sahel', 'nh', 'sh', 'nh_tropics', 'sh_tropics',
#                 'nh_extratropics', 'sh_extratropics']
    mp.intvl_in = ['monthly']
#    mp.intvl_in = ['20-day']
#    mp.intvl_in = ['20-day']
    mp.intvl_out = ['ann', 'jas', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] # 'jas', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    mp.dtype_in_time = ['ts']
    mp.dtype_in_vert = [False]
#    mp.dtype_in_vert = ['pressure']
    mp.dtype_in_vert = ['sigma']
    # mp.dtype_out_time = [('reg.av',)]
    mp.dtype_out_time = [('av')]# 'ts', 'reg.av', 'reg.ts')]# 'reg.av', 'reg.ts')]
#    mp.dtype_out_time = [('av', 'reg.av', 'reg.ts')]
#    mp.dtype_out_time = [('av','reg.std','reg.av','reg.ts')]
    mp.dtype_out_vert = ['vert_int']
#    mp.dtype_out_vert = [False]
    mp.level = [False]
    mp.chunk_len = [False]
    mp.verbose = [True]
    mp.compute = True
    mp.print_table = False

    calcs = main(mp)

    # Unusual dates seem to work -- test
    # mp.intvl_out = [12]
    # mp.dtype_out_time = [('ts')]
    # This returns three points for Dec; this is expected
    # the number of days is at the end of the averaging period in the
    # idealized model.
