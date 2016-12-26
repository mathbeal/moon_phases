#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

from astral import Astral
from main import jj2date
from main import phaseslune

from collections import defaultdict
from datetime import datetime

from random import randint
from random import seed
seed(0)

#------------------------------------------------------------------------------
class TestMoonPhase:

    def test_basic(self):
       assert jj2date(2436116.31) == "04/10/1957"
       assert jj2date(1842713.0) == "27/01/0333"
       assert jj2date(2443259.9) == "26/04/1977"

       
def generate_random_date():
    while True:
        yield datetime(randint(2000, datetime.now().year),
                       randint(1,12),
                       randint(1, 28)) 

NB_RANDOM_DATE = 100
        
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
class TestCompareWithCalendar:
    """ """
