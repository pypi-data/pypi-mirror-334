#!/usr/bin/env python3

import scipy.integrate as integrate


################################
# i need interpolation now.... #
#https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np

import urllib3
from bs4 import BeautifulSoup

from fire import Fire

import re
from console import fg,bg

import sys
import pandas as pd
import importlib_resources
import os

# ----------- z correspond the name
elements=['n','H','He','Li','Be','B','C','N','O','F','Ne',
                        'Na','Mg','Al','Si','P','S','Cl','Ar',
                        'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',  'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
                        'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
                        'Cs', 'Ba',
                        'La','Ce','Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu','Hf',
                        'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi',
                        'Po', 'At', 'Rn', 'Fr','Ra', 'Ac',  'Th', 'Pa', 'U',
                        'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es',
                        'Fm', 'Md', 'No', 'Lr','Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt',
                        'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']; #110-118

# --------- name corresponds the list of stables
# stable_isotopes[ elements[6] ]  # will also give 14C etc...
stable_isotopes={ "H":[1,2,3],
"He":[3,4],
"Li":[6,7],
"Be":[9],
"B":[10,11],
"C":[12,13,14],
"N":[14,15],
"O":[16,17,18],
"F":[19],
"Ne":[20,21,22],
"Na":[23,22],
"Mg":[24,25,26],
"Al":[27],
"Si":[28,29,30],
"P":[31],
"S":[32,33,34,36],
"Cl":[35,37,36],
"Ar":[36,38,40,39],
"K":[39,40,41],
"Ca":[40,42,43,44,46,48,41],
"Sc":[45],
"Ti":[46,47,48,49,50],
"V":[50,51],
"Cr":[50,52,53,54],
"Mn":[55,53],
"Fe":[54,56,57,58],
"Co":[59,60],
"Ni":[58,60,61,62,64],
"Cu":[63,65],
"Zn":[64,66,67,68,70],
"Ga":[69,71],
"Ge":[70,72,73,74,76],
"As":[75],
"Se":[74,76,77,78,80,82,79],
"Br":[79,81],
"Kr":[78,80,82,83,84,86,85],
"Rb":[85,87],
"Sr":[84,86,87,88],
"Y":[89],
"Zr":[90,91,92,94,96],
"Nb":[93],
"Mo":[92,94,95,96,97,98,100],
"Tc":[98,97,99],
"Ru":[96,98,99,100,101,102,104],
"Rh":[103],
"Pd":[102,104,105,106,108,110],
"Ag":[107,109],
"Cd":[106,108,110,111,112,113,114,116],
"In":[113,115],
"Sn":[112,114,115,116,117,118,119,120,122,124],
"Sb":[121,123,125],
"Te":[120,122,123,124,125,126,128,130],
"I":[127,129],
"Xe":[124,126,128,129,130,131,132,134,136],
"Cs":[133,134,135,137],
"Ba":[130,132,134,135,136,137,138,133],
"La":[138,139,137],
"Ce":[136,138,140,142],
"Pr":[141],
"Nd":[142,143,144,145,146,148,150],
"Pm":[145,146,147],
"Sm":[144,147,148,149,150,152,154,151],
"Eu":[151,153,152,154,155],
"Gd":[152,154,155,156,157,158,160],
"Tb":[159,157,160],
"Dy":[156,158,160,161,162,163,164],
"Ho":[165],
"Er":[162,164,166,167,168,170],
"Tm":[169,171],
"Yb":[168,170,171,172,173,174,176],
"Lu":[175,176,173,174],
"Hf":[174,176,177,178,179,180],
"Ta":[180,181],
"W":[180,182,183,184,186],
"Re":[185,187],
"Os":[184,186,187,188,189,190,192],
"Ir":[191,193],
"Pt":[190,192,194,195,196,198],
"Au":[197],
"Hg":[196,198,199,200,201,202,204],
"Tl":[203,205,204],
"Pb":[204,206,207,208],
"Bi":[209,207],
"Po":[208,209,210],
"At":[210,211],
"Rn":[210,211,222],
"Fr":[212,222,223],
"Ra":[226,228],
"Ac":[225,227],
"Th":[230,232,229],
"Pa":[231,233],
"U":[233,234,235,238,236],
"Np":[236,237],
"Pu":[238,239,240,241,242,244],
"Am":[241,243],
"Cm":[243,244,245,246,247,248],
"Bk":[247,249],
"Cf":[249,250,251,252],
"Es":[252,254],
"Fm":[253,257],
"Md":[258,260],
"No":[255,259],
"Lr":[261,262],
"Rf":[265,267],
"Db":[268,270],
"Sg":[269,271],
"Bh":[270,274],
"Hs":[269,270],
"Mt":[276,278],
"Ds":[280,281],
"Rg":[281,282],
"Cn":[283,285],
"Nh":[285,286],
"Fl":[287,288,289],
"Mc":[288,289,290],
"Lv":[291,292,293],
"Ts":[293,294],
"Og":[294] }


abundances = {
'H1' : 99.9885,
'H2' : 0.0115,
'He3' : 0.000134,
'He4' : 99.999866,
'Li6' : 7.59,
'Li7' : 92.41,
'Be9' : 100.0,
'B10' : 19.9,
'B11' : 80.1,
'C12' : 98.93,
'C13' : 1.07,
'N14' : 99.636,
'N15' : 0.364,
'O16' : 99.757,
'O17' : 0.038,
'O18' : 0.205,
'F19' : 100.0,
'Ne20' : 90.48,
'Ne21' : 0.27,
'Ne22' : 9.25,
'Na23' : 100.0,
'Mg24' : 78.99,
'Mg25' : 10.0,
'Mg26' : 11.01,
'Al27' : 100.0,
'Si28' : 92.223,
'Si29' : 4.685,
'Si30' : 3.092,
'P31' : 100.0,
'S32' : 94.99,
'S33' : 0.75,
'S34' : 4.25,
'S36' : 0.01,
'Cl35' : 75.76,
'Cl37' : 24.24,
'Ar36' : 0.3336,
'Ar38' : 0.0629,
'Ar40' : 99.6035,
'K39' : 93.2581,
'K40' : 0.0117,
'K41' : 6.7302,
'Ca40' : 96.94,
'Ca42' : 0.647,
'Ca43' : 0.135,
'Ca44' : 2.09,
'Ca46' : 0.004,
'Ca48' : 0.187,
'Sc45' : 100.0,
'Ti46' : 8.25,
'Ti47' : 7.44,
'Ti48' : 73.72,
'Ti49' : 5.41,
'Ti50' : 5.18,
'V50' : 0.25,
'V51' : 99.75,
'Cr50' : 4.345,
'Cr52' : 83.789,
'Cr53' : 9.501,
'Cr54' : 2.365,
'Mn55' : 100.0,
'Fe54' : 5.845,
'Fe56' : 91.754,
'Fe57' : 2.119,
'Fe58' : 0.282,
'Co59' : 100.0,
'Ni58' : 68.077,
'Ni60' : 26.223,
'Ni61' : 1.1399,
'Ni62' : 3.6346,
'Ni64' : 0.9255,
'Cu63' : 69.15,
'Cu65' : 30.85,
'Zn64' : 49.17,
'Zn66' : 27.73,
'Zn67' : 4.04,
'Zn68' : 18.45,
'Zn70' : 0.61,
'Ga69' : 60.108,
'Ga71' : 39.892,
'Ge70' : 20.57,
'Ge72' : 27.45,
'Ge73' : 7.75,
'Ge74' : 36.5,
'Ge76' : 7.73,
'As75' : 100.0,
'Se74' : 0.89,
'Se76' : 9.37,
'Se77' : 7.63,
'Se78' : 23.77,
'Se80' : 49.61,
'Se82' : 8.73,
'Br79' : 50.69,
'Br81' : 49.31,
'Kr78' : 0.355,
'Kr80' : 2.286,
'Kr82' : 11.593,
'Kr83' : 11.5,
'Kr84' : 56.987,
'Kr86' : 17.279,
'Rb85' : 72.17,
'Rb87' : 27.83,
'Sr84' : 0.56,
'Sr86' : 9.86,
'Sr87' : 7.0,
'Sr88' : 82.58,
'Y89' : 100.0,
'Zr90' : 51.45,
'Zr91' : 11.22,
'Zr92' : 17.15,
'Zr94' : 17.38,
'Zr96' : 2.8,
'Nb93' : 100.0,
'Mo92' : 14.53,
'Mo94' : 9.15,
'Mo95' : 15.84,
'Mo96' : 16.67,
'Mo97' : 9.6,
'Mo98' : 24.39,
'Mo100' : 9.82,
'Ru96' : 5.54,
'Ru98' : 1.87,
'Ru99' : 12.76,
'Ru100' : 12.6,
'Ru101' : 17.06,
'Ru102' : 31.55,
'Ru104' : 18.62,
'Rh103' : 100.0,
'Pd102' : 1.02,
'Pd104' : 11.14,
'Pd105' : 22.33,
'Pd106' : 27.33,
'Pd108' : 26.46,
'Pd110' : 11.72,
'Ag107' : 51.839,
'Ag109' : 48.161,
'Cd106' : 1.25,
'Cd108' : 0.89,
'Cd110' : 12.49,
'Cd111' : 12.8,
'Cd112' : 24.13,
'Cd113' : 12.22,
'Cd114' : 28.73,
'Cd116' : 7.49,
'In113' : 4.29,
'In115' : 95.71,
'Sn112' : 0.97,
'Sn114' : 0.66,
'Sn115' : 0.34,
'Sn116' : 14.54,
'Sn117' : 7.68,
'Sn118' : 24.22,
'Sn119' : 8.59,
'Sn120' : 32.58,
'Sn122' : 4.63,
'Sn124' : 5.79,
'Sb121' : 57.21,
'Sb123' : 42.79,
'Te120' : 0.09,
'Te122' : 2.55,
'Te123' : 0.89,
'Te124' : 4.74,
'Te125' : 7.07,
'Te126' : 18.84,
'Te128' : 31.74,
'Te130' : 34.08,
'I127' : 100.0,
'Xe124' : 0.0952,
'Xe126' : 0.089,
'Xe128' : 1.9102,
'Xe129' : 26.4006,
'Xe130' : 4.071,
'Xe131' : 21.2324,
'Xe132' : 26.9086,
'Xe134' : 10.4357,
'Xe136' : 8.8573,
'Cs133' : 100.0,
'Ba130' : 0.106,
'Ba132' : 0.101,
'Ba134' : 2.417,
'Ba135' : 6.592,
'Ba136' : 7.854,
'Ba137' : 11.232,
'Ba138' : 71.698,
'La138' : 0.08881,
'La139' : 99.91119,
'Ce136' : 0.185,
'Ce138' : 0.251,
'Ce140' : 88.45,
'Ce142' : 11.114,
'Pr141' : 100.0,
'Nd142' : 27.152,
'Nd143' : 12.174,
'Nd144' : 23.798,
'Nd145' : 8.293,
'Nd146' : 17.189,
'Nd148' : 5.756,
'Nd150' : 5.638,
'Sm144' : 3.07,
'Sm147' : 14.99,
'Sm148' : 11.24,
'Sm149' : 13.82,
'Sm150' : 7.38,
'Sm152' : 26.75,
'Sm154' : 22.75,
'Eu151' : 47.81,
'Eu153' : 52.19,
'Gd152' : 0.2,
'Gd154' : 2.18,
'Gd155' : 14.8,
'Gd156' : 20.47,
'Gd157' : 15.65,
'Gd158' : 24.84,
'Gd160' : 21.86,
'Tb159' : 100.0,
'Dy156' : 0.056,
'Dy158' : 0.095,
'Dy160' : 2.329,
'Dy161' : 18.889,
'Dy162' : 25.475,
'Dy163' : 24.896,
'Dy164' : 28.26,
'Ho165' : 100.0,
'Er162' : 0.139,
'Er164' : 1.601,
'Er166' : 33.503,
'Er167' : 22.869,
'Er168' : 26.978,
'Er170' : 14.91,
'Tm169' : 100.0,
'Yb168' : 0.123,
'Yb170' : 2.982,
'Yb171' : 14.09,
'Yb172' : 21.68,
'Yb173' : 16.103,
'Yb174' : 32.026,
'Yb176' : 12.996,
'Lu175' : 97.401,
'Lu176' : 2.599,
'Hf174' : 0.16,
'Hf176' : 5.26,
'Hf177' : 18.6,
'Hf178' : 27.28,
'Hf179' : 13.62,
'Hf180' : 35.08,
'Ta181' : 99.98799,
'W180' : 0.12,
'W182' : 26.5,
'W183' : 14.31,
'W184' : 30.64,
'W186' : 28.43,
'Re185' : 37.4,
'Re187' : 62.6,
'Os184' : 0.02,
'Os186' : 1.59,
'Os187' : 1.96,
'Os188' : 13.24,
'Os189' : 16.15,
'Os190' : 26.26,
'Os192' : 40.78,
'Ir191' : 37.3,
'Ir193' : 62.7,
'Pt190' : 0.012,
'Pt192' : 0.782,
'Pt194' : 32.86,
'Pt195' : 33.78,
'Pt196' : 25.21,
'Pt198' : 7.36,
'Au197' : 100.0,
'Hg196' : 0.15,
'Hg198' : 9.97,
'Hg199' : 16.87,
'Hg200' : 23.1,
'Hg201' : 13.18,
'Hg202' : 29.86,
'Hg204' : 6.87,
'Tl203' : 29.52,
'Tl205' : 70.48,
'Pb204' : 1.4,
'Pb206' : 24.1,
'Pb207' : 22.1,
'Pb208' : 52.4,
'Bi209' : 100.0,
'Th232' : 100.0,
'U234' : 0.0054,
'U235' : 0.7204,
'U238' : 99.2742,
} # abundances



# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================


def get_data_path():
    filename = f"tendl21"
    file_path = importlib_resources.files("nuphy2").joinpath("data/"+filename)
    return file_path

# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================


def plot_spline( ax, tckslist , Emax=50, label="label" ,  clear=False, logy=True):
    """
    serves for the plot_az ..... plots the list of data: [x,y] label
    """
    mymin=1
    for tcks2 in tckslist:   # list of pairs evidently
        tcks=tcks2[0]
        label=tcks2[1]
        if tcks is None:
            continue
        mymin = min( mymin, tcks[1].min() ) # minimum for yaxis
        #print( tcks )
        #print( type(tcks) )

        if label[-1]=="m":
            ax.plot( tcks[0], tcks[1],'-.',label=label)
        else:
            ax.plot( tcks[0], tcks[1],'-',label=label)

        # Emin=min(tcks.x) # MeV
        # # Emax=max(tcks.x) # MeV

        # unew = np.arange( Emin, Emax, 0.0001)
        # out=tcks(unew)

        # #out = interpolate.splev(unew, tcks, der=0)
        # #xnew = np.linspace(x[0], x[-1], num=10000 , endpoint=True )
        # #ynew = interpolate.splev(xnew, tcks, der=0)
        # #plt.plot( x,y , '.', xnew, ynew ,'-' )
        # plt.plot(  unew, out ,'-' , label=label)

        ax.legend( fontsize=8)

    if logy:
        plt.yscale("log")
        plt.ylim( max( [1e-2, mymin ]) )
    plt.xlim( [0, Emax] )
    plt.grid()
    #plt.show()


# ===========================================================================
# ===========================================================================
# ===========================================================================

# ===========================================================================


def prep_tendl( proj, targ, product,  xsset="tot" ):
    """
    prepares urls ... product Rb86??? or what?
    """
    if proj=="h1": p1="proton"
    if proj=="h2": p1="deuteron"
    if proj=="h3": p1="triton"
    if proj=="he3": p1="he3"
    if proj=="he4": p1="alpha"

    LABEL = "TENDL21_"+targ+"("+proj+",x)"+product  #TENDL21_sr88(h2,x)Rb86_02

    t=targ.capitalize()
    r=product.capitalize()
    t2,t3,r2,r3="","","",""

    extension = xsset
    if r[-3]=='_':   #   _00  _01  _10
        extension = f"L{str(r[-2:])}.ave"
        #extension = "L00.ave"
        r = r[:-3]

    #=====target create zeroes mg26 -> Mg026  ---> tzero
    for i in range(len(t)):
        if not t[i].isdigit():
            t2=t2+ t[i]
        else:
            t3=t3+ t[i]
        #print( i,t[i], t[i].isdigit() )
    tzero="{}{}".format( t2,t3.zfill(3) ) #zerofill
    #print(t, t2, t3)


    #=== product/residual ========= -> r
    for i in range(len(r)):
        if not r[i].isdigit():
            r2=r2+ r[i]
        else:
            r3=r3+ r[i]
        #print( i,r[i], r[i].isdigit() )
    r="{}{}".format( r2,r3.zfill(3) ) #zerofill
    #print(r, r2, r3)


    #================= Find Z Of Element  -> rZ
    if t2 in elements:
        tZ=elements.index(t2)
    else:
        print(f"{bg.red}X... no such element{bg.default}",t2)
        sys.exit(1)#quit()
    if r2 in elements:
        rZ=elements.index(r2)
    else:
        print(f"{bg.red}X... no such element{bg.default}",r2)
        sys.exit(1)#quit()

    t1=""

    return p1,t,t2,t3,tzero,r2,r3,rZ,tZ,LABEL,extension


# ===========================================================================
# ===========================================================================
# ===========================================================================

def get_tendl_levels( proj, targ, product,  xsset="tot" ):
    """
    gets levels observed in datafiles
    """
    p1,t,t2,t3,tzero,r2,r3,rZ,tZ,LABEL,extension =  prep_tendl( proj, targ, product )

    rname = "rp{}{}.L".format(  str(rZ).zfill(3), r3.zfill(3)  )
    web = "https://tendl.web.psi.ch/tendl_2021/"

    url=f"{web}{p1}_html/{t2.capitalize()}/{p1.capitalize()}{t.capitalize()}residual.html"
    #print("I...",url)

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data.decode('utf-8'), "lxml")
    links = [item['href'] if item.get('href') is not None else item['src'] for item in soup.select('[href^="http"], [src^="http"]') ]
    #print(links)

    possible_extensions = []

    for l in links:
        #if (l.find(rname)>=0) and (l[-4:]!=".ave") and (l[-4:]!=".L00"):
        if (l.find(rname)>=0):
            extension = l[-3:]
            print(f"L... {fg.magenta} {l} {fg.default}" )
            possible_extensions.append(l)

    if len(possible_extensions)>0:
        print(f"o... {fg.white} THERE ARE {len(possible_extensions)} POSSIBLE levels{fg.default}")
        return possible_extensions
    return None


# ===========================================================================
# ===========================================================================
# ===========================================================================

# =====================================================================

def get_tendl( proj, targ, product,  plot=False , kind="linear" , xsset="tot" , Emax = 50 , logy=True):
    """
    returns dataset and LABEL
    """
    url="https://tendl.web.psi.ch/tendl_2021/proton_html/Mg/ProtonMg26residual.html"

    p1,t,t2,t3,tzero,r2,r3,rZ,tZ,LABEL,extension =  prep_tendl( proj, targ, product, xsset="tot" )


    # I know LABEL here.... May be I have the file already:
    LOCALFILENAME = f"{get_data_path()}/{LABEL}.csv"
    LOCALFILE = False
    if os.path.exists( LOCALFILENAME ):
        LOCALFILE = True

    #LOCALFILE = False # !!!!!!!!!!!!!!!!!! I HAVE SOM CATCH IN EThresh
    if LOCALFILE:
        # at the end I need a list of 2 numpy arrays [ [e],[v] ]
        print(f"i... {fg.green} LOCAL! ...{LOCALFILENAME} {fg.default}")
        # # this evidently gets energies
        # tote = np.array([])
        # tcks = np.genfromtxt( f"{LOCALFILENAME}" , delimiter=',')
        # # rest taken from comb...
        # enes = np.transpose(tcks)[0]
        # tote = np.append( tote, enes )
        # tote = np.unique( sorted(tote) )
        df = pd.read_csv( LOCALFILENAME , names = [ 'e', LOCALFILENAME ] , header = None)
        #df.save csv in current FOLDER
        df[ ['e',LOCALFILENAME] ].to_csv( f"{LABEL}.csv" ,index=False, header = False)
        #print(df)
        tcks = [ df['e'], df[LOCALFILENAME] ]
    else:
        print("      _________________  ")
        print(f"i... {proj} x {targ} (Z={tZ}) -> {product}  (Z={rZ})")


        web = "https://tendl.web.psi.ch/tendl_2021/"
        tableurl = f"{web}{p1}_html/{p1}.html"
        #print(f"i... {tableurl}")
        isourl = f"{web}{p1}_html/{t2.capitalize()}/{p1.capitalize()}{t2.capitalize()}.html"
        #print(f"i... {isourl}")
        resurl = f"{web}{p1}_html/{t2.capitalize()}/{p1.capitalize()}{t2.capitalize()}{t3}residual.html"
        print(f"i... {resurl}")

        rname = "rp{}{}.{}".format(  str(rZ).zfill(3), r3.zfill(3) , extension )

        url="https://tendl.web.psi.ch/tendl_2021/{}_file/{}/{}/tables/residual/{}".format( p1 , t2, tzero , rname )
        #print("y...",url)


        http = urllib3.PoolManager()
        response = http.request('GET', url)
        print("Y...",url)
        soup = BeautifulSoup(response.data.decode('utf-8'), "lxml")
        tab= soup.get_text().strip().split("\n")
        #print(tab)
        if "".join(tab).find("404 Not Found")>=0:
            print(f"{bg.red}X... {LABEL} TENDL: reaction {rname} NOT FOUND in  TENDL ; {bg.default}" )
            sys.exit(1)#quit()
            return None, LABEL


        # for *.tot there are "E-threshold"
        Ethrs = [ i for i in tab if i.find("E-threshold")>0 ]
        if len(Ethrs)==0:
            Ethrs = 0
        else:
            Ethrs = Ethrs[0].split("=")[1].strip()
            Ethrs = float( '%.2f'%(float(Ethrs)) )
        if Ethrs >= Emax:
            print(f"{fg.yellow}X... {LABEL} Ethreshold too high = {Ethrs}{fg.default}")
            return None, LABEL

        tab=[x for x in tab if x.find("#")<0]
        #print(tab)
        #r=[x.extract() for x in soup.findAll('p')]
        #print(r[0])
        excit={}
        Elowest = 200
        for t in tab:
            # print(t.split())
            # ------ I kill all bellow some XS
            if float(t.split()[1])>1e-7:
                excit[ float(t.split()[0]) ] = float(t.split()[1])
                if Elowest > float(t.split()[0]):
                    Elowest = float(t.split()[0])
        if Elowest >= Emax:
            print(f"{fg.cyan}X... {LABEL} Elowest too high = {Elowest}{fg.default}" )
            return None, LABEL

        x= np.asarray( list(excit.keys()) ,   dtype=np.float32)
        y= np.asarray( list(excit.values()) , dtype=np.float32)



        # INTERP1D : gives the object with .x  .y and info howto manage
        #tcks = interpolate.interp1d( x, y ,kind="linear" )  #  FUNCTION
        #tcks = interpolate.interp1d( x, y ,kind="cubic" )  #  FUNCTION

        tcks = interpolate.interp1d( x, y ,kind=kind )  #  FUNCTION
        tcks = [x,y]
        print(tcks) # [array([  2.,   3. ...., 200.], dtype=float32), array([2.15 ...71e-02, 5.57971e-02], dtype=float32)]

        # --------------------------- save / use transpose for that
        np.savetxt(f"{LABEL}.csv",
               np.transpose(tcks),
               delimiter =", ",
               fmt ='% s')

        get_data_path()
        np.savetxt(f"{get_data_path()}/{LABEL}.csv",
                   np.transpose(tcks),
                   delimiter =", ",
                   fmt ='% s')

        print(f" ... saved csv: {fg.white}  {LABEL}.csv {fg.default}")
    # FILE EXISTED LOCALY ____end________________________________

    #
    #  SPLREP - it creates   TUPLE OF ARRAYS and needs SPLEV to DRAW
    # SPLREP find hte BSPLINE,  SPLEV evaluates from knots and repres.
    #tcks2 = interpolate.splrep( x, y, s=0 )  # SPLINE FUNCTION
        #print(tcks2)
    #
    if plot:
        plot_spline( [tcks] , label="Exc.Fun." , logy=logy)

    if not LOCALFILE:
        print(f"{fg.green}+... reaction: {LABEL} ... threshold/lowest: {Ethrs}/{Elowest} MeV    data length: {len(tcks[0])} {fg.default}" )
    return [tcks, LABEL ]  # interpolated function

# ----------------------------------------------- get_tendl  - returns dataset,label




# =================# ===========================================================================
# ===========================================================================
# ===========================================================================


# ----------------------------------------------------------- PLOT A Z : main function

# def plot_a_z( proj='h1', targ='fe56', prod_a=[53,57], prod_z=[26,28], exclude_stable = False):
def plot_a_z( proj=None, targ = None, aprod=[53,57], zprod=[26,28], Emax = 50, exclude_stable = False, logy=True):
    """
    PLOT TENDL data AZ - projectile, target, a,z (tuples)
    """
    print(f"{bg.white}_____________________________________________________________________{bg.default}")

    if proj is None or targ is None:
        print("i... Provide proj and targ parameters:   -p h1 -t fe56 ")
        print("""
e.g.
./tendl.py az -p h1 -t gd155 -a 156,157 -z 65,66
./tendl.py az -p h1 -t gd156 -a 156,157 -z 65,66
./tendl.py az -p h1 -t gd157 -a 156,157 -z 65,66
./tendl.py az -p h1 -t gd158 -a 156,157 -z 65,66
./tendl.py az -p h1 -t gd160 -a 156,157 -z 65,66
OR
grp  group the csv files
OR
comb  combine csv files based on nat abundances OR -x rat_ios
""")
        sys.exit(1)

    if aprod is None or zprod is None:
        print(" ... USE TUPLE for ranges  the 'last +1' ")
        print("Parameters:   -p h1 -t fe56 -a 54,57 -z 26,28 ")
        sys.exit(1)
    elif type(aprod) is not tuple or type(zprod) is not tuple:
        print("Parameters:   -a -z should be tuples  ")
        if type(aprod) is not tuple: aprod = [aprod]
        if type(zprod) is not tuple: zprod = [zprod]
        #if type(zprod) is not tuple: zprod = (zprod,)

    if type(aprod) is tuple:       aprod = list(aprod)
    if type(zprod) is  tuple:      zprod = list(zprod)

    print("i... a and z :", type(aprod), type(zprod) )
    print("i... a and z :", aprod, zprod )
    #print("i... a and z :", range(*aprod), range(*zprod) )
    #sys.exit(1)


    if type(targ) is tuple:
        print("i...  TARGET TUPLE :  IT MUST BE A COMPLETE LIST")
        for ttt in targ:
            print(f"{bg.cyan} -----------------------------> {ttt}{bg.default}")
            plot_a_z( proj, ttt, aprod, zprod, exclude_stable )
        sys.exit(1)


    curves=[]

    #  fe={54:5.8, 56:91.7, 57:2.12, 58:0.28 }

    plt.switch_backend('Agg')
    plt.ioff()

    # I will force it to plot a single function (+isomers) per png... it waas a mess

    for a in aprod:# range( *aprod ):
        print(f"{fg.black}{bg.yellow}________________________________  A={a}      {fg.default}{bg.default}")


        for z in zprod:#range( *zprod ):

            fig,ax = plt.subplots()
            curves = []

            print(f"{fg.white}________________________________  {fg.yellow}A={a}  Z={z}  {fg.default}")
            #print("_"*30, "A=",a, "Z=",z)
            final_or = elements[z]+str(a) # this is for TENDL


            # if exclude_stable:
            #     # exclude stable isotopes:
            #     radio = True
            #     for i in stable_isotopes[ elements[z] ]:  # will also give 14C etc...
            #         if i == a:
            #             radio = False # IS STABLE

            #     if not radio:
            #         print("X  {} .... STABLE .... ".format(final_or) )
            #         continue

            final=final_or  # tot
            print(f" ... {fg.green} getting {bg.green}{fg.white} TENDL's res{bg.default}{fg.green}  ... product = {final} {fg.default}")
            res = get_tendl( proj,targ, final  , Emax = Emax, kind="cubic" )
            curves.append( res )

            # EXISTS
            if res[0] is not None:
                print(f" ... {fg.green} getting {bg.green}{fg.white} TENDL {bg.default}{fg.green}  ... product = {final} {fg.default}")
                res = get_tendl_levels(  proj,targ, final)
                if res is not None:
                    for i in res:
                        lev = i.strip(".ave")
                        lev = "_"+lev[-2:]    #_00  _01 _10
                        print( "    ",lev)
                        print(f" ... {fg.green} getting TENDL  ... product = {final+lev} {fg.default}")
                        res = get_tendl( proj,targ, final+lev  , Emax = Emax, kind="cubic" )
                        curves.append( res ) #collect isome+ground


        # I will force it to plot a single function (+isomers) per png ... unmess

            LABEL2 = f"exc_TENDL21_{targ}({proj},x){final}" # +str(a)
            print("_"*30, f"{bg.blue} plotting - clearing {LABEL2} {bg.default}")
            plot_spline( ax, curves , Emax = Emax, clear = True, logy=logy)
            plt.savefig("i_"+LABEL2+".png")
            plt.cla()
            plt.clf()
            plt.close(fig)




# ===========================================================================
# ===========================================================================
# ===========================================================================
def group_csv(*filenames, Emax = 50, logy=True):
    """
    it 'only' plots the csv files  together as they are, no abundances involved
    """
    print(f"{bg.white}_________________________________________________________{bg.default}")

    print(filenames)
    if len(filenames)==0: return

    # get isotopes , taken from comb
    isots = [ x.split("_")[1].split("(")[0]  for x in filenames ]

    # guess the residue - taken from comb
    resi = set([ x.split(".csv")[0].split(")")[-1]  for x in filenames ])
    resi = list(resi)
    if len(resi)>1:
        print( "X... PROBLEM WITH common RESIDUE ",len(resi) )
    resi = resi[0]


    plt.switch_backend('Agg')
    plt.ioff()
    fig,ax = plt.subplots()
    curves = []

    for file1 in filenames:
        print(file1)
        data = pd.read_csv(file1,header=None)
        #print(data[0])
        #plt.plot(data.iloc[:,0], data.iloc[:,1])
        a = [ data.iloc[:,0], data.iloc[:,1]  ]
        LABEL2 = file1
        curves.append( [a,LABEL2] )
        #print("OK", file1)

    plot_spline( ax, curves , Emax = Emax, clear = True, logy=logy)

    plt.xlabel('Energy')
    plt.ylabel('mb')

    FNAME = f"i_grp_{'_'.join(isots)}_to_{resi}.png"
    print(f" ... saving {fg.yellow} {FNAME} {fg.default}")
    print("_"*30, f"{bg.blue} plotting - clearing {LABEL2} {bg.default}")
    plt.savefig(FNAME)

    plt.cla()
    plt.clf()
    plt.close(fig)

    #plt.show()

# ===========================================================================

def combine_tendl_csv( *args, xabundances = None, Emax = 50, logy=True):
    """
    read csv files, create either natural OR defined (-x for =percentual= abundances)  combination. Result in nat_...rat_ PNGs
    """
    print(f"{bg.white}_________________________________________________________{bg.default}")
    print(args)
    if len(args)==0: return

    # get isotopes
    isots = [ x.split("_")[1].split("(")[0]  for x in args ]
    print(" TYPICAL USAGE IS TO COMBINE ALL (target) ISOTOPE'S XS : ")
    print( "i... combining targets", isots )

    # guess the residue
    resi = set([ x.split(".csv")[0].split(")")[-1]  for x in args ])
    resi = list(resi)
    if len(resi)>1:
        print( "X... PROBLEM WITH common RESIDUE ",len(resi) )
    resi = resi[0]

    # ---------------------------- construct global index for energies
    tote = np.array([])
    # get energy grid
    for fname in args:
        print(f"i... {fg.green} reading  {fname} {fg.default}")
        a = None
        try:
            a = np.genfromtxt( fname , delimiter=',')
        except:
            print(f"X... {bg.red} FILE NOT FOUND {fname} {bg.default}")
            sys.exit(1)
        enes = np.transpose(a)[0]
        tote = np.append( tote, enes )
        #print( enes )
    tote = np.unique( sorted(tote) )
    # Emax = tote.max()
    print(" ... Energies:",tote)

    # ------------------ create initial dataframe ---------
    dfmain = pd.DataFrame( 1000*tote , columns=["e"])
    dfmain["e"] = dfmain["e"].astype( int )
    dfmain['pkeep'] = dfmain['e']
    dfmain = dfmain.set_index(['e'])
    # print(dfmain)

    #return
    i = -1
    for fname in args:
        i+=1
        print(f"i... {fg.cyan}reading  {fname}  {isots[i]} {fg.default}" )
        #a = np.genfromtxt( fname , delimiter=',')
        df = pd.read_csv( fname , header = None)
        df.columns = ["e",  isots[i] ]
        df["e"] = df["e"]*1000 # df.apply( lambda x: int(df['e']*1000) ) #
        df["e"] = df["e"].astype( int )
        df = df.set_index( ["e"] )
        print("i... data lenght", len(df))
        #print(df)

        # merging on
        dfmain = pd.merge(dfmain, df, how="left", left_index = True, right_index = True )

        #print(dfmain)
        #return
        #dfmain.append(df)
    #dfmain = dfmain.set_index(["e"])
    dfmain = dfmain.drop(["pkeep"], axis=1)
    dfmain = dfmain.dropna( how = "all") # where all are nan
    dfmain = dfmain.fillna(0)



    XAB = False
    if xabundances is None:
        print("i... using standard abundances")
    else:
        if type(xabundances) is float or type(xabundances) is int:
            xabundances = [ xabundances ]
        print(f"i... {fg.black}{bg.orange} Override for abundances {fg.default}{bg.default}")
        print("i...  test len", len(dfmain.columns) ,"==", len(xabundances) )
        xabundances  = list(xabundances)
        if len(dfmain.columns) != len(xabundances):
            sys.exit(1)
        XAB = True
        xabundances.append( 0 )
    # ---------------------sum-------------------

    # start plotting here
    plt.switch_backend('Agg')
    plt.ioff()
    fig,ax = plt.subplots()

    curves = []
    dfmain["sum"] = 0 # dfmain.sum(axis=1)
    dfmain['e'] = dfmain.index/1000

    for ic in sorted(dfmain.columns):
        if ic == 'e': continue
        if ic == 'sum': continue
        icca = ic.capitalize()
        abu = 0
        if XAB:
            abu = xabundances.pop(0)/100
        else:
            if icca in  abundances:
                abu =  abundances[icca]/100
        print( f" ... {fg.orange} summing with abbundances: {ic:5s},  Isotope {icca:5s} ... {round(100*abu,3):7.3f} %  {fg.default}")

        # I add the individual curves too
        #a = np.genfromtxt( outname  , delimiter=',' )
        #a = np.transpose(a)
        LABEL_ISO = f"{icca:5s} {round(100*abu,2):7.2f} %"
        # print(dfmain)   e was index earlier, isotopes are there
        a = [dfmain['e'] ,dfmain[ic]*abu]
        #print(a)
        curves.append( [a,LABEL_ISO] )

        dfmain["sum"] = dfmain["sum"] + dfmain[ic]*abu
    # ---------------------sum-------------------



    print(f" ... {fg.cyan} joined as numpy array ...  {fg.default}")

    print(f"{fg.white}______________________________________________{fg.default}")
    print(dfmain.head(4))
    print(dfmain.tail(4))
    print(f"{fg.white}______________________________________________{fg.default}")

    if XAB:
        outname_nocsv = f"rat_{'_'.join(isots)}_to_{resi}"
    else:
        outname_nocsv = f"nat_{'_'.join(isots)}_to_{resi}"


    print(f" ... saving joined  ... {fg.yellow}  {outname_nocsv}.csv {fg.default}")
    dfmain[ ['e','sum']].to_csv( outname_nocsv+".csv" ,index=False, header = False)

    a = None
    try:
        a = np.genfromtxt( outname_nocsv+".csv"  , delimiter=',' )
    except:
        print(f"X... {bg.red} FILE NOT FOUND {fname} {bg.default}")
        sys.exit(1)
    a = np.transpose(a)
    #print(a) #
    print(f" ... {fg.white}  ... and plotting {fg.default}")
    LABEL2 = outname_nocsv

    # Curves [] or already prepended?
    curves.append( [a,LABEL2] )


    plot_spline( ax, curves , Emax = Emax, clear = True,logy=logy)
    print(f" ... ... {fg.yellow} {LABEL2}.png  {fg.default}")
    print("_"*30, f"{bg.blue} plotting - clearing {LABEL2} {bg.default}")
    plt.savefig("i_"+LABEL2+".png")

    if XAB: print(f" ... {fg.black}{bg.orange} -x abundances must be in (Z) sorted order!!! Checkit !!!!!!  {fg.default}{bg.default}")
    plt.cla()
    plt.clf()
    plt.close(fig)

    return













# ===========================================================================
# ===========================================================================
# ===========================================================================


if __name__ == "__main__":
    #print("D... only az works now..... if you tune")
    Fire( {"az":plot_a_z,
           "comb":combine_tendl_csv,
           "grp":group_csv,
           "ps":plot_spline} )
    #ifun1=get_tendl( "h1", "mg26", "al26"  , kind="cubic" )
    #ifun2=get_tendl( "h1", "mg26", "al26g"  ,kind="cubic")
    #ifun3=get_tendl( "h1", "mg26", "al26m"  ,kind="cubic")
