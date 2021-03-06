#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Source:python.jpvweb.com
"""
from __future__ import division
 
from math import *
from datetime import datetime
from collections import defaultdict
from collections import namedtuple

translate_dict = defaultdict(lambda :dict())

translate_dict['fr'][0] = 'Nouvelle lune'
translate_dict['fr'][1] = 'Premier quartier'
translate_dict['fr'][2] = 'Pleine lune'
translate_dict['fr'][3] = 'Dernier quartier'

translate_dict['en'][0] = 'New Moon'
translate_dict['en'][1] = 'First quarter'
translate_dict['en'][2] = 'Full Moon'
translate_dict['en'][3] = 'Laster quarter'

#------------------------------------------------------------------------------
def to_datetime(str_date):
    """ dd/mm/yyyy to datetime """
    return datetime.strptime(str_date, '%d/%m/%Y')

#------------------------------------------------------------------------------
def is_leap(year):
    """dit si l'année donnée est is_bissextile ou non (True=oui, False=non)"""
    if (year % 4)==0:
        if ((year % 100)==0) and ((year % 400)!=0):
            return False
        else:
            return True
    else:
        return False

#------------------------------------------------------------------------------
def is_postdate(D1, D2):
    """dit si une date D2 'j/m/a' est postérieure ou égale à une autre date D1 'j/m/a'"""
    return to_datetime(D2) >= to_datetime(D1)
 

#------------------------------------------------------------------------------
def jj_to_date(JJ):
    """calcul d'une date (J,M,A) à partir du jour julien des éphémérides"""
    JJ += 0.5
    Z = int(JJ)
    F = JJ - Z
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) /30.6001)
 
    JD = B - D - int(30.6001 * E) + F          # calcul du jour décimal
 
    J = int(JD)                                # calcul du jour
 
    if (E < 13.5):                             # calcul du mois
        M = E - 1
    else:
        M = E - 13
 
    if (M > 2.5):                              # calcul de l'année
        A = C - 4716
    else:
        A = C - 4715
 
    return "%02d/%02d/%04d" % (J, M, A)
 
#------------------------------------------------------------------------------
def k_to_jj(k):
    """calcul de la date de la phase de la lune correspondant à la valeur k"""
 
    # calcul de T en fonction de k (formule 26.3 du livre de Jean MEEUS)
    T = k / 1236.85  
 
    # calcul de JJ = phase moyenne de la lune (formule 26.1 du livre de Jean MEEUS)
    JJ = 2415020.75933 + 29.53058868*k  + 0.0001178*T*T - 0.000000155*T*T*T   \
        + 0.00033 * sin(radians(166.56) + radians(132.87)*T - radians(0.009173)*T*T)
 
    # anomalie moyenne du soleil à l'instant JJ
    M = 359.2242 + 29.10535608*k - 0.0000333*T*T - 0.00000347*T*T*T
 
    # anomalie moyenne de la lune  à l'instant JJ
    MP = 306.0253 + 385.81691806*k + 0.0107306*T*T + 0.00001236*T*T*T
 
    # argument de la latitude de la lune  à l'instant JJ
    F = 21.2964 + 390.67050646*k - 0.0016528*T*T - 0.00000239*T*T*T
 
    # application de corrections selon les décimales de k
    kp = int(round((k - int(k))*100,0))
    if (kp==0) or (kp==50):
        # => nouvelle lune ou pleine lune
        JJ += (0.1734 - 0.000393*T) * sin(radians(M))  \
                + 0.0021 * sin(radians(2*M)) \
                - 0.4068 * sin(radians(MP))  \
                + 0.0161 * sin(radians(2*MP))  \
                - 0.0004 * sin(radians(3*MP))  \
                + 0.0104 * sin(radians(2*F))  \
                - 0.0051 * sin(radians(M+MP))  \
                - 0.0074 * sin(radians(M-MP))  \
                + 0.0004 * sin(radians(2*F+M))  \
                - 0.0004 * sin(radians(2*F-M))  \
                - 0.0006 * sin(radians(2*F+MP))  \
                + 0.0010 * sin(radians(2*F-MP))  \
                + 0.0005 * sin(radians(M+2*MP))
    else:
        JJ += (0.1721 - 0.0004*T) * sin(radians(M))  \
                + 0.0021 * sin(radians(2*M))  \
                - 0.6280 * sin(radians(MP))  \
                + 0.0089 * sin(radians(2*MP))  \
                - 0.0004 * sin(radians(3*MP))  \
                + 0.0079 * sin(radians(2*F))  \
                - 0.0119 * sin(radians(M+MP))  \
                - 0.0047 * sin(radians(M-MP))  \
                + 0.0003 * sin(radians(2*F+M))  \
                - 0.0004 * sin(radians(2*F-M))  \
                - 0.0006 * sin(radians(2*F+MP))  \
                + 0.0021 * sin(radians(2*F-MP))  \
                + 0.0003 * sin(radians(M+2*MP))  \
                + 0.0004 * sin(radians(M-2*MP))  \
                - 0.0003 * sin(radians(2*M+MP))
        if kp==25:
            # => premier quartier
            JJ += 0.0028 - 0.0004*cos(radians(M)) + 0.0003*cos(radians(MP))
        else:
            # => dernier quartier
            JJ += 0.0028 + 0.0004*cos(radians(M)) - 0.0003*cos(radians(MP))

    return JJ

def date_to_jj(dateStr):
    k = date_to_k(dateStr)
    return k_to_jj(k)

def calculphaseslune(k):
    # retour de la date du calendrier grégorien à partir du jour Julien des éphémérides
    return jj_to_date(k_to_jj(k))

#------------------------------------------------------------------------------
def date_to_k(D, as_int=True):
    """utilitaire de calcul de k pour la date D 'j/m/a' (phases de la lune)"""
    dt = to_datetime(D)
    J,M,A = dt.day, dt.month, dt.year     # extraction de la date
    
    # calcul de l'année décimale
    if is_leap(A):
        A += ((0,31,60,91,121,152,182,213,244,274,305,335,366)[M-1] + J) / 366
    else:
        A += ((0,31,59,90,120,151,181,212,243,273,304,334,365)[M-1] + J) / 365
    k = (A-1900)*12.3685
    return int(k) if as_int else k


#------------------------------------------------------------------------------
def to_phase_str(phase_id, lang='fr'):
    try:
        return translate_dict[lang][phase_id]
    except KeyError:
        return str(phase)

#------------------------------------------------------------------------------
def moon_phase_generator(D, lang):
    MoonPhase = namedtuple('MoonPhase', 'phase_id phase_txt date')
    k = date_to_k(D)  # calcul du k initial basé sur D
    def gen_next_phase(p):
        while True:
            yield p
            p = (p+1) % 4
            
    gen_p = gen_next_phase(p=0)
    while True:
        phase_id = next(gen_p)
        MP = MoonPhase(phase_id, to_phase_str(phase_id, lang), calculphaseslune(k))
        yield MP
        k += 0.25

#------------------------------------------------------------------------------
def phaseslune(D, n=1, lang='fr'):
    """Calcul des n dates de phase de la lune qui commence(nt) à la date D 'j/m/a' """
    gen_moon_phase = moon_phase_generator(D, lang)
    
    L = []
    while len(L) != n+1:
        mp = next(gen_moon_phase)
        if not is_postdate(D, mp.date):
            continue
        L.append(mp)
    return L
 
#------------------------------------------------------------------------------
def phaseslune2(D1, D2, lang='fr'):
    """calcul des dates de phase de la lune à partir de D1 'j/m/a' et jusqu'à D2 'j/m/a' exclue"""
    gen_moon_phase = moon_phase_generator(D1, lang)
    
    L = []
    while True:
        mp = next(gen_moon_phase)
        if is_postdate(D1, mp.date):
            if not L:
                L = [mp]
                continue
            if is_postdate(D2, mp.date):
                break
            L.append(mp)
                
    return L

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def samples():
    # calculer la date à partir du jour Julien des Ephémérides
    print(jj_to_date(2436116.31)) # affiche: 04/10/1957
    print(jj_to_date(1842713.0))  # affiche: 27/01/0333
    print(jj_to_date(2443259.9))  # affiche: 26/04/1977
    print("----------------------------------------------------------------------")
 
    # calculer la date de la 1ère phase lunaire postérieure ou égale à la date donnée
    print(phaseslune('1/8/2007'))  # affiche: [[3, '05/08/2007']]
    print(phaseslune('15/11/2007'))  # affiche: [[1, '17/11/2007']]
    print(phaseslune('25/7/2008'))  # affiche: [[3, '25/07/2008']]
    print("----------------------------------------------------------------------")
 
    # calculer les n=10 dates des phases lumaires commençant à la date D donnée
    d='1/1/2017'
    n=10
    print(d, n)
    L=phaseslune(d,n)
    for i in range(0,n):
        print(L[i])
    # affiche:
    # [0, '08/01/2008']
    # [1, '15/01/2008']
    # [2, '22/01/2008']
    # [3, '30/01/2008']
    # [0, '07/02/2008']
    # [1, '14/02/2008']
    # [2, '21/02/2008']
    # [3, '29/02/2008']
    # [0, '07/03/2008']
    # [1, '14/03/2008']
    print("----------------------------------------------------------------------")
 
    # calculer les dates des phases lumaires commençant à la date D1 donnée et antérieures à D2
    D1='1/7/2008'
    D2='1/8/2008'
    
    print(D1,D2)
    L=phaseslune2(D1,D2)
    for i in range(0,len(L)):
        print(L[i])
    
    # affiche: 
    # [0, '03/07/2008']
    # [1, '10/07/2008']
    # [2, '18/07/2008']
    # [3, '25/07/2008']
    print("*******")
    # cas d'un intervalle trop faible:
    print(phaseslune2('1/7/2009', '2/7/2009')) # affiche: [[]] car aucune date de convient
    print("----------------------------------------------------------------------")
    
    
    # affichage plus facile à lire:
    p=["nouvelle lune","premier quartier","pleine lune","dernier quartier"]
 
    x=phaseslune('25/7/2008')
    print("###",x[0][0])
    print(x[0][1], ' : ', p[x[0][0]])  # affiche: "25/07/2008  :  dernier quartier"
    
    x=phaseslune('5/3/2009')
    print(x[0][1], ' : ', p[x[0][0]])  # affiche: 11/03/2009  :  pleine lune)
    
    x=phaseslune('1/7/2009')
    print(x)
    print(x[0][1], ' : ', p[x[0][0]])  # affiche: 07/07/2009  :  pleine lun)
    
    #https://stackoverflow.com/questions/2526815/moon-lunar-phase-algorithm
    # [(2013/1/11 19:43:37, 'new'), (2013/1/27 04:38:22, 'full'), (2013/2/10 07:20:06, 'new'), (2013/2/25 20:26:03, 'full'), (2013/3/11 19:51:00, 'new'), (2013/3/27 09:27:18, 'full'), (2013/4/10 09:35:17, 'new'), (2013/4/25 19:57:06, 'full'), (2013/5/10 00:28:22, 'new'), (2013/5/25 04:24:55, 'full'), (2013/6/8 15:56:19, 'new'), (2013/6/23 11:32:15, 'full'), (2013/7/8 07:14:16, 'new'), (2013/7/22 18:15:31, 'full'), (2013/8/6 21:50:40, 'new'), (2013/8/21 01:44:35, 'full'), (2013/9/5 11:36:07, 'new'), (2013/9/19 11:12:49, 'full'), (2013/10/5 00:34:31, 'new'), (2013/10/18 23:37:39, 'full'), (2013/11/3 12:49:57, 'new'), (2013/11/17 15:15:44, 'full'), (2013/12/3 00:22:22, 'new'), (2013/12/17 09:28:05, 'full'), (2014/1/1 11:14:10, 'new'), (2014/1/16 04:52:10, 'full')]######################################################################


if __name__ == "__main__":
    samples()
