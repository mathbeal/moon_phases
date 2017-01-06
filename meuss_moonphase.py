from meuss_toolbox import jj_to_date
from meuss_toolbox import phaseslune
from meuss_toolbox import date_to_jj

class MeussMoonPhase(object):
    def __init__(self, dateStr):
        self.dateStr = dateStr

    @property
    def moon_phase(self):
        """ """
        jj = self.julian_date
        return jj_to_date(jj)
        
    @property
    def julian_date(self):
        """ """
        return date_to_jj(self.dateStr)

    def __repr__(self):
        return "MeussMoonPhase(%s, %s, %s)" % (self.dateStr,
                                               self.moon_phase,
                                               self.julian_date)

if __name__ == "__main__":
    MMP = MeussMoonPhase('1/8/2017')
    print(MMP)
    
