#!/usr/bin/env python3
"""
 This must be the old - semifunctional RADCAP
"""

from fire import Fire
from nuphy2.version import __version__

import subprocess as sp
import os

#import fileinput
import io
import re
import numpy as np

import matplotlib.pyplot as plt


_DEBUG=0


#==========================================================================RUNDICAP
def radcap_run(number, val=1):
    radcapexe='dicap.exe'
    #========================================== EXE PRESENCE ===============
    if os.path.isfile( radcapexe ):
        print("D... radcap exec found here")
        radcapexe="./"+radcapexe
    else:
        ok=False
        try:
            wh=sp.check_output( ['which',radcapexe ] ).decode('utf8').rstrip()
            ok=True
        except:
            print("!... NO RADCAP found:",radcapexe )
        if not(ok):quit()
        print("D... which => ",wh)
        radcapexe=wh


    #========================================= INPUT FILE ===========================
    if str(number)=='2':
        INP='EIGEN.INP'
        try:
            os.remove('EIGEN.TXT')
        except:
            print("D!.. output was not there to get deleted")
        if not( os.path.isfile( INP ) ):
            print("!... radcap input not present:", INP )
            quit()
        else:
            print("D... input present", INP)
    #========================================= INPUT FILE ===========================
    if str(number)=='4':
        INP='CONT.INP'
        number="4\n1\n"+str(val)+"\n"  # Ecm....
        try:
            os.remove('CONT.TXT')
        except:
            print("D!.. output was not there to get deleted")
        if not( os.path.isfile( INP ) ):
            print("!... radcap input not present:", INP )
            quit()
        else:
            print("D... input present", INP)
    #========================================= INPUT FILE ===========================
    if str(number)=='5':
        INP='DICAP.INP'
        number="5\n"  # Ecm....
        try:
            os.remove('DICAP.TXT')
        except:
            print("D... output was not there to get deleted (renamed?)")
        if not( os.path.isfile( INP ) ):
            print("!... radcap input not present:", INP )
            quit()
        else:
            print("D... input present", INP)
    #=========================================== RUN =============================
    try:
        #ps = sp.Popen(('echo',  str(number) ), stdout=sp.PIPE, stderr='/dev/null')
        ps = sp.Popen(('echo',  str(number) ), stdout=sp.PIPE)
        output = sp.check_output( radcapexe.split(), stdin=ps.stdout ).decode('utf8').rstrip()
        ps.wait()
    except:
        print("!... radcap crashed. Check the  input...", INP)
        quit()
    #print(output)
    #runthis='echo '+number+' | ./dicap.exe '
    #print('...exit code EIGEN=',os.system( runthis ))
    output=output.split('etc.')[1]
    return output







#============================================================= REPLACE ORBIT
def nuphy_replace_orbit(fname, orbit, spdf , prepend=""):
    print("D... replacing an  orbit with", orbit)
    # Does a list of files, and
    # redirects STDOUT to the file in question
    if fname=="EIGEN.INP":
        repl=False
        replline=1
    if fname=="CONT.INP":
        repl=False
        replline=3
    if fname=="DICAP.INP":
        repl=True
        replline=1
    orbok=True
    countlines=-1
    with io.FileIO(fname, 'r') as f:
        inp=f.read().decode('utf8').split("\r\n")
        with  io.FileIO(fname+".2", 'w') as f2:
            for i in inp:
                if i.find("*")!=0: countlines+=1
                if (countlines==replline) and (orbok):
                    orbok=False
                    if repl: # DICAP i have all
                        print("D?.. DICAP replacement", prepend)
                        ebound=i.split()[6] # ebound... 0.14
                        f2.write( bytes( prepend+"     "+ebound+"\r\n", "UTF8" ) )
                    else:
                        print("D?.. nonDICAP replacement")
                        f2.write( bytes( prepend+spdf[orbit]+"\r\n", "UTF8" ) )
                    continue  # DONT CONTINUE
#                #=========== NEXT LINE MEANS ORBOK....
#                if i.find("nuphy_replace_orbit")>=0:
#                    orbok=True
                if len(i)>0:
                    f2.write( bytes( i+"\r\n", "UTF8" ) )
    os.rename(fname,fname+".orig")
    os.rename(fname+".2",fname)








def nuphy_get_orbit( fname , spdf ):
        print("D... reading ORBIT ... ")
        if fname=="EIGEN.INP": orbline=1
        if fname=="CONT.INP":  orbline=3
        if fname=="DICAP.INP":  orbline=1
        with io.FileIO( fname , 'r') as f:
            inp=f.read().decode('utf8').split("\r\n")
            inp=[ i for i in inp if i.find("*")!=0]
            for j in spdf.keys():
                #print( "D... orbs:",spdf[j].split(), inp[orbline].split()  )

                if fname=="EIGEN.INP":
                    comp=inp[orbline].split()
                if fname=="CONT.INP":
                    comp=inp[orbline].split()[2:]
                if fname=="DICAP.INP":
                    comp=inp[orbline].split()[4:6]
                    #print(comp)


                if spdf[j].split()==comp:
                    orbit=j
                    #print( "D... orbit was found: ", orbit, comp )
                    return orbit
        return "unresolved"










#=========================================================================
def radcap_eigen(orbit='', WSP=[] , plot=False ):  # 0s1,0p3,0p1,0d5 ... WSpotential params
    """
    RUNS radcap option 2: EIGEN.INP
    """
    ################# EIGEN
    spdf={"0s1":"  0  0.5  0 ",
    "0p3":"  0  1.5  1 ",
    "0p1":"  0  0.5  1 ", ###8
    "0d5":"  0  2.5  2 ",
    "1s1":"  1  0.5  0 ",
    "0d3":"  0  1.5  2 ", ####20
    "0f7":"  0  3.5  3 ", ####28
    "1p3":"  1  1.5  1 ",
    "0f5":"  0  2.5  3 ",
    "1p1":"  1  0.5  1 ", #####40
    "0g9":"  0  4.5  4 ", #####50
    "0g7":"  0  3.5  4 ",
    "1d5":"  1  2.5  2 ",
    "1d3":"  1  1.5  2 ",
    "2s1":"  2  0.5  0 ",
    "0h11":" 0  5.5  5 "
    }

    e_bind={}
    print("D... RADCAP RUN - option 2 - EIGEN.INP")
    #------------- input file.... i dont want to create myself?
    #a=" 1 9999  250. "  ###  IOPT  NPTS  RMAX(250.fm)
    #a=a+'\n'+spdf[orbit]
    #    a=a+'\n '+' '.join( map( str, WSP ) )  + '\n'
    #    a=a+' 1. 1. '+str(self.Z)+' '+str(self.A) + '\n' ##PROTONS HERE!!

    if orbit!="":
        nuphy_replace_orbit("EIGEN.INP", orbit , spdf )
    else:
        orbit=nuphy_get_orbit("EIGEN.INP", spdf )
        print("D... orbit found in INP:", orbit)

    try:
        os.rename("GSWF.INP","GSWF.INP.prev")
    except:
        print("D... no previous GSWF.INP found")
    #================================================== RUN ===============
    radcap_run('2')
    #================================================== READ EIGEN.TXT same as GSWF.INP
    lines = [line.strip('\n') for line in open('EIGEN.TXT')]
    ######### SEARCH Energy
    eli=[ i for i, word in enumerate(lines) if re.search('Energy',word) ]
    #print( eli[0],')', lines[ eli[0]+1] )  # Check the line number
    try:
        e_bind[ orbit ]=  float(lines[ eli[0]+1 ].split()[3] ) # i want it to be float
    except:
        e_bind[ orbit ]= -9999.9
    print('E (',orbit,')= ', e_bind[ orbit ], 'MeV')
    ######### SEARCH WAVE
    eli=[ i for i, word in enumerate(lines) if re.search('Wavefunction',word ) ]
    #		for i in range(eli[0]+2,len(lines) ):
    #		d = numpy.loadtxt("EIGEN.TXT", dtype=float,skiprows= eli[0]+2 )
    r=[]
    w=[]
    for i in range(eli[0]+2,    len(lines) ):
        r.append(  float(lines[i].strip().split()[0]) )
        w.append(  float(lines[i].strip().split()[1]) )
    nu=np.array( list( zip(r,w) ) )

    #------------try OLD--------------------------------------------
    prev=False
    try:
        lines = [line.strip('\n') for line in open('GSWF.INP.prev')]
        r2=[]
        w2=[]
        for i in range( 1,   len(lines) ):
            r2.append(  float(lines[i].strip().split()[0]) )
            w2.append(  float(lines[i].strip().split()[1]) )
        sf2=np.array( list( zip(r2,w2) ) )
        prev=True
    except:
        print("D!... no previous GSWF.INP found")
    # ========================= returning function r x W
    if plot:
        plt.plot(r2, w2 , ':', color="gray",label='prevous g.s. wf')
        plt.plot(r, w , '.-', label='g.s. wavefunction')
        plt.yscale('log')
        plt.xscale('log')
        plt.grid()
        plt.legend()
        plt.show( )
    return nu







#======================================================================== PhaseShifts-4

def radcap_cont(  orbit='' ,Ecm=-1 , WSP=[] , plot=False, Eres=0.0, maxEne=5.0, maxEneN=600):
    """
    runs option 4: phase shift
    """
    ################# ORBITS CONT
    spdf={
        "0s1":"   0   0.5 ",
        "0p3":"   1   1.5 ",
        "0p1":"   1   0.5 ", ###8
        "0d5":"   2   2.5 ",
        "1s1":"   0   0.5 ",
        "0d3":"   2   1.5 ", ###20
        "0f7":"   3   3.5 ", ###28
        "1p3":"   1   1.5 ",
        "0f5":"   3   2.5 ",
        "1p1":"   1   0.5 ", ##40
        "0g9":"   4   4.5 ", ##50
        "0g7":"   4   3.5 ",
        "1d5":"   2   2.5 ",
        "1d3":"   2   1.5 ",
        "2s1":"   0   0.5 ",
        "0h11":"  5   5.5 "
    }
    a=" 1 9999  250. "+str(maxEneN)   # opt, points,  rmax, NEPTS n.points in energy
    #    a=a+'\n '+' '.join( map( str, WSP ) )  + '\n'
    #    a=a+' 1. 1. '+str(Z)+' '+str(A) + '\n' ##PROTONS HERE!!
    #    a=a+' 0  '+str(maxEne)+' '+cspdf[orbit]+'\n'   ## energy 0-8MeV
    # with io.FileIO("CONT.INP", 'w') as file:
    #     file.write( bytes(a,'UTF8') )
    #     runthis='rm CONT.TXT; rm CWAVE.TXT;echo "4\n1\n'+str(Eres)+'\n" | dicap.exe '

    if orbit!="":
        if Ecm<0:
            print("!... give me orbit and Ecm for wavefunction!")
            quit()
        nuphy_replace_orbit("CONT.INP", orbit , spdf ," 0.    3.   " )
    else:
        orbit=nuphy_get_orbit( "CONT.INP", spdf)
        print("D... orbit found in INP:", orbit)

    #================================================== RUN ===============
    if Ecm<0: Ecm=0.3
    radcap_run('4', Ecm)
    #================================================== READ

    lines = [line.strip('\n') for line in open('CONT.TXT')]
    #------------------------------------------------ get res energy
    eli=[ i for i, word in enumerate(lines) if re.search('Resonance energy',word) ]
    if (len(eli)>0):
        print( 'i... (line ',eli[0],')', lines[ eli[0] ] )
        ResLine=eli[0]-3
    else:
        ResLine=len(lines)
    #----------------------------------------------- phase shift
    eli=[ i for i, word in enumerate(lines) if re.search('hase shift',word) ]
    r1=[]
    w1=[]
    #print( eli )
    for i in range(eli[0]+2,    eli[1]-3 ):
        lines[i]=re.sub( 'D', 'e', lines[i] )
        #print(lines[i])
        r1.append(  float(lines[i].strip().split()[0]) )
        w1.append(  float(lines[i].strip().split()[1]) )
    dmax=max(w1)
    d=np.array( list( zip(r1,w1) ) )

    #------------------------------------------------- derivation of phase shift
    r2=[]
    w2=[]
    for i in range(eli[1]+2,    ResLine ):
        lines[i]=re.sub( 'D', 'e', lines[i] )
        #print(lines[i])
        r2.append(  float(lines[i].strip().split()[0]) )
        w2.append(  float(lines[i].strip().split()[1]) )
    w2=[ i*dmax/max(w2) for i in w2 ]
    dd=np.array( list( zip(r2,w2) ) )


    #================================================================== WF
    lines2 = [line.strip('\n') for line in open('CWAVE.TXT')]
    r3=[]
    w3=[]
    for i in range( len(lines2) ):
        r3.append(  float(lines2[i].strip().split()[0]) )
        w3.append(  -1.0*float(lines2[i].strip().split()[1]) )
    dcw=np.array( list( zip(r3,w3) ) )


    # ========================= returning function r x W
    if plot:
        plt.subplot(2,1,1)
        plt.plot(r1, w1 , '-' , label="phase shift")
        plt.plot(r2, w2 , '--'  , label="derivative")
        plt.grid()
        plt.legend()
        plt.subplot(2,1,2)
        plt.plot(r3, w3 , '.:', label="RealWF for Ecm="+str(Ecm))
        #plt.yscale('log')
        plt.xscale('log')
        plt.grid()
        plt.legend()
        plt.show( )
    #return d, dd, dcw








def plot_dicap( fname="DICAP.TXT" ):
    plot=True
    if fname!="DICAP.TXT":
        print("i... plotting ", fname)
    lines = [line.strip('\n') for line in open( fname )]
    #eli=[ i for i, word in enumerate(lines) if re.search('[eV.b]',word) ]
    r=[]
    w=[]
    for i in range( 0,   len(lines) ):
        lines[i]=re.sub( 'D', 'e', lines[i] )
        #print(lines[i])
        r.append(  float(lines[i].strip().split()[0]) )
        w.append(  float(lines[i].strip().split()[4]) )  # 5 is S-Factor
    sf=np.array( list( zip(r,w) ) )

    #------------try OLD--------------------------------------------
    prev=False
    try:
        lines = [line.strip('\n') for line in open('DICAP.TXT.prev')]
        #eli=[ i for i, word in enumerate(lines) if re.search('[eV.b]',word) ]
        r2=[]
        w2=[]
        for i in range( 0,   len(lines) ):
            lines[i]=re.sub( 'D', 'e', lines[i] )
            #print(lines[i])
            r2.append(  float(lines[i].strip().split()[0]) )
            w2.append(  float(lines[i].strip().split()[4]) )  # 5 is S-Factor
        sf2=np.array( list( zip(r2,w2) ) )
        prev=True
    except:
        print("D...  no previous dicap.tx.prev found")

    # ========================= returning function r x W
    if plot:
        #plt.subplot(2,1,1)
        if prev:
            plt.plot(r2, w2 , ':',color='gray', label='previous S-Factor')
            print("D... previous S-F  plotted")
        label='S-Factor'
        if fname!="DICAP.TXT":
            label=fname.split("/")[-3:]
        plt.plot(r, w , '.-', label=label)
        plt.grid()
        plt.title("S-Factor")
        plt.xlabel("E [MeV]")
        plt.ylabel("S [eV b]")
        #plt.subplot(2,1,2)
        #plt.yscale('log')
        #plt.xscale('log')
        #plt.grid()

        plt.legend()
        plt.show( )
    #return d, dd, dcw







#======================================================================== direct cap 5
def radcap_dicap(orbit="",gsnode="", spincore="",spings="", spinexc="", plot=False):#, WF, WSP=[]  , Egs=0.0, maxEne=5.0, maxEneN=600):
    """
    Uses G.S.wavefunction GSWF.INP
    """
    spdf={
        "0s1":"    0.5   0 ",
        "0p3":"    1.5   1 ",
        "0p1":"    0.5   1 ", ###8
        "0d5":"    2.5   2 ",
        "1s1":"    0.5   0 ",
        "0d3":"    1.5   2 ", ###20
        "0f7":"    3.5   3 ", ###28
        "1p3":"    1.5   1 ",
        "0f5":"    2.5   3 ",
        "1p1":"    0.5   1 ", ##40
        "0g9":"    4.5   4 ", ##50
        "0g7":"    3.5   4 ",
        "1d5":"    2.5   2 ",
        "1d3":"    1.5   2 ",
        "2s1":"    0.5   0 ",
        "0h11":"   5.5   5 "
    }

    if orbit!="":
        if gsnode=="" or spincore=="" or spings=="" :
            print("!... changing orbit needs: orbit, gsnode(0), spincore(3/2),  spings(2),  (spinexc)")
            quit()
        else:
            print("D... GSnode={} spincode={} spings={}".format(gsnode,spincore,spings))
        nuphy_replace_orbit("DICAP.INP", orbit , spdf ,
                    "  "+str(gsnode)+"      "+str(spincore)+"     0.5      "+str(spings)+"   "+spdf[orbit]
                            )
    else:
        orbit=nuphy_get_orbit( "DICAP.INP", spdf)
        print("D... orbit G.S. found in INP:", orbit)

    try:
        os.rename("DICAP.TXT","DICAP.TXT.prev")
    except:
        print("D... no previous DICAP.TXT found")
    #================================================== RUN ===============
    radcap_run('5')

    plot_dicap()



#======================================================================== MAIN
#======================================================================== MAIN
#======================================================================== MAIN


if __name__ == "__main__":
    print("D... in main of project/module:  nuphy2/radcap ")
    print("D... version :", __version__ )
    Fire(  )
