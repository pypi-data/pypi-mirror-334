#!/usr/bin/env python3


import sys # print stderr

from fire import Fire
from nuphy2.version import __version__

_DEBUG=0
from math import sin,cos,tan,pi,sqrt,asin,atan

from nuphy2.prj_utils import fail
from nuphy2.prj_utils import Bcolors
from nuphy2.prj_utils import super_print

import nuphy2.isotope as isotope
# import nuphy2.rolfs as rolfs # Coul barrier here

#-------------------- from nuphy---------------------
import os
import tempfile   # create tempdir
import shutil     # rm tempdir, copytree NOT GOOD ENOUGH
import glob, os   # find file in directory
from distutils.dir_util import copy_tree  # copytree
import subprocess
from contextlib import contextmanager       # for CD with context
from xvfbwrapper import Xvfb  # invisible RUN
import math # isnan()

from nuphy2.isotope import gaseous,densities,elements,molarweights
# # import nuphy2.isotope as isotope
import nuphy2.compounds as srcomp

import threading
import time

################################  SR
# i need interpolation now.... #
#https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np


import scipy.integrate as integrate

import pandas as pd

import re

T_STP = 273.15
T_NTP = 293.15
# ---------------- global definition
P_BASE = 101_325
T_BASE = T_NTP

TRIMAUTO="""1

TRIMAUTO allows the running of TRIM in batch mode (without any keyboard inputs).
This feature is controlled by the number in line #1 (above).
  0 = Normal TRIM - New Calculation based on TRIM.IN made by setup program.
  1 = Auto TRIM - TRIM based on TRIM.IN. No inputs required. Terminates after all ions.
  2 = RESUME - Resume old TRIM calculation based on files: SRIM Restore\*.SAV.

  Line #2 of this file is the Directory of Resumed data, e.g. A:\TRIM2\
  If empty, the default is the ''SRIM\SRIM Restore'' directory.

See the file TRIMAUTO.TXT for more details.
""";







#---------------------------------------------------------------------------STARTT OF SR




OUTPUTFILE="output"

#
# stopping units  eV/ ( 1E15 atoms/cm2 )   : 7
#

MANUAL_SR_IN="""---Stopping/Range Input Data (Number-format: Period = Decimal Point)
---Output File Name
"OOOUTPUTFILE"
---Ion(Z), Ion Mass(u)
1   1.008
---Target Data: (Solid=0,Gas=1), Density(g/cm3), Compound Corr.
0    1.0597    .9457121
---Number of Target Elements
 3
---Target Elements: (Z), Target name, Stoich, Target Mass(u)
1   "Hydrogen"               8             1.008
6   "Carbon"                 3             12.011
8   "Oxygen"                 2             15.999
---Output Stopping Units (1-8)
 7
---Ion Energy : E-Min(keV), E-Max(keV)
 10    10000
""";


MANUAL_SR_IN="""---Stopping/Range Input Data (Number-format: Period = Decimal Point)
---Output File Name
"OOOUTPUTFILE"
---Ion(Z), Ion Mass(u)
1   1.008
---Target Data: (Solid=0,Gas=1), Density(g/cm3), Compound Corr.
0    2.253    1
---Number of Target Elements
 1
---Target Elements: (Z), Target name, Stoich, Target Mass(u)
6   "Carbon"                 1             12.011
---Output Stopping Units (1-8)
 7
---Ion Energy : E-Min(keV), E-Max(keV)
 100    20000
""";

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    dirname=os.path.dirname( newdir )

    os.chdir(os.path.expanduser( dirname ))
    #print('i... from',prevdir,'entering',dirname )
    try:
        yield
    finally:
        #print('i... cd back to ',prevdir)
        os.chdir(prevdir)





def load_SR_file( SRFile ):
    """
    reads the file
    returns DICT with losses at certain energies
    """
    units_ok=False
    kevum=0.0
    mevmg=0.0  # MeV/mg/cm2
    print("D... opening SRFile", SRFile)
    with open( SRFile ) as f:
        li=f.readlines()


    li=[x.rstrip() for x in li] # remove \n
    #print("\n".join(li))

    begin,end=0,len(li)
    for i in range(len(li)):
        if (li[i].find("Energy")>=0) and  (li[i].find("Nuclear")>=0):
            begin=i+2
        if  (li[i].find("Multiply")>=0) and  (li[i].find("Stopping")>=0):
            end=i-1
        if  (li[i].find("eV/(1E15 atoms/cm2)")>=0) and  (li[i].find("1.0000E+00")>=0):
            units_ok=True
        if  (li[i].find("keV/micron")>=0):
            kevum=float( li[i].strip().split()[0] )
            print( ".... kevum=",kevum)
        if  (li[i].find("MeV/(mg/cm2)")>=0):
            mevmg=float( li[i].strip().split()[0] )
            print( ".... mevmg=",mevmg)
    if not units_ok:
        print("X... I am afraid the unit is not 7 / eV/(1E15 atoms/cm2).QUIT")
        quit()
    li=li[begin:end]
    #print(  li  )
    eneloss={}
    factor=1 ######000000  # eV => MeV
    for i in li:
        a=i.strip().split()
        ene=float(a[0])
        loss=float(a[2]) + float(a[3])
        #print(".... .... ", loss,float(a[2]) , float(a[3]) )
        #all in eV
        if a[1]=="keV":
            #ene=ene*1000.
            ene=ene/1000.
        if a[1]=="MeV":
            #ene=ene*1000000.
            ene=ene
        # change units for some reason
        eneloss[ ene ] =loss /factor # eV  => MeV/ (10^15/cm2)
    ###kevum=kevum*factor
    return eneloss,kevum,mevmg






def run_sr_exe( SRINFILE=MANUAL_SR_IN,  silent=True):
    """
    returns DICT  eneloss
    """
    RPATH=CheckSrimFiles()
    if not silent:print( "DDD...    SR.IN:",RPATH ," xxx")

    ############## CREATE TEMP #####################
    temppath = tempfile.mkdtemp(prefix='sr_')+'/'
    if not silent: print('DDD... SR.IN ... copying from',RPATH,'to',temppath)
    copy_tree( RPATH , temppath )
    print("D...  copied", temppath)
    with cd(temppath+'SR Module/'):
        if not silent:print("DDD... cd "+temppath+'SR\\ Module/')
        #srin=MANUAL_SR_IN.replace("OOOUTPUTFILE", OUTPUTFILE)+"\n"
        srin=SRINFILE.replace("OOOUTPUTFILE", OUTPUTFILE)+"\n"
        if srin.find("\r\n")<0:
            srin=srin.replace('\n','\r\n') # DOS
        with open("SR.IN","w") as f:
            f.write(srin)
        CMD="wine SRModule.exe"
        if not silent:print("DDD... ",CMD)
        if silent:
            print("############### VDISPLAY #########################start")
            vdisplay = Xvfb(width=1280, height=740, colordepth=16)
            vdisplay.start()

        process = subprocess.Popen(CMD.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        output, error = process.communicate()

        if silent:
            vdisplay.stop() #
            #print()
            print("\n############### VDISPLAY #########################stop")

        if not silent:print("DDD...  reading losses of SR.IN from ouput")
        #print("D... loading SR OUTPUTFILE",OUTPUTFILE)
        eneloss,kevum,mevmg=load_SR_file( OUTPUTFILE )
        #print("D... loaded")

        #print("losses and keV/um coef read")
    #print( "output==",eneloss )
    return eneloss,kevum,mevmg  # DICT WITH LOSSES





def srinterpolate( eneloss , plot=False):
    """
    get DICT of losses, create numpy arrays with interpolations
    return spline function
    that can be used like

    resu=interpolate.splev(x, splinefunction , der=0)
    print( "dE/dx value at 1.0MeV" , get_tcks(1.0)  )

    """
    x= np.asarray( list(eneloss.keys()) ,  dtype=np.float32)
    y= np.asarray( list(eneloss.values()) , dtype=np.float32)

    #tcks = interpolate.interp1d(x, y, kind="linear")  # simple linear picture #
    tcks = interpolate.interp1d(x, y, kind="cubic")  # simple linear picture #
    #
    #====== I DONT CARE ABOUT B-SPLINES==========FROM NOW
    # #print( "INTERPOLATED",tck )
    # # splines:
    # tcks = interpolate.splrep( x, y, s=0)  # SPLINE FUNCTION


    # ### plotting =======================
    # # 10e5 is enough to have smooth plot, but the function is important
    # xnew = np.linspace(x[0], x[-1], num=100000 , endpoint=True )
    # ynew = interpolate.splev(xnew, tcks, der=0)
    #plt.plot( x,y , '.', xnew, tck(xnew) ,'-')
    #plt.plot( x,y , '.', xnew, ynew ,'-' )

    if plot:
        Emin=min(tcks.x) # MeV
        Emax=max(tcks.x) # MeV
        unew = np.arange( Emin, Emax, 0.0001)
        out=tcks(unew)
        plt.plot(  x,y,'.',  label="losses")
        plt.plot( unew, out ,'-' , label="intep1d")
        plt.legend(  )
        plt.show()

    return tcks  # return spline function


#=====it was for b-splines not interp1d
# def get_interpolated_loss(x, tcks):
#     """
#     # stopping units  eV/ ( 1E15 atoms/cm2 )
#     """
#     resu=interpolate.splev(x, tcks, der=0)
#     return resu

# def get_interpolated_loss_inverse(x, tcks): # get splined values for X #
#     """
#     # stopping units  eV/ ( 1E15 atoms/cm2 )
#     - 1/S(E)  .... for integration
#     """
#     resu=-1.0*1E+15  / interpolate.splev(x, tcks, der=0)
#     return resu




def get_sr_loss( SRIN , Emax=5.8, dmax=10 , unit="um", silent=True):
    if SRIN=="":
        print("X...       SR.IN was not created, get_sr_loss() returns")
        return
    print("\ni... --------running---- SR.EXE LOSS: Eini={}  t={:.3f} {}".format(Emax, dmax, unit) )
    #
    eneloss,kevum,mevmg=run_sr_exe( SRIN, silent=silent)  # This returns loss tables BUT ALSO COEF!
    eneloss2=eneloss
    if unit=="um":
        for k in eneloss.keys():
            eneloss2[k]=eneloss[k]* kevum * 0.001
            #print(  "       --> ",eneloss[k] )
    if unit=="mg":
        for k in eneloss.keys():
            eneloss2[k]=eneloss[k]* mevmg
    if unit=="ug":
        for k in eneloss.keys():
            eneloss2[k]=eneloss[k]* mevmg/1000
            #print(  "       --> ",eneloss[k] )
    #print("i...   SR.IN coef:  keV/um",kevum)  # keV/um for loss simulation
    #print("i...   SR.IN coef:  MeV/mg/cm2",mevmg)  #  for loss simulation

    tcks=srinterpolate( eneloss2 , plot=False)
    #============== integration
#    Emax=5.8
#    dmax=10.0 # um
    e=Emax
    dx=0.01  # 0.7um also gives good result to 4,5 digits
    dx=dmax/500
    x=0
    xs,es=0,Emax # added later
    while (x<dmax) and (e>0):
        xs,es=x,e
        if e>min(tcks.x):
            #e=e-0.001* tcks( e )*dx  # ticks[keV/um] => Emax[MeV]
            e=e- tcks( e )*dx  # ticks[MeV/um] => Emax[MeV]
        else:
            #e=e-0.001* tcks( min(tcks.x) )*dx  # ticks[keV/um] => Emax[MeV]
            e=e- tcks( min(tcks.x) )*dx  # ticks[MeV/um] => Emax[MeV]
        x=x+dx
        #print(x, e)
    print("i... interpol: last two (x,e): {:.1f} {:.3f}   {:.1f} {:.3f}".format(x,e,xs,es) )
    dde=(dmax-xs)*(es-e)/(xs-x)
    if  es+dde < 0:
        print("_"*30,"\n\nE_SRIN = {:.5g}\n".format( 0 ) ,"_"*30 )
    else:
        print("_"*30,"\n\nE_SRIN = {:.5g}\n".format( es+dde ) ,"_"*30 )
        # stopping units  eV/ ( 1E15 atoms/cm2 )   : 7  #== this may work for yield







#--------------------------------------------------------------------------- END OF SR







#--- is ipython....
def is_interactive():
    import __main__ as main
    return not hasattr(main, '__file__')

def isjupyter():
    #print('D... checking JUPYTER')
#def in_ipynb():
#    try:
#        cfg = get_ipython().config
#        if cfg['IPKernelApp']['parent_appname'] == 'ipython-notebook':
#            return True
#        else:
#            return False
#    except NameError:
#        return False
    '''
    isjupyter recognizes if run from Jupyter / IPython
    '''
    try:
        __IPYTHON__
        return True
    except:
        return False

###################################
#  this part should return to CUR DIR
#   after the context ends...
####################################
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    dirname=os.path.dirname( newdir )

    os.chdir(os.path.expanduser( dirname ))
    #print('i... from',prevdir,'entering',dirname )
    try:
        yield
    finally:
        #print('i... cd back to ',prevdir)
        os.chdir(prevdir)





def CheckSrimFiles():
    '''
    I want to find installation of SRIM that i can copy to tmp
    '''

    helpsrim="""
====== SRIM Installation help: ========================================
    apt install wine

    SRIM 2013 can be downloaded from  http://www.srim.org/SRIM/SRIM-2013-Pro.e
    or better get a smaller version for multiple running copies http://www.srim.org/SRIM/SRIM-2013-Std.e

    #======= run this to install SRIM =========== BEGIN
    cd /tmp
    wine notepad # may help to initialize ~/.wine/drive_c/...
    cd ~/.wine/drive_c/Program\ Files/
    mkdir SRIM
    cd SRIM
    wget http://www.srim.org/SRIM/SRIM-2013-Pro.e
    wine SRIM-2013-Pro.e
    # all should be correctly extracted
    wine SRIM.exe
    #======= run this to install SRIM =========== END

    # Here an error probably appear: import_dll Library MSVBVM50.DLL not found
    # Following libraries are missing in ~/.wine/drive_c/windows/
    #       152848  COMDLG32.OCX
    #       244416  msflxgrd.ocx
    #      1347344  MSVBVM50.DLL
    #       212240  RICHTX32.OCX
    #       224016  TABCTL32.OCX
    #
    #  and later  617896  comctl32.ocx
    #
    # If you find the file libs2013.tgz - try:
    # find ~/.local/lib -iname "libs*.tgz"

    # ====== enter the dir with libs and run ======BEGIN
    cp  libs2013.tgz ~/.wine/drive_c/windows/system
    cd ~/.wine/drive_c/windows/system
    tar -xvzf libs2013.tgz
    cd ~/.wine/drive_c/Program\ Files/SRIM/
    wine SRIM.exe
    # ===============================================END

    # There can happen that locale produces numbers with decimal ",".
    # Check it with
    wine regedit
    # see MyComputer/HKEY_CURRENT_USER/ControlPanel/International/sDecimal
    # you may need to completely delete all your ~/.wine
    # change locale to en_US.utf8 (or en_GB) and start 'wine notepad'
    """
    home = os.path.expanduser("~")
    paths=[home]
    paths.append(home+'/srim/')
    paths.append(home+'/bin/srim/')
    paths.append(home+'/.wine/drive_c/Program Files/SRIM/')
    paths.append(home+'/.wine/drive_c/Program Files (x86)/SRIM/')
    # installation of NuPhyPy-------------
    MyPath= os.path.abspath(__file__)
    paths.append( os.path.dirname(MyPath)+'/srim_binary/rundir/'  )
    #
    #
    #
    #    print('i... checking PATH',  paths)
    RPATH=None
    for path in paths:
        if os.path.exists(path):
            #print('i... checking path ', path )
            for file in os.listdir( path ):
                if file=='TRIM.exe':
                    RPATH=path
                    # print('+...  found SRIM.exe in ',path)
    if RPATH is None:
        print("X... srim not found in ",paths)
        print(helpsrim)
        fail("X... install SRIM first")
        CMD =  "sriminst.sh"
        output = subprocess.check_output(CMD,
                   stderr=subprocess.DEVNULL)

    return RPATH






def PrepSrimFile( **kwargs ):
    '''
    thickness in  mg/cm2 from NOW
    '''
    SRLINE=[]
    OT=   proj( kwargs['ion'],kwargs['energy'],kwargs['angle'],kwargs['number'] , SRLINE)
    OT=OT+targ( kwargs['mater'],kwargs['thick'],kwargs['ion'],kwargs['dens'] ,    SRLINE)
    #print( SRLINE )
    if SRLINE!=[]:
        SRLINEOUTPUT= "\r\n".join(SRLINE)
        with open("/tmp/SR.IN","w") as f:
            f.write(  SRLINEOUTPUT+"\r\n" )
    else:
        SRLINEOUTPUT=""
    return OT,SRLINEOUTPUT



#------------------------------

def proj( ion, energy, angle, number ,    SRLINE):
    seed=765
    ####  Z, Amu,  Energy,  Angle,  Number, BraggCorr, AutoNum
    ####   Z, Amu, BragggCor   #########3
    pro={'h1'  :[ 1, 1.00782503,  1.0 ],   #0.9570329
         'h2'  :[ 1, 2.014101777, 1.0   ] ,
         'h3'  :[ 1, 3.01604928 , 1.0   ] ,
         'he3' :[ 2, 3.01602,     1.0   ] ,
         'he4' :[ 2, 4.00260325,  1.0   ] ,
         'be9' :[ 4, 9.012,       1.0   ] ,
         'be10':[ 4, 10.01353382, 1.0   ] ,
         'b8'  :[ 5, 8.02460723,  1.0   ] ,
         'b10' :[ 5, 10.01293699, 1.0   ] ,
         'b11' :[ 5, 11.00930541, 1.0   ] ,
         'c12' :[ 6, 12.000,      1.0   ] ,
         'c13' :[ 6, 13.00335484, 1.0   ] ,
         'c14' :[ 6, 14.00324199, 1.0   ] ,
         'o14' :[ 8, 14.0086,     1.0   ] ,
         'o16' :[ 8, 15.995,      1.0   ] ,
         'f19' :[ 9, 18.9984,     1.0   ] ,
         'ne20':[ 10, 19.992440,  1.0   ] }

    if ion.namesrim in pro:
        #print('?...',ion.namesrim, '... PROJECTILE ALREADY DEFINED',pro[ion.namesrim])
        print('    ',ion.namesrim, '... PROJECTILE ALREADY DEFINED',pro[ion.namesrim])
    else:
        print(ion.namesrim,'not defined, I am defining it now')
        pro[ion.namesrim]=[ ion.Z, ion. amu, 1.0 ]    ## Bragg Corr i set to 1.0/C+C,h1+c,he4+c,
        print(ion.namesrim, 'DEFINED',pro[ion.namesrim])

    pro[ion.namesrim].insert( 2, energy*1000. )
    pro[ion.namesrim].insert( 3, angle )
    pro[ion.namesrim].insert( 4, number )    # N
    pro[ion.namesrim].append(  number-1 )     # AUTOSAVENUMBER

#    print( 'ION:',ion, pro[ion] )
    line1=' '+'   '.join(map(str,pro[ion.namesrim]))
    li2=[1, seed, 0]
    line2=' '+'   '.join(map(str,li2))
#    print(line1,line2)

    template_proj1="Ion: Z1 ,  M1,  Energy (keV), Angle,Number,Bragg Corr,AutoSave Number."
    template_proj2="Cascades(1=No;2=Full;3=Sputt;4-5=Ions;6-7=Neutrons), Random Number Seed, Reminders"
    template_proj3="Diskfiles (0=no,1=yes): Ranges, Backscatt, Transmit, Sputtered, Collisions(1=Ion;2=Ion+Recoils), Special EXYZ.txt file"
    template_proj4="    1       0           1       0               0                               0"

    OUTTEXT=""
    OUTTEXT=OUTTEXT+'\r\n'
    OUTTEXT=OUTTEXT+template_proj1 +'\r\n'
    OUTTEXT=OUTTEXT+line1 +'\r\n'
    OUTTEXT=OUTTEXT+template_proj2 +'\r\n'
    OUTTEXT=OUTTEXT+line2 +'\r\n'
    OUTTEXT=OUTTEXT+template_proj3 +'\r\n'
    OUTTEXT=OUTTEXT+template_proj4 +'\r\n'


    #===================== SR.IN   must be unix \n, it is reverted later =======
    #SRLINE=[] # trick
    SRLINE.append("---Stopping/Range Input Data (Number-format: Period = Decimal Point)")
    SRLINE.append("---Output File Name")
    SRLINE.append('"OOOUTPUTFILE"')
    SRLINE.append("---Ion(Z), Ion Mass(u)")
    SRLINE.append("{}  {:.3f}".format( pro[ion.namesrim][0] , pro[ion.namesrim][1]  ) ) # Z,u
    #1   1.008)


    return OUTTEXT
#    print(OUTTEXT)
#    print('------- projectile done ------------')


#------------------------------


############################################
#def targ(  name, thick,   ion,  outerdens=0.0  , SRLINE ):
def targ(  name, thick,   ion,  outerdens  , SRLINE ):
    '''
    thickness in mg/cm2 from NOW
    ...
    This should hadle now:
    li li6 li7 ... c c12 c13 c14
    ELEMENTAL TARGETS - if dens==0 : density from tables
    ISOTOPIC TARGETS  - if dens==0 : density calculated from elemental/molar_mass
    ... gaseous elements H,He,NOFNe...Ra / isotopes=simply by Z
    COMPOUNDS -  ??????
    !!! check CORRECT VALUES FOR BragCorr, indiv Displac/Latti/Surf !!!
    '''

#   heatsubl      indivdisp  latdispl ======= The data from SRIM for elements are here:
    heatsubl=[
       .00,
       .00,
       .00,
      1.67,
      3.38,
      5.73,
      7.41,
          2.00,
          2.00,
          2.00,
          2.00,
      1.12,
      1.54,
      3.36,
      4.70,
      3.27,
      2.88,
          2.00,
          2.00,
       .93,
      1.83,
      3.49,
      4.89,
      5.33,
      4.12,
      2.98,
      4.34,
      4.43,
      4.46,
      3.52,
      1.35,
      2.82,
      3.88,
      1.26,
      2.14,
           2.00,
           2.00,
       .86,
      1.70,
      4.24,
      6.33,
      7.59,
      6.83,
            2.00, #Tc
      6.69,
      5.78,
      3.91,
      2.97,
      1.16,
      2.49,
      3.12,
      2.72,
      2.02,
           2.00, #I
           2.00, #Xe
       .81,
      1.84,
      4.42,
      4.23,
      3.71,
      3.28,
           2.00, #Pm
      2.16,
      1.85,
      3.57,
      3.81,
      2.89,
      3.05,
      3.05,
      2.52,
      1.74,
      4.29,
      6.31,
      8.10,
      8.68,
      8.09,
      8.13,
      6.90,
      5.86,
      3.80,
       .64,  # Hg
      1.88,
      2.03,
      2.17,
      1.50,
           2.00,  #At
           2.00, #Rn
           2.00,
           2.00, #Ra
           2.00, #AC
      5.93,
           2.00, #Pa
      5.42 ]


    indivdisp=[
        0 ,
        10     ,
        5   ,
        25    ,
        25    ,
        25   ,
        28   ,
        28    ,
        28   ,
        25    ,
        5    ,
        25    ,
        25    ,
        25    ,
        15    ,
        25    ,
        25     ,
        25    ,
        5  ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        15   ,
        25    ,
        25   ,
        25   ,
        5    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        25    ,
        5   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25    ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25  ,
        25   ,
        25  ,
        25   ,
        25   ,
        25   ,
        25   ,
        25   ,
        25  ,
        25  ,
        25  ,
        25  ,
        25  ,
        25  ,
        25  ,
        25  ,
        25  ,
        25  ,
        25  ,
        25   ,
        25   ,
        25 ,
        25  ,
        25  ,
        25 ,
        25,
        25
        ]


    lattdisp=[
        0,
        3    ,
        1  ,
        3   ,
        3   ,
        3  ,
        3  ,
        3   ,
        3  ,
        3   ,
        1   ,
        3   ,
        3   ,
        3   ,
        2   ,
        3   ,
        3    ,
        3   ,
        1 ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        2  ,
        3   ,
        3  ,
        3  ,
        1   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        3   ,
        1  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3   ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3 ,
        3  ,
        3 ,
        3  ,
        3  ,
        3  ,
        3  ,
        3  ,
        3 ,
        3 ,
        3 ,
        3 ,
        3 ,
        3 ,
        3 ,
        3 ,
        3 ,
        3 ,
        3 ,
        3  ,
        3  ,
        3,
        3 ,
        3 ,
        3,
        3,
        3
        ]
    ####  Z, Amu,  Energy,  Angle,  Number, BraggCorr, AutoNum
    ####   Z, Amu, BragggCompCorr, indivDispl,  indivLattice, indivSurf==heatSubl
    mat={} # I NEED FOR ELEMENT
#     mat={#'li'          :[ 3,    6.941,     1.0,     25,      3,    1.67  ],
#          ########   prvky +  stoich,   CompoundBragg       density
#          'mylar'  : [{ 'h': 0.363636 },{ 'c': 0.454545 },{ 'o': 0.181818 }, 0.9570329,  1.397 ],
#          'ch2'    : [{ 'h': 0.666667 },{ 'c': 0.333333 }, 0.9843957 , 0.93  ],
#          'cd2'    : [{ 'h': 0.666667 },{ 'h2': 0.333333 }, 0.9843957 , 1.062857 ],
#          'lif'    : [{ 'li': 0.5 },{ 'f': 0.5 }, 1.0 , 2.635 ],
#          'cd2'    : [{ 'h': 0.666667 },{ 'h2': 0.333333 }, 0.9843957 , 1.062857 ],
# #         'havar'  : [{ 'c': 0.666667 },{ 'cr': 0.333333 }, 0.9843957 , 1.062857 ],
#          'melamin': [{ 'c': 0.2 },{ 'h': 0.4 },{ 'n': 0.4 }, 1.0 , 1.574 ],
#          'air'    : [{ 'c': 0.000124 },{ 'o': 0.231781 },{ 'n': 0.755268 }, { 'ar': 0.012827 },1.0,0.00120484 ],

#     #     'ar':[ 10, 19.992440,  0.0   ]
#     }



    #########################################
    #  heatsubl   indi lat displacement  and other data defined/introduced up to this point
    #
    #  NOW - find material/element/isotope
    #  mat[name]  will contain  eZ,amu  1. i,la,heatsu
    #
    #    AGAIN THE SAME ????????????? I DID IT ALREADY !!!!!
    isgas=-1
    #      compounds == No .title()
    #print("DDD>...",name, srcomp.material_text.keys())
    if name in srcomp.material_text.keys():     ###########################
        #==========  predefined materials HERE ===================
        if name in srcomp.material_gas: isgas=1  # "only Air"
        print('+...',name, '... MAT IS KNOWN and defined in compounds')
        # THIS CAN HAPPEN ONLY FOR COMPOUNDS NOW....................
        # replace  "HHHHH into MMMMM  WWWWW    DDDDD"
        ##OUTTEXT=srcomp.material_text[ name.title() ]
        OUTLIST=srcomp.rebuild( name )  # no title() for compounds
        #for i in OUTLIST: print(i)
        OUTTEXT="\r\n".join( OUTLIST )
        OUTTEXT=OUTTEXT.replace("HHHHH",  ion.namesrim )
        OUTTEXT=OUTTEXT.replace("MMMMM", name )
        if outerdens<=0.0:
            dens=srcomp.get_density( name )  # no .title() for compounds
        else:
            dens=outerdens
        OUTTEXT=OUTTEXT.replace("DDDDD", str(dens) )
        OUTTEXT=OUTTEXT.replace('WWWWW', str( 1000*thick/dens/1e-2  ) )  # in Angstr

        #print(OUTTEXT)
        #quit()
        print("i...  compoud is returned, I cannt do SR.IN now")
        while len(SRLINE)>0:
            SRLINE.pop(0)###### I cannot create SR.IN for compounds now.....
        return OUTTEXT  #################################################### COMPOUND RETURN HERE
    else:
        #print('DDD...',name,'MAT NOT defined ... ')
        if name.title() in elements:
            #print('+...',name.title(),'ELEMENT detected ... ')
            eZ=elements.index(name.title())
            isgas=gaseous[ eZ ]
            heatsu= heatsubl[eZ]
            #if isgas==1: heatsu=0.0
            mat[name]=[ eZ,molarweights[eZ], 1., indivdisp[eZ], lattdisp[eZ], heatsu ]
        else:
            #print('+...',name,'Isotope detected ... ')
            isoto1=isotope.create( name )
            eZ=isoto1.Z
            isgas=gaseous[ eZ ]
            heatsu= heatsubl[eZ]
            #if isgas==1: heatsu=0.0
            mat[name]=[ eZ, isoto1.amu,  1., indivdisp[eZ], lattdisp[eZ],  heatsu ]

        #print('i...',name, 'MAT ... ',mat[name], '   "is gas"==',isgas)
        if isgas==0:
            print('    ',name, '  is NOT a gas')
        else:
            print('    ',name, '  is a GAS')
        #print('!... ============= not correct ====== VERIFY INPUT in SRIM!')


    line=[]
    line.append("Target material : Number of Elements & Layers")
    line.append("\"HHHHH into MMMMM                     \"       1               1")
    line.append("PlotType (0-5); Plot Depths: Xmin, Xmax(Ang.) [=0 0 for Viewing Full Target]")
    line.append("       5                         0          0")
    line.append("Target Elements:    Z   Mass(amu)")
    #5
    line.append("Atom 1 = MMMMM =        ZZZZZ   AAAAA")
    line.append("Layer   Layer Name /               Width Density     MMMMM")
    line.append("Numb.   Description                (Ang) (g/cm3)    Stoich")
    line.append(" 1      \"MMMMM\"             WWWWW    DDDDD       1")
    line.append("0  Target layer phases (0=Solid, 1=Gas)")
    #10
    line.append("0")
    line.append("Target Compound Corrections (Bragg)")
    line.append(" 1")
    line.append("Individual target atom displacement energies (eV)")
    line.append("      25")
    #15
    line.append("Individual target atom lattice binding energies (eV)")
    line.append("       3")
    line.append("Individual target atom surface binding energies (eV)")
    line.append("    1.67")
    line.append("Stopping Power Version (1=2006, 0=2006)")
    #20
    line.append(" 0")
    line.append("")

    line[1]=line[1].replace('MMMMM', name )
    line[1]=line[1].replace('HHHHH', ion.namesrim )

    line[5]=line[5].replace('MMMMM', name )
    line[5]=line[5].replace('ZZZZZ', str(mat[name][0]) )
    line[5]=line[5].replace('AAAAA', str(mat[name][1]) )
    line[6]=line[6].replace('MMMMM', name ) # NEW - Be(4) -> to element

    # GET TABLE DENSITY
    if outerdens<=0.0:
#        print('i... density is given 0 - trying to find a rho for...',name.title())
        if name.title() in elements:
            CC=name.title()
            #print(CC,type(CC))
            zzz=elements.index(CC)
            #print(zzz)
            dens=densities[ elements.index(name.title() ) ]
            #print('i... element ',name.title(),'found, density is set to:', dens)
            print('        ',name.title(),'found, density is set to:', dens)
        else:
            #print('i... element NOT found, maybe it is an isotope?')
            isoto1=nubase.isotope( name )
            dens=isoto1.isodensity
            print('        ',isoto1.name,'found;  density is set to:',dens)
    else:
        dens=outerdens


    #SRLINE=[] # i cannot do compound here
    SRLINE.append("---Target Data: (Solid=0,Gas=1), Density(g/cm3), Compound Corr.")
    #0    2.702    1)
    SRLINE.append("{}   {:.4f}  {}".format(isgas , dens  , 1 ) ) # gas, dens, compouncorr
    SRLINE.append("---Number of Target Elements")
    #1 )
    SRLINE.append("{}".format(1 )  ) # number of target elements 1 here
    SRLINE.append("---Target Elements: (Z), Target name, Stoich, Target Mass(u)")
    #13   "Ablb"              1             26.982)
    SRLINE.append('{}  "{}"  {}  {}'.format(mat[name][0], name, 1, mat[name][1]  ) ) # Z , name , stoich==1  u(mass)
    SRLINE.append("---Output Stopping Units (1-8)")
    SRLINE.append(" 7")
    SRLINE.append("---Ion Energy : E-Min(keV), E-Max(keV)")
    SRLINE.append(" 10    99000")

    #======================= I AM DONE WITH SR.IN for isotope or element================


    line[8]=line[8].replace('DDDDD', str(dens) )
    #um_thickness * rho
    print('i... Thickness: {:.5f} mg/cm2 ==> {:.3f} um'.format( thick, 1000*thick/dens/1e+2 )  )
    #line[8]=line[8].replace('WWWWW', str(thick*10000.) ) # thickness will be ug/cm2 in future
    line[8]=line[8].replace('WWWWW', str( 1000*thick/dens/1e-2  ) )  # in Angstr
    line[8]=line[8].replace('MMMMM', name )


    if isgas>0:
        print('!... ASSUMING GASEOUS material:', name.title() )
        line[10]=line[10].replace('0', str( isgas) )  # SOILID 0,  GAS 1

    line[12]=str(mat[name][2])  # BragCorr 1.0
    line[14]=str(mat[name][3])  # indivDsplacement 25-28
    line[16]=str(mat[name][4])  # indivLatice  3
    line[18]=str(mat[name][5])  # indivSurf    1.67-7.41

    OUTTEXT=""
    for i in range(len(line)):
        OUTTEXT=OUTTEXT+line[i] +'\r\n'

    return OUTTEXT
#    print( OUTTEXT )
#    print('------- target done ------------')
#############################################################################




#######  um to  mg/cm2   and back ######
def get_mgcm2(t_in_um,  dens):
    return t_in_um*1e-6 * 100 * dens*1000
def get_um(t_in_mgcm2,  dens):
    return 1000*t_in_mgcm2/dens/1e+2




#-----------------------------------------------







##############################################
#
#      DATA READOUT

def srim_readout(temppath):
    '''
    returns list of relevant lines
    '''
    #print("D... SRIM READ FROM ",temppath)
    with cd(temppath):
        with open(r'SRIM Outputs/TRANSMIT.txt') as f:
            print("D... SRIM READ FROM ",temppath,r'SRIM Outputs/TRANSMIT.txt')
            cont=f.readlines()
            #f.close() #automatic
        while cont[0].find('Numb Numb')<0:
            cont.pop(0)
        cont.pop(0)
        #print("DEBUG DAT",cont)
        return [x.rstrip() for x in cont]


def srim_readout_range(temppath):
    file_range3d = r'SRIM Outputs/RANGE_3D.txt'
    with cd(temppath):
        with open(file_range3d , 'rb' ) as f:
            cont=f.readlines()
            f.close()
        print('D... file is read:',file_range3d)
        for i in range(13):
            cont.pop(0) # 1st 12 lines down
            ###print( 'LINEREM=',cont[0].decode('ascii', errors='ignore') )
        while cont[0].decode('utf8', errors='ignore').find('Number')<0 or cont[0].decode('utf8', errors='ignore').find('Angstrom')<0:
            cont.pop(0)
        #print( 'LINEREM=',cont[0].decode('utf8', errors='ignore') ) # removing this line  Number    (Angstrom) (Angstrom)  (Angstrom)
        cont.pop(0)
        cont.pop(0)
        #print( 'LINE=',cont[0].decode('utf8', errors='ignore') ) # good line ?
        return [x.decode('utf8', errors='ignore').rstrip() for x in cont]



def run_srim(RPATH, TRIMIN , strip=True, silent=False , nmax=1 ):
    '''
    This creates and environment in /tmp
    where TRIM.exe can be run
    TRIMIN contains all TRIM.IN text.
    strip... strip points above 3sigma
    '''
    if (RPATH is None):
        print("!...  SRIM.EXE not found.")
        print("i... try  nuphy.py helpinstall")
        quit()
    ############## CREATE TEMP #####################
    temppath = tempfile.mkdtemp( prefix='srim_')+'/'
    if not silent: print('I... copying from',RPATH,'to',temppath)
    copy_tree( RPATH , temppath )
#    os.chdir(temppath)
    #print('D...', glob.glob("TRIM.exe")  )
    ####################### IN CD CONTEXT #############
    with cd(temppath):
        #print('D...',glob.glob("TRIM.exe")  )
        for file in glob.glob("TRIM.exe"):
            if not silent: print('    : ',file)
        with open('TRIM.IN','w') as f:
            f.write( TRIMIN )
            f.close()
        with open('TRIMAUTO','w') as f:
            f.write( TRIMAUTO )
            f.close()
        # if not silent: print('i...   TRIM.IN  and TRIMAUTO written')
        if isjupyter():
            print('i... JuPyter detected - vdislay initiated')
            silent=True #### PROBLEM with X in Jupyter?
#################################################### PROCESS WITH WAIT ####

        if silent:
            print("############### VDISPLAY ####################start r_srim")
            vdisplay = Xvfb(width=1280, height=740, colordepth=16)
            vdisplay.start()

        def worker():
            process = subprocess.Popen('wine TRIM.exe'.split(),
                                       stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL)
            output, error = process.communicate()
            return
        t=threading.Thread(target=worker)
        t.start()


        ###====>
        toolbar_width = 50
        #print("IS_INTERACTIVE", is_interactive())
        if not is_interactive():
            sys.stdout.write("[%s]" % (" " * toolbar_width))
            sys.stdout.flush()
            sys.stdout.write("\b" * (toolbar_width+1)) # return to start after '['

        #===========watch progress-------------------
        for i in range(84500):  # ONE DAY CHECK - just return number of lines
            destin=temppath+'SRIM Outputs/TRANSMIT.txt'
            destio=temppath+'SRIM Outputs/RANGE_3D.txt'
            #print(destin)
            CMD = ['wc','-l',destin]
            CME = ['wc','-l',destio]
            #print("CMD=",CMD)
            try:
                output = subprocess.check_output(CMD,
                                                  stderr=subprocess.DEVNULL)
                #print(output)
                output = output.decode('utf8').rstrip().split()[0]
                output=int(output)

                output2 = subprocess.check_output(CME,
                                                  stderr=subprocess.DEVNULL)
                output2 = output2.decode('utf8').rstrip().split()[0]
                output2=int(output2)
                output = output + output2 -28
                if output<0:
                    output=0
            except:
                output = 0

            ratio=output/nmax
            if ratio>1.0:ratio=1.0
            toolfull=int(toolbar_width*ratio)
            time.sleep(1)
            bar1="[%s" % ("#" * toolfull   )
            bar2="%s]%d/%d" % (" " * (toolbar_width-toolfull+0), output,nmax  )
            bar=bar1+bar2
            if not is_interactive():
                sys.stdout.write("\b" * (len(bar)+1)) # return to start a
                sys.stdout.write(bar)
                sys.stdout.flush()
            if not t.is_alive(): break
        ###========================>
        t.join()

        if silent:
            vdisplay.stop() #
            #print()
            print("\n############### VDISPLAY ###################stop r_srim")
#################################################### PROCESS WITH WAIT ####


#################################################### PROCESS NO WAIT ####
        #vdisplay = Xvfb(width=1280, height=740, colordepth=16)
        #vdisplay.start()
#        process = subprocess.Popen('wine TRIM.exe'.split())
        #print('CMD ended with string=',output,'... with error=',error)
        #vdisplay.stop() #
#################################################### PROCESS NO WAIT ####

#   return temppath
#def recollect_srim( temppath,  strip=True ):
    #import os
    #import time
    #vdisplay.stop()
    if not os.path.exists(temppath):
        print('!... Path',temppath,'DOES NOT EXIST !')
        return None
    #    os.chdir(temppath)
    with cd(temppath):
        if os.path.exists(r'SRIM Restore/TDATA.sav'):
            if not silent: print('ok')
        else:
            print('!... data not ready ',temppath,'... return')
            print('     can be:   Srim-Windows libraries not installed')
            print('     can do:   tar -xvzf libs2013.tgz  -C ~/.wine/drive_c/windows/')
            return None

    # TRANSMIT DATA
    data=srim_readout( temppath )
    # back with cd() =============================
    # I want to remove 1st column: T   :BUT above T 9999 it reads T10000
    # what if i replace T with space?
    data=[  'T '+x[1:] for x in data ]
    datas=[ (x.split()[1:]) for x in data ]
    datas=[ [ float(j) for j in i ] for i in datas ]
    # now i have list of list of floats : each line
    from pandas import DataFrame
    df = DataFrame(datas, columns=['n','i','e','x','y','z','cosx','cosy','cosz'])
    df['e']=df['e']/1000000.  # MeV
    df['x']=df['x']/10000.  # um
    df['y']=df['y']/10000.  # um
    df['z']=df['z']/10000.  # um
    #print( df.iloc[-5:][['e','x','y','z','cosx','cosy'] ] )
    print("D... events in ",temppath,":", len(df))
    # i dont remember these....
    df.drop('i', axis=1, inplace=True)
    df.drop('n', axis=1, inplace=True)
    print("D... events in ",temppath,":", len(df))
    if strip:
        llen=len(df)
        sigma=df['e'].std()
        mean=df['e'].mean()
        if math.isnan(sigma):
            sigma=mean
        if sigma<0.001*mean:
            sigma=0.001*mean
        print("D... sigma=",sigma,"mean==",mean)
        df=df.loc[ (df['e']>mean-3*sigma)&(df['e']<mean+3*sigma) ]  #&
        if not silent:print('i... ',llen - len(df),'events were removed due to sigma limit,new 3sigma calc...' )
        sigma=df['e'].std()
        mean=df['e'].mean()
        if math.isnan(sigma):
            sigma=mean
        if sigma<0.001*mean:
            sigma=0.001*mean
        df=df.loc[ (df['e']>mean-3*sigma)&(df['e']<mean+3*sigma) ]  #&
        remvd = llen - len(df)
        if not silent:print('i... ',llen - len(df),'events were removed due to sigma limit in total' )




    print(f"D...  len TRANSMIT {len(df)}   vs  nmax {nmax}  vs removed {remvd}")
    dfr = DataFrame({}, columns=['x','y','z'])
    # RANGE_3D
    # if len(df)<1 or  df['e'].mean is None:
    if len(df)+remvd<nmax or  df['e'].mean is None:
        print("!... no transmited ions:  i go to check RANGE_3D.TXT ... ")
        data=srim_readout_range( temppath )
        print('D... data read LEN=', len(data))
        datas=[ (x.split()[1:]) for x in data ]
        datas=[ [ float(j) for j in i ] for i in datas ]
        dfr = DataFrame( datas, columns=['x','y','z'])
        dfr['x']=dfr['x']/10000.  # um
        dfr['y']=dfr['y']/10000.  # um
        dfr['z']=dfr['z']/10000.  # um
        #print( df.iloc[-5:][['e','x','y','z','cosx','cosy'] ] )
        #df.drop('i', axis=1, inplace=True)
        #df.drop('n', axis=1, inplace=True)
        # I WILL ANNOUNCE LATER *************************************************** LATER
        #print("i... DEPTH= ",dfr['x'].mean(),'um +- ',dfr['x'].std())

        print("### Total events: {} = {} pass  + {} range ".format(nmax, len(df), len(dfr) ) )
    ###########################  DELETE TEMP #########
    #if not silent:print('x... deleting temporary', temppath)
    #shutil.rmtree(temppath)
    #              df and df with range
    return df,dfr



# in perl:
#     - convolution with nehomogenities
#     - analyse range
#     - gpressTAB  STD    my $densNEW=$densSTD  *  $p/101.325  *   273.15/$T;
#     -   if ( $args{"fthick"} >0){           amoeba











#================================================ OLD MAIN =---------------------------------------





###############################################################  SRIM
#
#  srim    -  first functions -
#
###############################


######################################
# look for compounds/elements/isotopes : return tabulated density
#
######################################
def material_density( matnam ):
    """
    called TWICE in the program:  returns  density, mm_amu
    if not material and not element => it could be isotope:
    """
    #print('i... testing if ',matnam,'is in compounds ')
    #print('DDD...  compounds keys: ',srcomp.material_text.keys()  )
    mm_amu=1.0  # NONSENSE
    myisotope=None
    # print("matnam in material_density /{}/".format(matnam))

    if matnam in srcomp.material_text.keys():
        print('F... ',matnam,'was FOUND in compounds')
        dens=srcomp.get_density( matnam  )
        print('i... FOUND density from compounds=',dens)  # mm_amu ???
        # mm_amu determined probably somewhere in SRIM.... # i dont need
    elif matnam.title() in elements:   # ELEMENT ARE AWAYS Capitalized
        print('F...  ',matnam,' was FOUND in elements ')
        CC=matnam.title()
        #print(CC,type(CC))
        zzz=elements.index(  matnam.title() )
        #print(zzz)
        dens=densities[ elements.index( matnam.title() ) ]
        mm_amu=molarweights[  elements.index( matnam.title() ) ]  # Mm for mix of isotopes
        print('i... element ',matnam.title() ,'found, density is set to:', dens)
    else:
        print('i... @material_density; element NOT found, maybe it is an isotope?')

        print("matnam",matnam, matnam.title())
        myisotope=isotope.create( matnam.title() )
        print("created:",myisotope)
        if myisotope.Z<0:
            quit()
        dens=myisotope.isodensity
        mm_amu=myisotope.amu   # This is for cross sections  Mm pure
        #
        #  COULD BE SOME CATCH HERE!!!!!!!! I REMOVED PRINTLINE
        #
        #print( myisotope,myisotope.Z, myisotope.name , myisotope)
        print('        isotope density set {:.4f} g/cm3'.format(dens) )
    return dens,mm_amu,myisotope


##################
#  question on GAS = we use 2x
#################
def isitGas( material ):
    if material.title() in srcomp.material_gas:
        return 1
    if material.title() in elements:
        eZ=elements.index(material.title())
        if gas[ eZ ]==1:
            return 1
    try:
        print("i... is is gas - isotope")
        isotope=isotope( material , silent=True  )
    except:
        return 0
    if isotope==None:
        eZ=isotope.Z
        if gas[ eZ ]==1:
            return 1
    return 0





#####################################
# get_thick_rho  ......  I extract the part
#         return   thick [ug/cm2] and rho g/cm3
#####################################
#def get_thick_rho( material,  thick, rho ,Pressure=101325, Temperature=273):   #convert properly um and find rho
def get_thick_rho( material,  thick, rho ,Pressure=P_BASE, Temperature=T_BASE):   #convert properly um and find rho
    """
    takes all thicknesses   um  ug:

    returns:  thickness,  rho, MM_amu

    1. a/ rho is given => ok,
       b/ rho not given => call material density; find rho,mm_amu

    for this it is necessary to create isotope
    """
    #print('D... in  get_thick_rho ::: DUPLICITE CODE:', material, thick, rho, '-------------')
    rho=float(rho)
    isotope=None
    mm_amu=0.0
    #print("i... @ get_thick_rho start")
    # i need rho(maybe; amu(for rrate)
    print("*** *** *** ***  get_thick_rho() ")
    rho1,mm_amu,isotope=material_density(material) # compound/element/isot = ALL
    if rho==0:
        rho=rho1

    # GASEOUS DENSITY
    # 1/ if compound - rho from function
    # 2/ element:
    rho2=rho # to keep if solid phase

    #========test gas phase =========
    #print("***testgas")
    print("D... pressure=",Pressure,"Pa")
    if material.title() in srcomp.material_gas:
        """
        trim assumes the target as STP before 1982
        T=273.15 K     I say T_BASE willl be T_STP or T_NTP
        p=101.325 kPa           =>>>>     p=101.325 kPa   10^5 !!!!!
        SRIMHelp/helpTR23.rtf
        """
        #R=101.325e+3/T_BASE/rho
        #print("*** * * * * * * * * * * * * *")
        R=P_BASE/T_BASE/rho
        rho2=Pressure/R/Temperature
        #print(P_BASE, T_BASE, rho, Pressure, Temperature)
        print(f'i...rho at STD (0deg,101.3kPa)={rho:.7f} NEW now={rho2:.7f}  (comp)')
    elif material.title() in elements:
        #print("D... rho - elements")
        eZ=elements.index(material.title())
        print("D... rho - elements  eZ={:d}".format(eZ))
        #print(gas)
        if gas[ eZ ]==1:
            R=P_BASE/T_BASE/rho
            rho2=Pressure/R/Temperature
            print(f'i...rho at STD (0deg,101.3kPa)={rho:.7f} NEW now= {rho2:.7f}  (elem)')
    else: # could be also a gaseous  isotope
        #print('D... maybe gaseous isotope?')
        if isotope is None:
            try:
                print("i... @ get_thick_rho  function")

                isotope=isotope( material , silent=True )
            except:
                 isotope=None
        if isotope==None:
            print('D... not a gaseous isotope')
        else:
            eZ=isotope.Z
            if gas[ eZ ]==1:
                print('i... GAS')
                R=P_BASE/T_BASE/rho
                rho2=Pressure/R/Temperature
                print(f'i...rho at STD (0deg,101.3kPa)={rho:.7f} NEW now={rho2:.7f}  (isotope)')
    rho=rho2
    #print("D... rho WAS deduced")
    # THICKNESS TO mgcm2:    ##### MY UNIT WILL BE mg/cm2

    thickok=False
    if thick.find('ug')>0:
        thick=float(thick.split('ug')[0])/1000
        thickok=True
    elif thick.find('mg')>0:
        thick=float( thick.split('mg')[0] )
        thickok=True

    elif thick.find('um')>0:
        #print('   i... um ! I use rho=',rho)
        thick=float(thick.split('um')[0])
        thick=get_mgcm2( thick,  rho ) # um in, mgcm2 out
        thickok=True
    elif thick.find('mm')>0:
        #print('   i... mm ! I use rho=',rho)
        thick=float(thick.split('mm')[0])
        thick=get_mgcm2( thick*1000,  rho ) # um in, mgcm2 out
        thickok=True
    elif thick.find('cm')>0:
        #print('   i... cm ! I use rho=',rho)
        thick=float(thick.split('cm')[0])
        thick=get_mgcm2( thick*10000,  rho ) # um in, mgcm2 out
        thickok=True

    if not(thickok):
        print('X...  thicknesses must be in ug,mg or um,mm')
        quit()
    #print('i... {} thickness {:.6f} mg/cm2 for rho={:.3f} ... {:.0f} A = {:.2f}um'.format( material.title(),thick,
    #                                            rho,1000*thick/rho/1e-2  ,   1000*thick/rho/1e+2 ) )
    print('         {} : {:.6f} mg/cm2 (rho={:.3f}) '.format( material.title(),thick, rho) )
    return thick, rho, mm_amu








######################################
#PREPARE TRIMIN
#  prepare single layer, return one TRIM.IN line
#
#
#            prasarna  ......... incomming0
########################################
#def prepare_trimin( material,  thick,  rho  , incomming0 , Eini, angle, number, Pressure=101325, Temperature=273):
def prepare_trimin( material,  thick,  rho  , incomming0 , Eini, angle, number, Pressure=P_BASE, Temperature=T_BASE, silent=False):
    '''
    Here I prepare materials:  single layers
    '''
    print('D... preparing TRIMIN:', material, thick, '  rho_ini=',rho, '-------------')
    #print('D... PV/T density:')
    # print("material trimin {}".format( material) )
    rho=float(rho)
    isotope=None
    if rho==0:
        rho,mm_amu,isotope=material_density(material) # compound/element/isot = ALL
        #print("DDD...  rho_fromtables=", rho)
    # GASEOUS DENSITY
    # 1/ if compound - rho from function
    # 2/ element:
    rho2=rho # to keep if solid phase
    #print("DDD .... items of material_gas", srcomp.material_gas ) #"Air" only
    if material in srcomp.material_gas:
        """
        trim assumes the target as STP before 1982 ... not sure, the air density shows values pV=nRT for 293K???
        T=273.15 K
        p=101.325 kPa
        SRIMHelp/helpTR23.rtf
        """
        R=P_BASE/T_BASE/rho
        rho2=Pressure/R/Temperature
        #print("...   P T  rho Pr Te:", P_BASE, T_BASE, rho, Pressure, Temperature)
        print(f'i...rho at STD (0deg,101.3kPa)={rho:.7f} NEW now={rho2:.7f}   (trimin-comp)')
    elif material.title() in elements:
        print("D... rho - elements")
        eZ=elements.index(material.title())
        print("D... rho - elements  eZ=",eZ)
        if gaseous[ eZ ]==1:
            R=P_BASE/T_BASE/rho
            rho2=Pressure/R/Temperature
            print(f'i...rho at STD (0deg,101.3kPa)={rho:.7f} now={rho2:.7f}  (trimin-elm)')
    else: # could be also a gaseous  isotope
        #print('D... maybe gaseous isotope?')
        try:
            isotope=isotope( material , silent=True )
        except:
            isotope=None
        if isotope==None:
            print('D... not a gaseous isotope')
        else:
            eZ=isotope.Z
            if gaseous[ eZ ]==1:
                print('i... GAS')
                R=P_BASE/T_BASE/rho
                rho2=Pressure/R/Temperature
                print(f'i...rho at STD (0deg,101.3kPa)={rho:.7f} now={rho2:.7f} (trimin isot)')
    rho=rho2

    #print("DDD... rho deduced")============================================
    # THICKNESS TO mgcm2:    ##### MY UNIT WILL BE mg/cm2
    thickok=False
    if thick.find('ug')>0:
        thick=float(thick.split('ug')[0])/1000
        thickok=True
    elif thick.find('mg')>0:
        thick=float( thick.split('mg')[0] )
        thickok=True
    elif thick.find('um')>0:
        print(f'i...  thickness in [um] ==> I use rho={rho:.7f}')
        thick=float(thick.split('um')[0])
        thick=get_mgcm2( thick,  rho ) # um in, mgcm2 out
        thickok=True
    elif thick.find('mm')>0:
        print(f'i... thickness in [mm] ==> I use rho={rho:.7f}')
        thick=float(thick.split('mm')[0])
        thick=get_mgcm2( thick*1000,  rho ) # um in, mgcm2 out
        thickok=True
    if not(thickok):
        print('!...  thicknesses must be in ug,mg or um, mm')
        quit()
    # INFO:
    print( "DDD... rho=",rho )
    print('i... {} thickness {:.6f} mg/cm2 for rho={:.7f} ...  {:.2f}um'.format(
        material,
        thick,
        rho,
#        1000*thick/rho/1e-2  ,
        1000*thick/rho/1e+2 ) )

    # AT THIN MOMENT I HAVE A GOOD rho an thick in mgcm2

    #print('DDD... goto PrepSrimFile')
    TRIMIN,SRIN=PrepSrimFile( ion=incomming0, energy=Eini, angle=0., number=number,
                            mater=material, thick=thick, dens=rho  )
    #print('DDD ... after PrepSrimFile',Eini, thick)
    #print("DDD ... SRIN==",SRIN)
    #print("********************************")
    get_sr_loss( SRIN , Eini, thick , unit="mg", silent=silent) # if no SRIN... then wnat?

    return TRIMIN
############# END OF PREPARE TRIMIN
#------------------------------------------------- END OF OLD NUPHY MAIN

#--------------------------------------------------- START OF OLD NUPHY BIN
def old_nuphy_bin( incomming=None, energy=5.8, number=100, density=0, thickness="0ug",
                  material="c12", Pressure=P_BASE, Temperature=T_BASE,
                  silent = False, fwhm=0, Store="" ):

    #print("1=============/{}/==========".format(Store)) # writeh5
    ipath=CheckSrimFiles()
    if ipath is None:
        fail("X... SRIM not found ")
    incomming0=isotope.create(incomming )
    Eini=float( energy )
    number=int(number)
    rho=density
    thick=str(thickness)
    #material=args.material.title()  # this will get complicated with layers
    #print("DDD... ", material)

    material=material.lower()           # I will keep Uppercase
    if material[0]=="(":
        material=material[1:]
    if material[-1]==")":
        material=material[:-1]
    material = material.replace("'","")
    material = material.replace(" ","")

    #print("DDD... ", material)
    nmats=len(material.split(','))
    print("D... counting number of layers",nmats)
    # rho is default 0 .... but LIST=> commaseparated STR from HERE
    if nmats>1:
        print('!... ',nmats,'materials - TEST REGIME:', thick.split(","))
        if nmats!=len(thick.split(',')):
            print('!... NOT THE SAME NUMBER OF THICKNESSES')
            sys.exit(1)
        if nmats!=len(rho.split(',')):
            if float(rho)!=0.:
                print('!... NOT THE SAME NUMBER OF densities')
                sys.exit(1)
            else:
                rho=','.join( map(str,[0]*nmats) )
        print('i... PREPARING ANALYSIS  mat, thick, rho for:', nmats,"materials",material,".")
        TRILIST=[]
        # now work with rho commaseparated for different layers
        # --------------------------------------- BEGIN --------------@@@
        for imat in range(nmats):
            print(imat,'... =========', material.split(',')[imat], thick.split(',')[imat],  rho.split(',')[imat]
                  , incomming0 , Eini , 0 , number
                  ,    "================================"  )
            #TRIMIN=main.prepare_trimin(  material, thick,  rho  , incomming0  , Eini, 0, number) # prasarna incomming0

            TRILIST.append( prepare_trimin(  material.split(',')[imat], thick.split(',')[imat],  rho.split(',')[imat] , incomming0 , Eini , 0 , number  , Pressure=Pressure, Temperature=Temperature, silent=silent)  )
        # --------------------------------------------- END -------@@@
        print('i... I GOT ALL TRIM.IN files. Now somebody must merge....')
        ############################   MERGING  LAYERS ##############
        print('D--------------')
        for xi,xii in enumerate(TRILIST):  print( xi, xii,'\n')          # PRINT
        TRIMIN="==> SRIM-2013.00 This file controls TRIM Calculations.\r\n"
        #TRIMIN= TRIMIN + TRILIST[0].split("\n")[0].rstrip()+'\r\n'
        TRIMIN= TRIMIN + TRILIST[0].split("\n")[1].rstrip()+'\r\n'
        TRIMIN= TRIMIN + TRILIST[0].split("\n")[2].rstrip()+'\r\n'
        TRIMIN= TRIMIN + TRILIST[0].split("\n")[3].rstrip()+'\r\n'
        TRIMIN= TRIMIN + TRILIST[0].split("\n")[4].rstrip()+'\r\n'
        TRIMIN= TRIMIN + TRILIST[0].split("\n")[5].rstrip()+'\r\n'
        TRIMIN= TRIMIN + TRILIST[0].split("\n")[6].rstrip()+'\r\n'
        TRIMIN= TRIMIN + TRILIST[0].split("\n")[7].rstrip()+'\r\n'
        # target material  num ele and layers
        #TRIMIN=TRIMIN+"            8 \r\n"


        #print(TRIMIN)
        #quit()
        #############################################################
#        with open('TRIM.IN.ALL','w') as f:
#            for imat in range(nmats):
#                f.write(TRILIST[imat])
        line8=[]      # Target material+1
        TRILISTTOT=[] # totallist for Atom
        lineLay=[]    # Layer Layer long line
        layerList=[]
        # -------------------------------- BEGIN @@@@@@
        for imat in range(nmats):
            listOfLines=TRILIST[imat].split('\n')
            if listOfLines[7].find('Target material')<0:
                print('!... Target material line not detected...quit')
                quit()
            # define line8 (7: Target material)
            line8.append(   re.findall(r'".+"|[\w\.]+',  listOfLines[8] )  )
            TRILISTTOT.extend(  listOfLines  )
            # lineLay...
            liLa=[ i for i in listOfLines if re.match('^Layer\s+Layer\s+Name',i)  ]
            lineLay.extend(liLa)  # line with columns for layers.
            #---- duplicate: but i find #line of Layer Layer +2
            for j,v in enumerate( listOfLines ):
                if v.find('Layer')>=0 and v.find('Density')>0:
                    print(imat,'LAYER LINE= #',j+2+1) # starts with 0
                    layerList.append( re.findall(r'".+"|[\w\.\-]+', listOfLines[j+2] ) )
        # -------------------------------- END @@@@@@
        #print(line8)
        layname='...'.join( [ i[0].strip("\"").rstrip() for i in line8]  )
        layname='"'+layname+'"'
        nelems=sum( map(int, [i[1] for i in line8] ) )
        nlayers=sum( map(int, [i[2] for i in line8] ) )
        print(layname,nelems,nlayers)
        TRIMIN=TRIMIN+"{} {} {}\r\n".format(layname,nelems,nlayers)
        #TRIMIN= TRIMIN + TRILIST[0].split("\n")[8].rstrip()+'\r\n'  # He 4  into C  - nedavat
        TRIMIN= TRIMIN + TRILIST[0].split("\n")[9].rstrip()+'\r\n'
        TRIMIN= TRIMIN + TRILIST[0].split("\n")[10].rstrip()+'\r\n'
        TRIMIN= TRIMIN + TRILIST[0].split("\n")[11].rstrip()+'\r\n'

        # NOW I need to get all Atom .. = ... = lines
        #print(TRILISTTOT)
        #regex = re.compile('^Atom\s\d+\s=\s')
        atoms=[i for i in TRILISTTOT if re.match('^Atom\s\d+\s=\s',i) ]
        if len(atoms)!=nelems:
            print('!... Atoms lines and # elements differ!')
            quit()
        #        atoms=[m.group(1) for l in TRILISTTOT for m in [regex.search(l)] if m]
        #atoms=re.findall(r'Atom\s\d+\s=\s', TRILISTTOT)
        for i,v in enumerate(atoms):
            atoms[i]=re.sub( 'Atom\s(\d+)\s','Atom '+str(i+1)+' ' , v ).rstrip()
        print( '\n'.join( atoms ) )
        TRIMIN=TRIMIN+ '\r\n'.join(atoms)+'\r\n'
        # NOW I need Layer Layer
        preLayer=re.sub(r'^(.+Density).+$',r'\1', lineLay[0] )
        for i,v in enumerate(lineLay):
            lineLay[i]=re.sub('^.+?Density ','', v).strip()
        print( preLayer,'  '.join(lineLay) )
        TRIMIN=TRIMIN+preLayer+' '+'  '.join(lineLay)+'\r\n'
        # NOW I need the same with next "stoich stoich stoich...."
        lineStoich="Numb.   Description                (Ang) (g/cm3)   "+" Stoich "*nelems
        print(lineStoich)
        TRIMIN=TRIMIN+lineStoich+'\r\n'
        # NOW I need 1   "Layer 1";  2  "Layer 2"
        zeroes=0
        for i,v in enumerate(layerList):
            zstring=' 0   '*zeroes
            zpost=' 0   '*(nelems-zeroes -  int(line8[i][1]) )
            prepart='  '.join(v[1:4])
            postpart='  '.join(v[4:])
            print( "{} {} {} {} {}".format(i+1,prepart,zstring,postpart, zpost) )
            TRIMIN=TRIMIN+ "{} {} {} {} {}\r\n".format(i+1,prepart,zstring,postpart, zpost)
            zeroes=zeroes+int(line8[i][1])
            # 16 fields;
        # NOW I need to copy lines with GAS.....
        lineGas="0  Target layer phases (0=Solid, 1=Gas)"
        print(lineGas)
        TRIMIN=TRIMIN+lineGas+'\r\n'
        for i,v in enumerate(layerList):
            ###print( 'material====',v )
            print(  isitGas(v[1]),' '   , end=' ')
            TRIMIN=TRIMIN+ str( isitGas(v[1]) )+' '
        #print()
        TRIMIN=TRIMIN+'\r\n'
        ######## RAGG
        lineBragg="Target Compound Corrections (Bragg)"
        print(lineBragg)  # i want to put all lines  12 ( i think)
        TRIMIN=TRIMIN+lineBragg+'\r\n'
        for imat in range(nmats):
            listOfLines=TRILIST[imat].split('\n')
            for jmat in range( len(listOfLines) ):
                if listOfLines[jmat].find('Target Compound Corrections')>=0:
                    #print( listOfLines[jmat].rstrip() )
                    print( listOfLines[jmat+1].rstrip()  , end=' ')
                    TRIMIN=TRIMIN+ listOfLines[jmat+1].rstrip() +' '
                    break
            if jmat==len(listOfLines)-1:
                print('!... Bragg line not found')
                quit()
        #print()
        TRIMIN=TRIMIN+'\r\n'
        #Individual target atom displacement energies (eV)
        lineAtomDisp="Individual target atom displacement energies (eV)"
        print(lineAtomDisp)
        TRIMIN=TRIMIN+lineAtomDisp+'\r\n'
        for imat in range(nmats):
            listOfLines=TRILIST[imat].split('\n')
            for jmat in range( len(listOfLines) ):
                if listOfLines[jmat].find('Individual target atom displacement energies')>=0:
                    #print( listOfLines[jmat].rstrip() )
                    print( listOfLines[jmat+1].rstrip()  , end=' ')
                    TRIMIN=TRIMIN+ listOfLines[jmat+1].rstrip() +' '
                    break
            if jmat==len(listOfLines)-1:
                print('!... Displacement line not found')
                quit()
        #print()
        TRIMIN=TRIMIN+'\r\n'

        #Individual target atom displacement energies (eV)
        lineAtomDisp="Individual target lattice binding energies (eV)"
        print(lineAtomDisp)
        TRIMIN=TRIMIN+lineAtomDisp+'\r\n'
        for imat in range(nmats):
            listOfLines=TRILIST[imat].split('\n')
            for jmat in range( len(listOfLines) ):
                if listOfLines[jmat].find('Individual target atom lattice binding energies')>=0:
                    #print( listOfLines[jmat].rstrip() )
                    print( listOfLines[jmat+1].rstrip()  , end=' ')
                    TRIMIN=TRIMIN+ listOfLines[jmat+1].rstrip() +' '
                    break
            if jmat==len(listOfLines)-1:
                print('!... Lattice binding line not found')
                quit()
        #print()
        TRIMIN=TRIMIN+'\r\n'
        #Individual target atom displacement energies (eV)
        lineAtomDisp="Individual target atom surface binding energies (eV)"
        print(lineAtomDisp)
        TRIMIN=TRIMIN+lineAtomDisp+'\r\n'
        for imat in range(nmats):
            listOfLines=TRILIST[imat].split('\n')
            for jmat in range( len(listOfLines) ):
                if listOfLines[jmat].find('Individual target atom surface binding energies')>=0:
                    #print( listOfLines[jmat].rstrip() )
                    print( listOfLines[jmat+1].rstrip()  , end=' ')
                    TRIMIN=TRIMIN+ listOfLines[jmat+1].rstrip() +' '
                    break
            if jmat==len(listOfLines)-1:
                print('!... Surface binding line not found')
                quit()
        #print()
        TRIMIN=TRIMIN+'\r\n'
        print('Stopping Power Version (1=2011, 0=2011)')
        TRIMIN=TRIMIN+'Stopping Power Version (1=2011, 0=2011)\r\n'
        print(' 0 ')
        TRIMIN=TRIMIN+' 0\r\n'

        print('\n\n\n',TRIMIN,"\n\n\n")
        #quit()

    else:
        print("i... one material (not layers) - preparing TRIMIN")
        TRIMIN=prepare_trimin(  material, thick,  rho  , incomming0  ,
                                Eini, 0,
                                number,
                                Pressure=Pressure, Temperature=Temperature,
                                silent=silent) # prasarna incomming0
        #  angle==0
    #########################################
    # PREPARE FILE
    ##########################################
    #    print('D... goto TRIMIN')
    #    TRIMIN,SRIN=sr.PrepSrimFile( ion=n0, energy=Eini, angle=0., number=number,
    #                            mater=material, thick=thick, dens=rho  )



    #print("i... ----running rho=",rho,type(rho)) #  rho==0 if compound??
    # RUN ############################
    if silent:
        tmpp,tmppr=run_srim(ipath, TRIMIN,  silent=True, nmax=number)
    else:
        tmpp,tmppr=run_srim(ipath, TRIMIN,  silent=False, nmax=number)



    # i am adding an artifitial Eini = 0
    tmpp['eini']=tmpp['x']*0.0 +  Eini
    #
    # tmpp ========= DATAFRAME FROM SRIM
    #
    IMPLANT = False
    PASSTHR = False
    if 'e' in tmpp and len(tmpp) > 0: # 'e' is it is always IN
        PASSTHR = True
        if fwhm!=0.:  # convolute wit FWHM at Eini level ##### save -f
            print("i... fwhm applied to E")
            tmpp['fwhmi']=np.random.normal( 0.0, float(fwhm)/2.355 ,  len( tmpp ) )
            tmpp['e']=tmpp['e']+tmpp['fwhmi']
        deint=tmpp['e'].max()-tmpp['e'].min()
        sigma=tmpp['e'].std()
        #if fwhm!="":  # convolute wit FW
        #    sigma= ( sigma*sigma + (float(fwhm)/2.355)**2 )**0.5
        mean=tmpp['e'].mean()
        median=tmpp['e'].median()
        print(tmpp[-5:]) # MAIN OUTPUT  TRANSMITTED
        print()
        print( "{:.3f} MeV (median {:.3f}) +- {:.3f}  hi-lo={:.3f}  Eloss={:.3} MeV ({} events)".format( mean, median, sigma, deint, Eini-mean, len(tmpp)) )

    #else:
    if len(tmppr)>0:
        IMPLANT=True
        tmppr['eini']=tmppr['x']*0.0 +  Eini
        #print(tmpp)
        #print()
        print(tmppr[-5:])  # MAIN OUTPUT RANGE3D
        #
        output_unit = 'um'
        divko = 1
        if tmppr['x'].mean() > 10_000:
            output_unit = 'mm'
            divko = 1000
        print('{:.3f} +- {:.4f} {} implanted depth ({} events)'.format( tmppr['x'].mean() / divko,
                                                                        tmppr['x'].std() / divko,
                                                                        output_unit,
                                                                        len(tmppr) )  )
        mean=0.0
        median=0.0
        deint=0.0
        sigma=0.0
        #print( tmpp['e'].max(),tmpp['e'].min(), de  )
    #plt.hist( tmpp['e'], 20 , facecolor='red', alpha=0.25)
    #    print("R...    E mean +- std")
    #    print(tmpp['e'].mean(), '  ' ,tmpp['e'].std() )
    #   print(tmpp['e'].mean(), '  ' ,tmpp['e'].std() )


    print(f" IMPLANT {IMPLANT}, PASSTHR {PASSTHR}")
    if IMPLANT and PASSTHR:
        print("i... combining implant and passthrough")
        tmpp = pd.concat([tmpp,tmppr], axis=0, ignore_index=True)
    elif IMPLANT:
        tmpp = tmppr
        #print(tmpp)

    ### MAYBE - I WILL NUMBER ALREADY FROM HERE
    if Store!="":  # writeh5

        store = pd.HDFStore( Store )
        existing=len(store.keys())
        store.close()

        print('D... already existing keys: ', existing )

        #print(store)
        #print(" MAT ****************************", material.title()   )
        # WHY THE HACK   TITLE????
        #if material.title() in srcomp.material_gas:
        pt=""
        for ima in material.split(","):
            if ima.lower() in srcomp.material_gas:
                pt='P{}_T{}'.format( Pressure, Temperature )
        #print( "D... args=",fwhm )
        #  rho instead of density === can be a problem :  0,0
        WRmat=material.lower().replace(",","_")
        WRthi= thickness.replace(",","_")
        # howto get rho from compound????
        #print("+++++", rho)
        WRrho=str(rho).replace(",","_")
        #print("+++++", WRrho)

        # I removed pt{} and left {}
        # I fill ____ to keep alignement  _<6 .........
        fname='srim{:03d}_{}_in_{:_<6s}_t{:_<6s}_r{}_{}_n{:04d}_ei{:06.3f}_ef{:06.3f}_sf{:06.4f}_f{:0.4f}'.format(
            existing, # serialnumber
            incomming, # h1
            WRmat, WRthi,  # mylar, 120um
            WRrho, # DENSITY only if in argument else 0
            pt, #  ptP...T...
            int(number), # 9999
            float(energy), # keV
            mean, # keV
            sigma, # straggling ~0.1keV
            float(fwhm) # FWHM??? artificially already into simulation?
        )
        #
        print("i... TAGName:\n",fname )
        print()
        fname=fname.replace('.','_')

        # shorter time when parallel
        store = pd.HDFStore( Store )
        if len(tmpp) > 0:
            store[fname] = tmpp # DF TRANSMIT + RANGE combined ABOVE concat
            #elif len(tmppr) > 0:
            #    store[fname] = tmppr # DF RANGE
        else:
            print("X... DF NULL!!!!", tmpp)
        #print(store)
        store.close()

# RUN SRIM ENDED





#--------------------------------------------------- END OF OLD NUPHY BIN






#---------------------------------------------------------------------NEW MAIN--------------------
# i need i,o, e, angle..... NOT excitation
#  d,h reserved
#
def main( i="", m="" , t="", e="", a="",  n=100,
          dens=0,              # override density
          f=0,                 # fwhm of the detector
          pressure=P_BASE,
          kelvin=T_BASE, #k =temp in K was 273.15
#          h="",                #
          writeh5="",
          s = False,           # silent
          debug=False,
          ):
    """
    SRIM MODULE:
    -i: h2        ... projectile
    -m: mylar     ... material (isotope,element,compound)
    -t: 15um      ... thickness (um,mm,cm,m, mgcm2 ugcm2)
    -e: 5.8       ... energy in MeV

    -f:    was like file out, now fwhm
    -dens: override density
    -w:    write:store into h5 file
    """
    global print
    print=super_print(debug)(print)
    print("\n")

    ipath=CheckSrimFiles()
    # -- in commandline it may be a tuple: force to str
    m = str(m)
    t = str(t)
    if len(m.split(","))!=len(t.split(",")):
        print("X... number of materials and targets differ")
        sys.exit(1)
    if len(m.split(","))!=len(str(dens).split(",")):
        print("X... number of materials and densities differ, I put zeroes")
        dens=",".join( ["0" for x in m.split(",")] )
        print(dens)
        #sys.exit(1)

    # print("m",m,type(m))
    #=========================================== SRIM ERAL STUFF =======================
    if 0==0:
        if i == "":
            print(main.__doc__)
            fail(Bcolors.WARNING+"?... give me projectile,target  -i h2" + Bcolors.ENDC )
        if m == "": fail(Bcolors.WARNING+"?... give me material           -m c" + Bcolors.ENDC )
        if e == "": fail(Bcolors.WARNING+"?... give me energy of the reaction in MeV -e 5.8" + Bcolors.ENDC )
        # if a == "": fail(Bcolors.WARNING+"?... give me angle of the reaction -a 15" + Bcolors.ENDC )
        if t == "": fail(Bcolors.WARNING+"?... give me target thickness   -t 10ug -t 10um" + Bcolors.ENDC )
        # if f == "": fail(Bcolors.WARNING+"?... give me value,outfile      -f t3a  -f t3a,a.txt" + Bcolors.ENDC )
        # -S a,T3 ... save to textfile the value

        if isinstance(writeh5,bool): fail(Bcolors.WARNING+"? -w filename.h5 is expected")

        if writeh5=="": print(Bcolors.WARNING+"i... not saving.... -w filename.h5" + Bcolors.ENDC)
        #
        #
        print(Bcolors.OKGREEN + "D... PROJECTILE   :", i + Bcolors.ENDC )
        nu1=isotope.create( i , debug=debug)
        nu1.pprint()
        print( Bcolors.OKGREEN +  "D... E=           :", e,"MeV" + Bcolors.ENDC )
        print( Bcolors.OKGREEN +  "D... TARGET       :", m + Bcolors.ENDC )
        #nu2.pprint()
        print( Bcolors.OKGREEN +  "D... Thickness   =:", t + Bcolors.ENDC)



        print( Bcolors.OKGREEN +  "i... to run without SRIM GUI screen:  -s" + Bcolors.ENDC)
        # print( Bcolors.OKGREEN +  "D... OUTGOING 1   :" , m+ Bcolors.ENDC)
        #nu3.pprint()

        # print( Bcolors.BOLD +  "D... Angle       =:", str(a) + Bcolors.ENDC)
        # print( Bcolors.BOLD +  "D... Excitation  =:", x,"MeV"+ Bcolors.ENDC )
        #  print( Bcolors.BOLD +  "D... Outputfile,V=:", "None"+ Bcolors.ENDC )
        print("\n")
        #print("... zmatek before old *******  T ", kelvin)
        old_nuphy_bin(incomming=i, energy=e, number=n,
                      density=dens,
                      thickness=t,
                      material=m, Pressure=pressure, Temperature=kelvin,
                      silent = s,
                      fwhm=f,
                      Store=writeh5 )


        # h1 = isotope.create(i)  # incomming ion
        # TRIMIN,SRIN=PrepSrimFile( ion=h1, energy=e, angle=0., number=n,
        # mater=m, thick=t, dens=1.85  )
        # #####? create_env(ipath)
        # print("------------ TRIMIN PREPARED -----------------------------")
        # print(TRIMIN)
        # print("------------ TRIMIN PREPARED -----------------------------")
        # run_srim(ipath, TRIMIN,  silent=False, nmax=1000)



#print("i... module  kinematics  is being loaded", file=sys.stderr)
if __name__ == "__main__":
    print("D... in main of project/module:  nuphy2/srim ")
    print("D... version :", __version__ )
    Fire( main )
