#!/usr/bin/env python3

from fire import Fire
import pytz
import datetime as dt
import math


def main():
    GMT = pytz.timezone("Etc/GMT")

    #print()
    year = 365*24*3600
    t12 = 30.07 * year

    lambd = math.log(2)/t12
    #print("i... LAMBDA = ",lambd)

    nucl="137Cs"
    ene=661
    act0 = 30.2e+3
    area = 12641
    darea = math.sqrt(area)
    tmeasure = 3600
    time0="2022-06-03T12:00:00-05:00"


    print(f"{nucl} E={ene} Area={area} / {tmeasure} sec.  Original activity {act0}")
    print()

    time0 = dt.datetime.fromisoformat(time0)
    time0gmt = time0.astimezone(GMT)
    print(f"i... activity determined: {time0}")
    print(f"i... activity        gmt: {time0gmt}")

    now = dt.datetime.now()
    #print( GMT.localize(now) )
    #print(now)
    #print(now.astimezone(GMT) )
    nowgmt = now.astimezone(GMT)
    deltat = (nowgmt - time0gmt).total_seconds()
    print( f"i... time until      now: {nowgmt - time0gmt}")

    final = math.exp(-lambd*deltat) * act0

    print("i...  ACTIVITY NOW      :",final)

    ratenow = area/tmeasure
    print(f"i... rate   now         : {ratenow:.3f} cps")

    print(f"i... efficiency = {ratenow/final*100:.3f} %")

if __name__=="__main__":
    Fire(main)
