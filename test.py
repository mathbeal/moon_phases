#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

from astral import Astral
from main import jj2date
from main import phaseslune
from main import is_leap

from collections import defaultdict
from datetime import datetime

from random import randint
from random import seed
seed(0)

import calendar
NB_RANDOM_DATE = 100

#------------------------------------------------------------------------------
def generate_random_date():
    while True:
        yield datetime(randint(2000, datetime.now().year),
                       randint(1,12),
                       randint(1, 28)) 

#------------------------------------------------------------------------------
class TestMoonPhaseFunctions:

    def test_jj2date(self):
       assert jj2date(2436116.31) == "04/10/1957"
       assert jj2date(1842713.0) == "27/01/0333"
       assert jj2date(2443259.9) == "26/04/1977"
       
    def test_leapyear(self):
        for year in range(0, 2020):
            assert calendar.isleap(year) == is_leap(year), 'is_leap error in %d' % year
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class TestCompareWithAstralLib:
    """ Error in comparison with Astral on few dates : 4% error"""
    def setup(self):
        self.a = Astral()
        self.answers_set = set()
        
    def astral_to_currentcode(self, astral_code):
        self.answers_set.add(astral_code)
        if astral_code == 0: return 0
        if astral_code <= 7: return 1
        if astral_code <= 14: return 2
        if astral_code <= 21: return 3
        return 0

    def compare_moon_phase(self, test_date):
        str_date = test_date.strftime('%d/%m/%Y')
        phase = phaseslune(str_date)[0]
        status = self.astral_to_currentcode(self.a.moon_phase(test_date)) == phase.phase_id
        if status == False:
            print(str_date, "Astral", self.a.moon_phase(test_date), "Cur", phase.phase_id)
        return status
    
    def test_compare(self):
        gen_test_dates = generate_random_date()
        total = defaultdict(int)
        total[True] = total[False] = 0
        
        for idx in range(NB_RANDOM_DATE):
            test_date = next(gen_test_dates)
            status = self.compare_moon_phase(test_date)
            total[status] += 1
            
        print("Conformite %.2f %%" % (100 * total[True] / sum(total.values())))
        print("Astral set: ", sorted(self.answers_set))
        assert total[False] == 0.0, 'must all be True'
        assert total[True] == 100.0, 'must all be True'


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
import ephem
class TestCompareWithPyEphem:
    """ 
    """
        
    # def test_jj2date(self):
    #     assert jj2date(2436116.31) == "04/10/1957"
    #     assert jj2date(1842713.0) == "27/01/0333"
    #     assert jj2date(2443259.9) == "26/04/1977"
        
    #     assert ephem.Date('1957/10/04') == jj2date(2436116.31), '%.2f' % ephem.Date('1957/10/04')
        
        
    def test_compare(self):

        def build_test_set():
            test_set = defaultdict(list)
            fm_date, fq_date, nm_date, lq_date = ['1984'] * 4

            to_str_date = lambda dt: dt.strftime('%d/%m/%Y')
            
            for i in range(NB_RANDOM_DATE):
                
                # next full moon (fm)
                fm_date = ephem.next_full_moon(fm_date)
                test_set['fm'].append(to_str_date(fm_date.datetime()))
            
                # next first quater moon (fq)
                fq_date = ephem.next_first_quarter_moon(fq_date)
                test_set['fq'].append(to_str_date(fq_date.datetime()))

                # next new moon (nm)
                nm_date = ephem.next_new_moon(nm_date)
                test_set['nm'].append(to_str_date(nm_date.datetime()))

                # last quarter moon (lq)
                lq_date = ephem.next_last_quarter_moon(lq_date)
                test_set['lq'].append(to_str_date(lq_date.datetime()))
                
            return test_set

        test_set = build_test_set()
        conformite = defaultdict(lambda: defaultdict(int))
        
        for dt in test_set['fm']:
            for moonphase in phaseslune(dt):
                conformite['fm'][moonphase.phase_txt == 'Pleine lune'] += 1 # 'fm %s' % dt)

        for dt in test_set['fq']:
            for moonphase in phaseslune(dt):
                conformite['fq'][moonphase.phase_txt == 'Premier quartier'] += 1 # 'fq %s' % dt)

        for nm in test_set['nm']:
            for moonphase in phaseslune(dt):
                conformite['nm'][moonphase.phase_txt == 'Nouvelle lune'] +=1 # 'nm %s' % dt)

        for lq in test_set['lq']:
            for moonphase in phaseslune(dt):
                conformite['lq'][moonphase.phase_txt == 'Dernier quartier'] +=1 # 'lq %s' % dt)

        from pprint import pprint
        pprint(conformite)


