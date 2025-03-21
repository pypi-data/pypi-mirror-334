#!/usr/bin/env python3
# -fire CLI
from fire import Fire
from nuphy2.version import __version__
from math import pow, sqrt, exp

from nuphy2.prj_utils import fail
from nuphy2.prj_utils import Bcolors
from nuphy2.prj_utils import super_print


#print("D... module nuphy2/rolfs is being run")

def func():
    print("D... function defined in nuphy2:rolfs")
    return True

def test_func():
    print("D... test function ... run pytest")
    assert func()==True

#-------------------------------------------------------



# used only in other expressions   #  r in [cm]
def CoulombPotential(Z1,Z2,r, debug=False):
    '''
    Z1 Z2/r  ...  units  keV cm
    '''
    global print
    print=super_print(debug)(print)

    print("D...  Z1*Z2*e^2 / R - in [keV] and [cm]")

    e2=1.44e-10;  #keV cm
    return 1.0/r *Z1 * Z2 *e2;


def test_CoulombPotential():
    print("12C + 12C at distance of 10-12cm = 10-14m... 5184 keV")
    assert CoulombPotential(6,6,1e-12)==5184.0

#-----------------------------------------------------------



# used in   CoulAZ / CoulombBarrier //  r0 in [cm]
def NuclearDistance(A1,Z1,A2,Z2, r0=1.3e-13, debug=False):
    '''
    sum of the two nuclear radii by A^1/3
    ...  units -  cm  if r0=1.3e-13 cm
    '''
    global print
    print=super_print(debug)(print)
    print("D...  r0 * A^1/3  + r0*A2^1/3 ;   units [cm]")
    return r0*pow(A1,0.3333) + r0*pow(A2,0.3333)


def test_NuclearDistance():
    print("Just a sum of radii :  in [cm] r0=1.3e-13cm ")
    assert NuclearDistance(12,6,12,6, r0=1.3e-13)==5.952021033637274e-13


#-----------------------------------------------------------



# Barrier in keV        r in [cm]
def CoulombBarrier(A1,Z1,A2,Z2, r0=1.3e-13, debug=False):
    '''
    Coulomb potential at a closest distance of two nuclei
    ... units  keV cm
    '''
    global print
    print=super_print(debug)(print)

    print("D... units are [keV] and [cm]")

    e2=1.44e-10;  #//keV cm
    #//  double k= 8.617343E-11; //MeV
    k= 8.617343E-8; # //keV
    #//  double r=pow(A1,0.3333)*r0 + pow(A2,0.3333)*r0 ;
    r=NuclearDistance(A1,Z1,A2,Z2, r0)
    #EC=1.0/r *Z1 * Z2 *e2
    EC=CoulombPotential(Z1,Z2,r)
    T=EC/k  # QUESTION: k or k 2/3 3/2 or so?
    #print('   {:.4g} keV,   {:.3f} T6'.format(EC, T/1e+6,'K' ) )
    return EC #; //in keV


# Barrier in keV        r in [cm]
def test_CoulombBarrier():
    print("CoulBarrier at touch:")
    assert CoulombBarrier(12,6,12,6 )==8709.646640532894

#-----------------------------------------------------------

def Sommerfield(A1,Z1,A2,Z2,Ecm_kev, debug=False):
    '''
    Sommerfield factor e^(-2 pi nu), depends on Z1Z2, Ecm and reduced mass
    just A1A2 here, not with mass excess
    ... units  Ecm in keV
    '''
    global print
    print=super_print(debug)(print)

    print("D... something like ? exp^(2*Pi*eta); eta ~? (Z1 Z2 / m/Ecm)")
    print("D... units [keV]")

    amu=A1*A2/(A1+A2)
    e2=1.44e-10   #  //keV cm//
    hbar=6.5821195e-16  #;   //  eV s
    hbarkev=hbar/1000.  #;   //  keV s
    #   double nu=Z1 * Z2* e2 /hbarkev/ v ;
    twopinu= 31.29 * Z1 * Z2  * sqrt(amu/Ecm_kev);
    # approximation at low energies, where E<< Ec
    P=exp(-1.0 * twopinu);
    print( '   2 Pi eta={}  P={:.4g} '.format(twopinu, P )  );
    return P

def test_Sommerfield():
    print("Sommerfeld: strangly small, rises to 0.001 @100MeV")
    assert Sommerfield(12,6,12,6,100)==1.476816227833165e-120
#-----------------------------------------------------------

def GamowEnergy(A1,Z1,A2,Z2,T6,Skevb, debug=False):
    '''
     effective mean energy
    ... temperature in T6
    ... rate is calculated based on S in keVb
    minimum star size - http://www-star.st-and.ac.uk/~kw25/teaching/stars/STRUC10.pdf
    R ~ M^13/18 (Kramers M^12.5/18.5)
    stackexchange: surface estTemp=5740∗mass0.54
    '''
    global print
    print=super_print(debug)(print)

    print("""               M_sun       T6
minimum star :   0.1      1.5
                 1      10-100      ( -He*)
                10      20-100-400  ( -He*-C*)
               100      25-125-500    -''-
maximum star :  50 (pressure instability)
maximum star : 120-200 Astrophysical Journal, vol. 162, p.947
Carbon burning: 600-1000 T6
Expl.Carbon   :1800-2500 T6
Oxygen burn   :1500-2700 T6
Expl. Oxygen  :3000-4000 T6
    Silicon burn  :2800-4100 T6 (with photodesintegrations)
Expl. Silicon :4000-5000 T6
""")
    #  T6 is temperature in T6 Kelvins
    #  AMU =   A1 * A2 / ( A1 + A2 )
    amu=A1*A2/(A1+A2)
    k= 8.617343E-8  #; //keV
    Eg=0.989*Z1*Z2*pow(amu,0.5)
    Eg=Eg*Eg # b^2  (4.18)
    #print(Eg)  # Gamow energy - exponential term b/E^1/2
    # (4.21) effective mean energy
    E0=1.22*pow( amu*T6*T6*Z1*Z1*Z2*Z2 ,0.3333)
    #  dimensionless tau:
    # Imax= exp(-tau)  .....  max value of the integrand
    # reactions with smallest CoulBar = highest Imax will be most rapid
    tau=42.46* pow( Z1*Z1*Z2*Z2*amu/T6, 0.33333)   # (4.23)
    Imax=exp(-1.0*tau)
    # gamow peak can be approximated by gaussian: sigma = delta (4.25)
    delta=0.749*pow( Z1*Z1*Z2*Z2*amu*pow(T6,5.0),0.33333/2.)
    # delta * Imax ~ approx value of the integral
    #
    #  consider gaussian shape of gamow; <sigma v> with tau from (4.23)
    # gives the rate when S(E0) is given keVb:  rate per particle pair
    rate=7.20e-19 /amu/Z1/Z2*tau*tau *exp(-1.0*tau)*Skevb
    #
    #  reaction rate can have a correction F(tau) Rolfs (4.31)
    #     it is like 3% for p+p or less

    # print(" kT={:5.3g} keV, E0={:6.3g} keV  delta/2={:6.3g} keV  Imax={:7.3g}   rate={:.3g} cm3/s".format(	k*T6*1e+6 ,E0, delta/2., Imax,  rate )   )    print(" kT={:5.3g} keV, E0={:6.3g} keV  delta/2={:6.3g} keV  Imax={:7.3g}   rate={:.3g} cm3/s".format(	k*T6*1e+6 ,E0, delta/2., Imax,  rate )   );

    print(" kT   ={:5.3g} keV,  E0={:6.3g} keV  delta/2={:6.3g} keV  Imax={:7.3g}".format(	k*T6*1e+6 ,E0, delta/2., Imax )   );
    print(" rate ={:5.3g} cm3/s  (at S={:g} keVb)".format(  rate, Skevb )   )


    # E0 is efffective mean energy for thermonucl reactions
    return E0


def test_GamowEnergy():
    print("13 mil.K, C+C fussion energy  --- @ 133 keV")
    assert GamowEnergy(12,6,12,6,13, 5 )==133.56833985657408


#-----------------------------------------------------------


if __name__=="__main__":
    print("D... in main of project/module:  nuphy2/rolfs ")
    print("D... version :", __version__ )
    Fire( {"GamowEnergy":     GamowEnergy,
           "Sommerfield":     Sommerfield,
           "CoulombBarrier":  CoulombBarrier,
           "NuclearDistance": NuclearDistance,
           "CoulombPotential":CoulombPotential
    })
