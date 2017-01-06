# -*- coding:utf-8 -*-
from datetime import date
from datetime import datetime
import julian
import ephem
from astral import Astral

to_datetime = lambda dateStr: datetime.strptime(dateStr, '%d/%m/%Y')

CITY_LOCATION = "Paris"

from meuss_moonphase import MeussMoonPhase

# Setup a code for each moon phase.
PHASE_NEW_MOON = 3
PHASE_FIRST_QUARTER = 5
PHASE_FULL_MOON = 7
PHASE_LAST_QUARTER = 11

# Accurate or not:
OK = 1
NOK = 2

from model_toolbox import Answer

class BaseApi(object):
    def __init__(self):
        self._init()
        
    def _init(self):
        """ """
        pass

    def to_julianDate(self, dateStr):
        """ """
        raise NotImplementedError
    
    def to_moonEnlightment(self, dateStr):
        """ """
        raise NotImplementedError

    def to_moonPhase(self, dateStr):
        """ """
        raise NotImplementedError

#----------------------------------------------------------------------------
class CalendarApi(BaseApi):
    def __init__(self):
        super().__init__()

    def to_moonPhase(self, dateStr):
        """ """
        pass

    def to_julianDate(self, dateStr):
        """ """
        pass
    
    def to_moonEnlightment(self, dateStr):
        """ """
        pass
    
#----------------------------------------------------------------------------
class AstralApi(BaseApi):
    def __init__(self):
        super().__init__()

    def _init(self):
        self.a = Astral()
        self.location = self.a[CITY_LOCATION]
        self.timezone = self.location.timezone
        
        self.translate = {}
        self.translate[0] = PHASE_NEW_MOON
        self.translate[7] = PHASE_FIRST_QUARTER
        self.translate[14] = PHASE_FULL_MOON
        self.translate[21] = PHASE_LAST_QUARTER

    def to_moonEnlightment(self, dateStr):
        """ """
        pass

    def to_julianDate(self, dateStr):
        """ """
        dt = to_datetime(dateStr)
        return self.a._julianday(dt)
        
    def to_moonPhase(self, dateStr):
        """ """
        print(dateStr)
        dt = to_datetime(dateStr)
        moon_phase = self.a.moon_phase(dt)
        try:
            return Answer(OK, self.translate[moon_phase])
        except KeyError:
            if moon_phase <= 7:
                print("~ NEW MOON -- FIRST_QUARTER")
                return Answer(NOK, self.translate[0] * self.translate[7])
            elif moon_phase <= 14:
                print("~ FIRST QUARTER -- FULL MOON")
                return Answer(NOK, self.translate[7] * self.translate[14])
            elif moon_phase <= 21:
                print("~ FULL MOON -- LAST QUARTER")
                return Answer(NOK, self.translate[14] * self.translate[21])
            else:
                print("~ LAST QUARTER -- NEW MOON")
                return Answer(NOK, self.translate[21] * self.translate[0])        

    
#----------------------------------------------------------------------------
class PyEphemApi(BaseApi):
    def __init__(self):
        super().__init__()

    def _init(self):
        pass

    def to_julianDate(self, dateStr):
        dt = to_datetime(dateStr)
        return ephem.julian_date(dt)
        
    def to_moonEnlightment(self, dateStr):
        """Return enlightment rate between 0 and 1
        """
        return ephem.Moon(dateStr).phase  # or moon_phase ?
    
    def to_moonPhase(self, dateStr):
        """ """
        #return ephem.Moon(dateStr)
        dt = to_datetime(dateStr)
        
        def get_phase_on_day(year, month, day):
            """
            source: http://stackoverflow.com/questions/2526815/moon-lunar-phase-algorithm
            Returns a floating-point number from 0-1. where 0=new, 0.5=full, 1=new
            """
            #Ephem stores its date numbers as floating points, which the following uses
            #to conveniently extract the percent time between one new moon and the next
            #This corresponds (somewhat roughly) to the phase of the moon.

            #Use Year, Month, Day as arguments
            _date = ephem.Date(date(year, month, day))

            nnm = ephem.next_new_moon(_date)
            pnm = ephem.previous_new_moon(_date)

            lunation=(_date-pnm)/(nnm-pnm)

            #Note that there is a ephem.Moon().phase() command, but this returns the
            #percentage of the moon which is illuminated. This is not really what we want.

            return lunation
        
        return get_phase_on_day(dt.year, dt.month, dt.day)

#----------------------------------------------------------------------------
class MeussApi(BaseApi):
    def __init__(self):
        super().__init__()

    def _init(self):
        pass
                
    def to_moonPhase(self, dateStr):
        """ """
        pass

    def to_julianDate(self, dateStr):
        """ """
        return MeussMoonPhase(dateStr).julian_date
    
    def to_moonPhase(self, dateStr):
        """ """
        pass
    

#----------------------------------------------------------------------------
if __name__ == "__main__":
    from datetime import date
    from pandas import DataFrame
    from collections import OrderedDict
    
    libs = {'Ephem':PyEphemApi(),
            "Astral": AstralApi(),
            "Calendar": CalendarApi(),
            "Meuss": MeussApi()}

    answers = []
    expected_date_moon = {'12/01/2017':'Nouvelle Lune',
                          '28/01/2017':'Dernier Quartier',
                          '19/01/2017':'Premier Quartier',
                          '5/01/2017':'Pleine Lune'}
    
    for a_day, a_moon in expected_date_moon.items(): 
        tp = OrderedDict()
        tp['Date'] = a_day
        #tp['#Phase'] = a_moon
        tp['#Julian'] = julian.to_jd(to_datetime(a_day))
        for lname, lobj in libs.items():
            #tp['%s_Phase' % lname] = lobj.to_moonPhase(a_day)
            tp['%s_Julian' % lname] = lobj.to_julianDate(a_day)

        answers.append(dict(tp))

    print(DataFrame(answers).to_string())
        
        # print(lobj.to_moonPhase('28/01/2017')) # nouvelle lune
        # print(lobj.to_moonPhase('19/01/2017')) # Dernier Quartier
        # print(lobj.to_moonPhase('5/01/2017'))  # Premier quartier

    
