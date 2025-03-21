#!/usr/bin/env python3

import sys # print stderr

from fire import Fire
from nuphy2.version import __version__

########_DEBUG=0
from math import sin,cos,tan,pi,sqrt,asin,atan

# NEW SYSTEM
from nuphy2 import config

from nuphy2.prj_utils import fail
from nuphy2.prj_utils import Bcolors
#from nuphy2.prj_utils import super_print


import nuphy2.isotope as isotope
import nuphy2.rolfs as rolfs # Coul barrier here



def KREACT( op_amu,op_mex,ot_amu,ot_mex,oo_amu,oo_mex,oor_amu,oor_mex,
            TKE_=21.0, ExcT=0,theta=10.0,silent=0, output="all",
            coul= -1,
            nu3name=""):
    """
    This is the real calculation
    """

    TKE = TKE_
    TKE_UNIT = "mev" # lower()
    if type(TKE) == str:
        if TKE.lower().find("amev") == len(TKE) - 4:
            # Unit AMEV is solved in react() ... it never reaches this place
            if config.DEBUG: print("D...  units A*MeV ")
            TKE_UNIT = "amev"
            TKE = float(TKE[:-4]) * 0 # AMEV never reaches here
        elif TKE.lower().find("mevu") == len(TKE) - 4:
            if config.DEBUG: print("D...  units MeV/u ")
            TKE_UNIT = "mevu"
            TKE = float(TKE[:-4]) * op_amu # u * ENE
        elif TKE.lower().find("mev") == len(TKE) - 3:
            if config.DEBUG: print("D...  units MeV ")
            TKE_UNIT = "mev"
            TKE = float(TKE[:-3])
        else:
            if config.DEBUG: print("D... no unit given")
            TKE_UNIT = "mev"
            TKE = float(TKE)


    amu_unit = config.AMU_UNIT # 931.49403 I had an error????

    if TKE==0:
        print("X...  TKE is zero.... quit" ,  file=sys.stderr)
        sys.exit(0)
    #print( "D... TKE=",TKE )
    #my (  $exctgt, $amu1, $amu2, $amu3, $amu4, $Q )=@_;
    if config.DEBUG: print("******************************************* using mass excess ")
    if config.DEBUG: print(f"   D...op_mex ot_mex:  {op_mex}     {ot_mex}  "  )
    if config.DEBUG: print(f"   D...op_amu ot_amu:  {op_amu}     {ot_amu}  "  )

    # -------  this is used to calculate  threshold later on -------
    Q= op_mex+ot_mex - oo_mex - oor_mex # based on mex; notwrk4 e+e-  ; I need artificial mass e+e-
    #print(Q)
    #  they give the same .....  trr not problem from here
    Qamu=op_amu+ot_amu-oo_amu-oor_amu   # based on amu

    Q=Qamu*amu_unit*1000 # in keV # 8 DIGITS MAX....
    #print(Q)
    #
    # e+e- and gamma case tested on h2+h1 -> he3 + ...

    if config.DEBUG: print("DEBUG ... Q={}".format(Q) , file=sys.stderr);
    #if silent==0:
        #print()
        #print("--- {:3.1f} deg  TKE={:6.3f} MeV Q={:6.3f} MeV ------------".format(theta,TKE,Q/1000. ) ,
        #print("--- {:3.1f} deg  TKE={:6.3f} MeV --------------------------".format(theta,TKE) ,   file=sys.stderr )
    #rs;
    m1=op_amu* amu_unit
    m2=ot_amu* amu_unit

    m3=oo_amu* amu_unit
    m4=oor_amu* amu_unit

    #print(f"   i...     m1 m2: {m1:.5f}         {m2:.5f}  ")
    #print(f"   i...     m3 m4: {m3:.5f}         {m4:.5f}  ")
    Etot_proj = TKE + m1
    gamma_proj = Etot_proj / m1
    beta_proj = sqrt(1 - 1 / gamma_proj**2)

    print(f"{' ':12s}         proj.AMU:{op_amu:15.8f} ")
    print(f"{' ':12s}         targ.AMU:{ot_amu:15.8f} ")
    print(f"{' ':12s}         outg.AMU:{oo_amu:15.8f} ")
    print(f"{' ':12s}         rema.AMU:{oor_amu:15.8f} ")
    print(f"{' ':12s}   outg.theta.deg:{theta:12.5f} ")
    print(f"{' ':12s}         proj.TKE:{TKE:12.5f} ")
    print(f"{' ':12s}   proj.TKE.MeV/u:{TKE/op_amu:12.5f}  ")
    print(f"{' ':12s}        proj.Etot:{Etot_proj:12.5f} ")
    if config.DEBUG: print(f"D...               proj.gamma:{gamma_proj:12.5f} ")
    print(f"{' ':12s}        proj.beta:{beta_proj:12.5f}  {beta_proj*299.792:.2f}mm/ns  ")

    t=TKE  # projectile energy
    # adding excitation of target later

    if config.DEBUG: print("DEBUG...   AMUs (nudat): %f %f %f %f" % (m1,m2,m3,m4) , file=sys.stderr)

    # input channel masses + tke   /es/
    es=t + m1 + m2;

    ##### JAROCMS p1 good; E1 ^2=(t + m1)**2  ####   calculate p1, I believe earlier myself
    p1=sqrt(     (t + m1)**2  - m1**2  )

    ######### JAROCMS Ecms  from invariant # p3cform= sum p^2/2m
    Ecms2= (t + m1)**2   +  m2**2  + 2*(t + m1)*m2 - p1**2
    Ecms=sqrt( Ecms2 )
    TKEicms=Ecms-m1-m2 # not useful I think
    #    [1] M. Wang, G. Audi, A.H. Wapstra, F.G. Kondev, M. MacCormick, X. Xu and B. Pfeiffer, Chinese Physics C 36 (2012), P. 1603.
    #    [2] P. Moller, A.J. Sierk, T. Ichikawa, H. Sagawa. Atomic Data and Nuclear Data Tables 109-110 (2016), P. 1.
    #    [3] T. Tachibana, M. Uno, M. Yamada, S. Yamada, Atomic Data and Nuclear Data Tables 39 (1988) P. 251.
    #    [4] R. Bass, Nuclear Reactions with Heavy Ions, Springer-Verlag, NY, 1980, Chapter 7.4, pp. 318 - 340
    #    [5] J. Blocki, J. Randrup, W.J. Swiatecki, C.F. Tsang, Ann.Phys.(N.Y.), 1977, vol. 105, p. 427
    # simple situation for threshold, I used the M notation from  ***************** BASIC INFO ON REACTION ***************
    # https://makingphysicsclear.com/energy-threshold-for-creation-of-particles-in-relativistic-collisions/
    # where M==Sum(all m0 masses after reaction)
    M = m3 + m4
    #print(f"final state at threshold  Etot {M:.4f} MeV")
    TKEthrsh1 = (M * M - (m1 * m1 + m2 * m2) ) / 2 / m2 - m1# m2 is target  ... DIFFERS!!!!
    #   -- but it gave slightly different results....
    TKEthrsh = -(m1 + m2) / m2 * Q / 1000
    if TKEthrsh < 0:TKEthrsh = 0
    print(f"               reac.Ethrs_lab:{TKEthrsh:12.5f}")# ... TKEi of CMS={TKEicms:9.5f} MeV")
    # done earlier !Q= -1 * (m4 + m3 - m1 - m2)
    qtype = "exo"
    if Q <= 0:
        qtype = "endot"
    print(f"                       reac.Q:{Q/1000:12.5f}")
    print(f"        reac.CoulBarr_(Rolfs):{coul:12.5f} ")
    # ---SEE:     https://www.nndc.bnl.gov/qcalc/ *************** some 0.5 kev diff. @n15 10kev
    #h1 + c12:
    #  9B + α	-7552.4	9		8187.0	10
    #h2 + li6:
    #  2α	22372.77160	15		0
    #  7Li + p	5026.528	4		0
    #h1 + li7:
    #  6Li + d	-5026.528	5		5748.990	5

    if m4 == 0:
        #print(f"             ______________ fussion ______________")
        print(f"{' ':20s}  fussion:     1")
        #if _DEBUG!=0:  print("DEBUG... TKEcms=",TKEcms, file=sys.stderr)
        # Now I need to solve the problem of fussion:
        Excit = Q / 1000 + TKEicms
        Excit2 = Excit + ExcT
        spaces = 25 - len(nu3name)
        #formatted = f"{nu3name}:".ljust(22, ' ') + f"E*({nu3name}):{Excit:10.5}"
        #print(formatted)
        print(f"{' '*spaces}E*({nu3name}):{Excit:10.5} ")
        if ExcT != 0:
            print(f"{' ':25s} E**:{Excit2:10.5} MeV (when ExcT is included)")
        if Excit > 2 * 0.510999:
            Excit3 = Excit - 2 * 0.510999
            print(f"{' ':18s}  E*-(e+e-):{Excit3:10.5} ")

        return
        # *********************************** RETURN HERE *******************


    # theta is defacto theta3.
    costh3=cos( theta * 3.1415926535/180);
    sinth3=sin( theta * 3.1415926535/180);
    INVALID=0;

    if (ExcT>0.0):
        if config.DEBUG: print("DEBUG excitation=", ExcT,"MeV", file=sys.stderr)
    m4=m4 + ExcT #adding excitation of target HERE

    #nerelativ
    #    $m3=$m3 + $exctgt; #adding excitation of scattered particle HERE
    # my $SQne=sqrt( $m1*$m3*$t*$costh3**2 +($m1+$m2)*($m4*$Q+($m4-$m1)*$t)  );
    #    my $t3na=(sqrt($m1*$m3*t)*$costh3 + $SQne )**2 /($m1+$m2)**2;
    #    my $t3nb=(sqrt($m1*$m3*t)*$costh3 - $SQne )**2 /($m1+$m2)**2;
    #    print "Q=$Q ;  T3nerel = $t3na  $t3nb  \n";
    #-->>    print "           Q=$Q , p=$p1;  \n";
    #relativ
    a3b= es**2 - p1**2 + ( m3**2 - (m4)**2)
    #--- this is square root  from eq (4)  T3=.......
    # on fussion it is nonsense ....
    SQ= a3b**2 - 4*m3**2 * (es**2-p1**2*costh3**2)
    #    print  $a3b," ",$m3," ",$es,"  ",$p1,"  ",$costh3,"\n";
    #   print  $a3b**2,"    ", 4*$m3**2 * ($es**2-($p1**2)*($costh3**2) ),"\n";
    if ( SQ<0 ):
        #print(f"    SQ < 0  : {SQ:.5f}  : setting to           ##### ZERO ####")
        print(f"    SQ < 0  : ")
        SQ=0
        INVALID=1
        print(f"!... probably bellow threshold (for the angle {theta} deg)")
        #print(f"!... probably under threshold, quitting, Q=={m3-m1-m2}xxx")
        return

    SQ=sqrt( SQ ) # prepare for sqrt   <0
    ####### 2 SOLUTIONS ########
    t3a=( a3b * es + p1* costh3* SQ)/2/( es**2 - p1**2* costh3**2) - m3
    t3b=( a3b * es - p1* costh3* SQ)/2/( es**2 - p1**2* costh3**2) - m3
    ####### 2 SOLUTIONS ########
    if config.DEBUG:
        print("DEBUG...    kinetic E T3={} ({}) \n".format(t3a,t3b) ,
              file=sys.stderr);


    # prepare 2-solution's --- decision......
    # ----------- the following lines are separate ------- from the kinematics -----------------
    E1=t+m1 # full energy
    V=p1/( E1 + m2 ) # CMS velocity  pc/E->v/c?
    beta_cms =V;
    # ------------ THIS *** Threshold in LAB **** this is  DIFFERENT than with M above
    ttr=- ( m1 + m2)/ m2 * Q
    if (Q>0):
        ttr=0
    ttrc=-Q
    if (Q>0):
        ttrc=0
        if config.DEBUG:
            print("DEBUG...    E1={}  V={} t={} ttr={}\n".format( E1, V, t,ttr) ,
              file=sys.stderr);


    # equation   (21)  p3c CMS
    # !!!!!!!!!!  error in this line - use p3c defined later!!!!!
    #
    # 20171107 - i commentout
    #p3c= m2*sqrt( (t-ttr)*(t-ttr + 2/m2*m3*m4 )/( 2*m2*t + (m1+m2)**2)  )
    # varianta p3c: (19) and (20)
    Es=t + m1 +m2 # it is here alrady !@!!@!
    Esc= Es * sqrt( 1-V**2 )
    if config.DEBUG:  print('DEBUG ... Es,Esc',Es,Esc,  file=sys.stderr)
    #PROB  print "tot E= $Es  totEcms = $Esc   p3c= $p3c\n";
    p3c=sqrt( ( Esc**2-( m3+ m4)**2)*( Esc**2-( m3- m4)**2) )/2/Esc

    #    print( "Esc,m3,m4:",Esc, m3,m4 ,
    #     " @ Es,V,t,m1,m2",Es,V,t,m1,m2 ,  file=sys.stderr)
    #PROB  print "tot E= $Es  totEcms = $Esc   p3c= $p3c\n";

    E3c=sqrt( p3c**2 + m3**2 )

    #print("D.... p3c  E3c ",p3c, E3c)
    rho3=V/p3c * E3c
    #    mam-li  p3c  mam samozrejme i p4c :)
    #  ziskam E4c - bude dobre pro theta4
    p4c=p3c

    E4c=sqrt ( p4c**2 + m4**2 )
    # Q !!!! IN KEV !!!!!! from the database
    t4a= t- t3a + Q/1000; #rovnice (1) zzEne, nezavisle
    if config.DEBUG: print("... DEBUG: {}  {}  {}".format(t,t3a,Q)  , file=sys.stderr)
    t4b= t- t3b + Q/1000; #rovnice (1) zzEne, nezavisle


    #======================================================== THETA3
            #ziskej p3 (pozor na <0) klasicky ze znalosti p a t  [p3b]
    p3=    ( t3a +  m3)**2  -  m3**2  ;  # sqrt pozdeji...
    p4=    ( t4a +  m4)**2  -  m4**2  ;  # sqrt pozdeji...
    p4b=   ( t4b +  m4)**2  -  m4**2  ;  # sqrt pozdeji...i added 20180830
    p3b=   ( t3b +  m3)**2  -  m3**2  ;  # sqrt pozdeji...
    if (p3<0):
        print("    p3 <0:  $p3 : setting to ##### ZERO ####" ,  file=sys.stderr)
        p3=0.0
    p3=sqrt(  p3  )
    if (p3b<0):
        print("    p3b <0:  $p3b : setting to ##### ZERO ####" ,
              file=sys.stderr)
        p3b=0.0

    p3b=sqrt(  p3b  )
    # symetrically for p4: - it was missing in beta4
    if (p4<0):
        print("    p4 <0:  $p4 : setting to ##### ZERO ####" ,  file=sys.stderr)
        p4=0.0
    p4=sqrt(  p4  )
    if (p4b<0):
        print("    p4b <0:  $p4b : setting to ##### ZERO ####" ,
              file=sys.stderr)
        p4b=0.0

    p4b=sqrt(  p4b  )


    #    $p3b=42.85920142;
    # ziskej plnou informaci o  theta3cm - i sin i cos =>  theta3cm a
    #  a PI-theta3cm
    # equation (22) 2nd part
    sinth3cm = p3/ p3c* sinth3
    sinth3cmb= p3b/p3c* sinth3
    costh3cm=  ( p3*  costh3)/(1/sqrt(1-V**2))
    costh3cmb= ( p3b* costh3)/(1/sqrt(1-V**2))

    costh3cm= ( costh3cm -  V*E3c )/ p3c
    costh3cmb=( costh3cm -  V*E3c )/ p3c
    #tmpr2dc=R2dc
    #R2dc=1.0   ####  change default transofrmation..........

    th3cm = asin(  sinth3cm )*180/3.1415926
    th3cmb= asin(  sinth3cmb)*180/3.1415926
    if (costh3cm <0):
        th3cm =180-th3cm
    if (costh3cmb<0):
        th3cmb=180-th3cmb
    #-====================================================== THETA4
    th4cm =  180.0 - th3cm
    th4cmb=  180.0 - th3cmb
    #z eq (22)
    cotgth4 = 1/(sqrt(1-V**2)) *  ( p4c*cos( th4cm /180 * 3.1415926) + V*E4c  )
    cotgth4b= 1/(sqrt(1-V**2)) *  ( p4c*cos( th4cmb/180 * 3.1415926) + V*E4c  )
    tmpjmen =( p4c* sin( th4cm/180.0 * 3.1415926 )  )
    tmpjmenb=( p4c* sin( th4cmb/180.0 * 3.1415926 ) )
    #print("D... tmpjmenb:", tmpjmenb, p4c ,  file=sys.stderr )

    if ( tmpjmen ==0):
        print(" ?...   p4csin ==0::cotg is taken only approximate",
              file=sys.stderr)
        #print("o...   p4csin ==0:  $tmpjmen :cotg approx:
        #  setting to ##### ZERO ####")
        cotgth4=1e+7
    else:
        cotgth4= cotgth4/tmpjmen
    if ( tmpjmenb==0):
        print("o...    p4csinb ==0:::cotg approximate: \n", file=sys.stderr)
        #print("o...    p4csinb ==0:  $tmpjmenb :cotg approx:
        #     setting to ##### ZERO ####\n")
        cotgth4b=1e+7
    else:
        cotgth4b= cotgth4b/tmpjmenb

    #print("D... cotgh4=", cotgth4 ,  file=sys.stderr)

    theta4= atan( 1/ cotgth4 )*180/3.1415926
    if (theta4<0):
        theta4=180+theta4
    theta4b=atan( 1/ cotgth4b )*180/3.1415926
    if (theta4b<0):
        theta4b=180+theta4b


    # equation (32)  theta max
    #    print "doing sinmax\n";
    theta3max=180.0
    if (rho3>=1.00000):
        sinth3max=sqrt(  (1-V**2)/(rho3**2-V**2)  )
        theta3max=asin( sinth3max )*180/3.1415926
    else:
        theta3max=180.0
        t3b=0.0
        #R2dc=tmpr2dc  #put back translation deg2rad.......................

    # equation (30) for conversion sigma cm -> sigma lab (sCMS=K*sLab)
    #    my $convsig=($p3c/$p3) *
    #              sqrt( 1- (($rho3**2-$V**2)*$sinth3**2)/(1-$V**2)  );
    #    print "doing  k sigma  V=$V\n";
    #
    #   at 0 or 180 == p3c/p3
    convsig=  (( rho3**2-V**2)*sinth3**2)/(1-V**2)
    convsig=1.0 - convsig
    if (convsig>0 and p3>0):
        convsig=(p3c/p3)**2 * sqrt(  convsig )
    else:
        convsig=0.

    # b-variant
    convsigb=  ((rho3**2-V**2)*sinth3**2)/(1-V**2)
    convsigb=1.0 - convsigb
    if (convsigb>0 and p3b>0):
        convsigb=(p3c/p3b)**2 * sqrt(  convsigb )
    else:
        convsigb=0.


    #=====================  INVALIDATE ALL ====================
    if (INVALID==1):
        (th3cm,th4cm,theta4,t3a,t4a,th3cmb,th4cmb,theta4b,t3b,t4b)=(
            0,0,0,0,0,0,0,0,0,0 )

    p3cform=0 # case of gamma
    if config.DEBUG: print("DEBUG:  {}   {}  {}".format(m3,m4, p3cform) ,
                    file=sys.stderr)
    if (m3>0):
        p3cform=(p3c**2)/2/m3
    if config.DEBUG: print("DEBUG:  {}   {}  {}".format(m3,m4, p3cform) ,
                    file=sys.stderr)
    if (m4>0):
        p3cform=p3cform+(p4c**2)/2/m4
    if config.DEBUG: print("DEBUG:  {}   {}  {}".format(m3,m4, p3cform) ,
                    file=sys.stderr)

    #===== calculation to here:
    if not (rho3>1):
        th3cmb=0.
        th4cmb=0.
        t3b=0.
    #ttr/1000
    #ttrc/1000
    #Q/1000
    E3full=sqrt(p3**2 + m3**2 )
    gamma3=E3full/m3
    gamma1,beta1,beta3,gamma4,beta4=0,1,1,0,1
    Kscsl= convsig # factor
    Kscslb= convsigb # factor
    if gamma3>1:
        E1full=E1
        gamma1=E1full/m1
        beta1=sqrt( 1- (1/gamma1/gamma1) )
        #print("        beta1={:15.5f}    {:.1f}mm/ns".
        #format( beta1 , beta1*300 )   )

        beta3=sqrt( 1- (1/gamma3/gamma3) )
        #print("        beta3={:15.5f}    {:.1f}mm/ns".
        #format( beta3 , beta3*300 )   )

        E4full=sqrt(p4**2 + m4**2 )
        if m4==0:
            gamma4=0.
            beta4=1.
        else:
            gamma4=E4full/m4
            beta4=sqrt( 1- (1/gamma4/gamma4) )
            #print("    beta4={:15.5f}    {:.1f}mm/ns".
            #format( beta4 , beta4*300 )   )

    Q=Q/1000 # Q in MeV
    ttr=ttr/1000 #threshold lab in MeV
    ttrc=ttrc/1000 # threshold cms in MeV
    if (silent==0) and (output=="all"):
        ############################### PRINTOUT #####
        #        print(' ')
        #        print("        T1   =%15.5f  (projectile TKE)" % t )
        #         printf ("        th3MX=%15.5f\n",$theta3max );
        #print( "       th3  =%15.5f  (thetaMAX=%15.5f)"
        #    %  (theta,  theta3max)  )
        #        print("----------------------------------")

        print("        th3cm:%15.5f" % th3cm )
        print("        th4cm:%15.5f" % th4cm )
        print("          th4:%15.5f" % theta4 )
        print("          T3a:{:15.5f}       T3 {:15.5f}  ".format( t3a, t3b ) )
        print("          T4a:{:15.5f}       T4b{:15.5f}  ".format( t4a, t4b ) )
        print("        Kscsl:%15.5f (sigma_cms=Kscsl*sigma_lab)" % convsig )
        print("         rho3:%15.5f (if <=1.0 then 1 solution for T3; else 2)" %  rho3 )

        if (rho3>1.0 + 1e-6): # ARBIRARY epsilon!??!?!?!?!?!
            print("      b_th3cm:%15.5f" % th3cmb )
            print("      b_th4cm:%15.5f" % th4cmb )
            print("      b_th4__:%15.5f" % theta4b )
            print("      b_T3(b):%15.5f" % t3b)
            print("      b_T4(b):%15.5f" % t4b )
            print("      b_Kscsl:%15.5f sigma_cms=K*sigma_lab)" % convsigb )

        print("           p1:%15.5f (projectile momentum)" %  p1 )
        print("     beta_cms:%15.5f (velocity of CMS ... v/c)" % V )
        print(f"    gamma_cms:{1. / sqrt(1 - V * V):15.5f} " )
        print("          ttr:{:15.5f} (Threshold in Lab)".format(ttr) )
        print("         ttrc:{:15.5f} (Threshold in CMS == -Q)".format(ttrc) )
        print("            Q:{:15.5f} (if Q>0 = exoterm  [MeV])".format(Q) )
        print("         ExcT:%15.5f (input tgt excitation)" % ExcT )
        print("          p3c:%15.5f"  % p3c )
        print("          p4c:%15.5f"  % p4c )
        print(" TKEiCMS(1,2):%15.5f"  %  TKEicms )
        print(" EtotCMS(3,4):%15.5f"  %  p3cform )
        print("           p3:{:15.5f}     b  p3b  ={:15.5f}".format(p3,p3b) )
        print("           p4:{:15.5f}     b  p4b  ={:15.5f}".format(p4,p4b) )
        if gamma3>1:
            print("        beta3:{:15.5f}    {:.2f}mm/ns".format(
                beta3 , beta3*299.792 )   )
            print("        beta4:{:15.5f}    {:.2f}mm/ns".format(
                beta4 , beta4*299.792 )   )
        if (rho3>1):
            print("        t3a  :%15.5f   and  t3b  %f  (TKE)" % (t3a,t3b)  )
        else:
            print("      TKEout3:%15.5f  " % t3a )


    rs=t3a;
    #####################################################
    #
    # RETURN HERE ====================================
    #
    ##################################################

#    return t3a,t3b,th3cm,th3cmb,  p3cform  ,convsig
##################################
#  RETURN FROM REACTION
#       i need also TKE_CMS and ANGLE_CMS FOR RUTHERFORD
#          th3cm  ... OK
#          TKEcms ... OK   so it already is OK
#          0,1       2,3        4,     5
    if output!="all":
        #====== output can have  LIST from NOW ON
        output=output.split(',')
        if len(output)>1:
            print("H...  from bash-you can get the array vals: my_array=( $(<command>) )",
                  file=sys.stderr)
            print("H...      read with   echo  ${#my_array[@]}  ${my_array[0]}   ",
                  file=sys.stderr)
        print( output,"= ", file=sys.stderr )
        ret=""
        for i in output:
            try:
                ret+= str( locals()[i] ) +"\n"
            except:
                print("X... NO variable like",i)
                ret+="0\n"
        ret=ret.rstrip()
        #print( ret) # NO PRINT
        return ret  #=================================++ RETURN when not ALL
        print( locals()[output] )
        return locals()[output]
    #print("D...  old return")# old tpe return
    return t3a,t3b,th3cm,th3cmb,  TKEicms  ,convsig
    #print("   Kscsl=%15.5f (sigma_cms=K*sigma_lab)" % convsig )
    #print("b  Kscsl=%15.5f sigma_cms=K*sigma_lab)" % convsigb )

    # self.T3       =t3a
    # self.T3b      =t3b
    # self.Theta3   =theta
    # self.Theta3cms   =th3cm
    # self.Theta3cmsb  =th3cmb
    # #self.Theta3b   =thetab
    # self.Theta3max=theta3max
    # self.Theta4   =theta4
    # self.Theta4b  =theta4b
    # self.Ecms     =p3cform
    # self.Kscsl    =convsig
    # self.Kscslb   =convsigb
    # self.Q        =Q
    # self.Vc       =V


    # self.pd1_Ang=pd.DataFrame(
    #[ [theta, None, theta3max, th3cm, th3cmb ],
    #  [ theta4,  theta4b, None, th4cm, th4cmb ]  ],
    #     index=['part3 '+str(oo)+':','part4 '+str(oor)+':'],
    #     columns=[ 'Theta_LAB', 'Th_LAB_b','Th_LAB_max','Th_CMS','Th_CMS_b'] )
    # #print(self.pd1_ang)
    # #print(' ')

    # self.pd2_
    #Tke=pd.DataFrame( [ [ t, t3a, t3b, t4a,t4b  ]   ],  index=['Energies: '],
    #     columns=[ 'T1', 'T3_a', 'T3_b', 'T4_a','T4_b'] )
    # #print(self.pd2_T)
    # #print(' ')

    # self.pd3_Ene=pd.DataFrame(
    #[ [ Q, ttr, ttrc , p3cform , ot.Exc]   ],  index=['Energies: '],
    #     columns=[ 'Q','ThrLAB','ThrCMS', 'EtotCMS', 'ExcTgt'] )
    # #print(self.pd3_Ene)
    # #print(' ')

    # self.pd4_Ep=pd.DataFrame(
    #[ [E1, p1, None, None , None],[ None, p3, E3c, p3c , p3b ] ,
    #[ None, None, E4c, p4c , None ]  ],
    #     index=['part1 '+str(op)+':',
    #         'part3 '+str(oo)+':',
    #         'part4 '+str(oor)+':',
    #         ],
    #     columns=[ 'E_LAB', 'p_LAB','E_CMS','p_CMS' , 'p_b_CMS'] )

    # self.pd5_Trans=pd.DataFrame( [ [ convsig, convsigb, rho3, V ] ],
    #     index=['Conversions :' ],
    #     columns=[ 'XScms2lab', 'XScms2labb','rho3','Vcms' ] )

    #print "           try  http://t2.lanl.gov/data/qtool.html
    # for all possible reactions\n";






def test_KREACT(  ):

    res=KREACT( 3.01602931959, 14931.2155,
              15.9949146198, -4737.0013,
              3.01602931959, 14931.2155,
              15.9949146198, -4737.0013,
              TKE=24.96,
           theta=10.0  )
    assert res[0]==24.816736008366206
    res=KREACT( 1.008, 7288.97,
              15.9949146198, -4737.0013,
              1.008, 7288.97,
              15.9949146198, -4737.0013,
              TKE=1.175,
           theta=10.0  ) # beta==0.05 gamma 1.00125
    assert res[0]==1.1727507542732383





# ============================================================
#  this is called from nuphy.py
# ------------------------------------------------------------
#
# this needs NuPhyPy.db.ReadNubase.isotope library
def react( a,b,  c, d , TKE=1, theta=10, ExcT=0 , output="", silent=0, coul= -1, nu3name=""):
    """
    The last point where all A Z are present.  KREACT called from here
    """
    th3=theta
    if d is None:
            n4amu=0
            n4mex=0
            n4z,n4a=0,0
            #th3=0 # I DONT KNOW, MAYBE PHOTON TAKES SOME ENEERGY ag gamma4
            #silent=1  # ALL KINEM IS INCORRECT!!!!!!1
    else:
            n4amu=d.amu
            n4mex=d.mex
            n4z,n4a=d.Z,d.A
    zok=a.Z+b.Z-c.Z-n4z==0
    aok=a.A+b.A-c.A-n4a==0
    if not zok:
        print("Z sum incorrect:  particle 4 Z=",a.Z+b.Z-c.Z,"!=", d.Z)
        return [0,0,0,0,0,0,0,0] # why I added also here?
    if not aok:
        print("A sum incorrect:  particle 4 A=",a.A+b.A-c.A)
        return [0,0,0,0,0,0,0,0]
    if not zok:
        return [0,0,0,0,0,0,0,0]



    #print(  a.amu, a.mex, b.amu, b.mex, c.amu, c.mex, d.amu, d.mex ,"\n============")

    # ============================================================
    #   KREACT !!!!!!!!!!!!!!!!!!
    # ------------------------------------------------------------
    TKE2 = TKE
    # ----- UNIT AMEV HERE
    if type(TKE) == int:
        TKE_ = TKE
    elif TKE.lower().find("amev") == len(TKE) - 4:
        if config.DEBUG: print("D...  A*MeV ")
        TKE_UNIT = "amev"
        TKE2 = float(TKE[:-4]) * a.A

    res=KREACT( a.amu, a.mex, b.amu, b.mex,
                c.amu, c.mex, n4amu,n4mex,
                TKE_=TKE2, theta=th3, ExcT=ExcT,silent=silent,
                coul=coul, nu3name=nu3name)

    #return t3a,t3b,th3cm,th3cmb,  TKEcms  ,convsig
    if (output!="") and (not output is None):

        if output.lower()=="t3" or output.lower()=="t3a":
            res=res[0]
        if output.lower()=="t3b":
            res=res[1]
        if output.lower()=="tkecms":
            res=res[4]
        if output.lower()=="convsig":
            res=res[5]
    #print( output )
    if (output=="") or (output is None):
        return
    return res







# ============================================================
# PRINT C++ CODE ON THE SCREEN
# ------------------------------------------------------------

def printc_code():
    """
    Just print C++ code to calculate TKE3.  Compile simple with g++
    """
    code = """#include <iostream>
#include <cstdlib>
#include <cmath>

using namespace std;

double get_energy_tke3(double proj_amu, double targ_amu, double outg_amu, double rema_amu, double energy, double theta) {
  double pi = 3.1415926535;
  double Q;
  double amu_unit = 931.49410372;
  double m1, m2, m3, m4;
  double t = energy;
  m1 = proj_amu * amu_unit;
  m2 = targ_amu * amu_unit;
  m3 = outg_amu * amu_unit;
  m4 = rema_amu * amu_unit;

  Q  = proj_amu + targ_amu - outg_amu - rema_amu ;
  Q = Q*amu_unit;

  double  es=t + m1 + m2;
  double p1 = sqrt(    std::pow(t + m1, 2 )  - std::pow(m1, 2  ) );
  double costh3=cos( theta * pi/180.0);
  double a3b= std::pow(es, 2) - std::pow(p1, 2) + ( std::pow(m3, 2) - std::pow(m4, 2)  );
  double SQ = std::pow(a3b, 2) - 4*std::pow(m3, 2) * (  std::pow(es, 2) - std::pow(p1, 2) * std::pow(costh3, 2)  );
  if (SQ<0.0){
    return 0.0;
  }
  SQ = sqrt(SQ);
  double t3a = ( a3b * es + p1* costh3* SQ) /2.0/( std::pow(es, 2) - std::pow(p1, 2) * std::pow(costh3, 2) ) - m3;
  double t3b = ( a3b * es - p1* costh3* SQ) /2.0/( std::pow(es, 2) - std::pow(p1, 2) * std::pow(costh3, 2) ) - m3;
  double E1 = t + m1;
  double V = p1 / (E1 + m2);
  double Esc= es * sqrt( 1 - std::pow(V, 2) );
  double p3c=sqrt( ( std::pow(Esc, 2) - std::pow( m3+ m4, 2)) * ( std::pow(Esc, 2) - std::pow( m3- m4, 2) ) ) /2.0/Esc;
  double E3c = sqrt( std::pow(p3c, 2) + std::pow(m3, 2) );
  double rho3 = V / p3c * E3c;
  if ((rho3>1.0 + 1e-6) and (t3b>0.0)){ //  NOT SURE IF 1e-6 is OK
    cout << "!... 2 kinematics " << t3b << " " << endl;
  }
  return t3a;
}


int main(int argc, char* argv[]) {
    if (argc != 7) {
      cerr << "Usage: " << argv[0] << " proj_amu targ_amu outg_amu energy angle, arguments given==" << argc << endl;
      cerr <<" make clean && make && ./kinesample 1.00782503 12.0 4.00260325 9.01332966 10 15    " << endl;
      cerr << "make clean && make && ./kinesample 33.97857528 1.00782503 1.00782503 33.97857528 1360.00000 85 " << endl;
        return 1;
    }

    double proj_amu = atof(argv[1]);
    double targ_amu = atof(argv[2]);
    double outg_amu = atof(argv[3]);
    double rema_amu = atof(argv[4]);
    double energy = atof(argv[5]);
    double angle = atof(argv[6]);

    cerr << "Projectile AMU: " << proj_amu << endl;
    cerr << "Target AMU    : " << targ_amu << endl;
    cerr << "Outgoing AMU  : " << outg_amu << endl;
    cerr << "Remainin AMU  : " << rema_amu << endl;
    cerr << "Energy TKE MeV: " << energy << endl;
    cerr << "Angle    deg  : " << angle << endl;
    cerr << " - - - - - - - - - - - - - - - - - - - - - --" << endl;
    double result = get_energy_tke3(proj_amu, targ_amu, outg_amu, rema_amu, energy, angle);
    cout << angle << " " << result << endl;
    return 0;
}
"""
    print(code)






# ============================================================
#   MAIN **********************
# ------------------------------------------------------------
#
# i need i,o, e, angle..... NOT excitation
def main( inpart="", outpart="" , energy="", angle="", xcitation=0, f=None, debug=False):
    """
    KINEMATICS MODULE:
    -i: h2,o16    ... projectile,target
    -a: 15        ... angle of reaction
    -x: 0         ... (target) excitation energy in MeV
    -e: 10AMeV  MeVu or just MeV Total Kinetic Energy
    -f: t3a,a.txt ... output variable,file
                     variable can be: t3,t3a,t3b,tkecms,convsig,all
    """
    #global print
    #print=super_print(debug)(print)
    config.DEBUG = debug
    #===================================== digest the parameters ======
    if inpart!="":
        if config.DEBUG: print("D... type of i", type(inpart) )
        if type(inpart) is tuple: # sometimes tuple, sometimes str???
            if config.DEBUG: print("D... tuple")
            in1=inpart[0]
            in2=inpart[1]
        elif type(i) is list:
            if config.DEBUG: print("D... list")
            in1=inpart[0]
            in2=inpart[1]
        else:
            if config.DEBUG: print("D... string", i)
            inc1=inpart.split(",")[0]
            in2=inpart.split(",")[1]
        if config.DEBUG: print("D... creating isotopes ... ", in1, in2)
        nu1=isotope.create( in1 , debug=debug)
        nu2=isotope.create( in2  , debug=debug )
    if outpart!="":
        # this seems to allow for no output3??? NO, later error!
        nu3=isotope.create( outpart  , debug=debug)


    #=========================================== MODES ===========================react
    if 0==0:
        if inpart == "":
            print(main.__doc__)
            fail(Bcolors.WARNING+"?... give me projectile,target  -i h2,o15" + Bcolors.ENDC )
        if outpart == "": fail(Bcolors.WARNING+"?... give me outgoing           -o h1" + Bcolors.ENDC )
        if energy == "": fail(Bcolors.WARNING+"?... give me energy of the reaction in MeV -e 5.8" + Bcolors.ENDC )
        if angle == "": fail(Bcolors.WARNING+"?... give me angle of the reaction -a 15" + Bcolors.ENDC )
#        if t == "": fail(Bcolors.WARNING+"?... give me target thickness   -t 10ug -t 10um" + Bcolors.ENDC )
        # if f == "": fail(Bcolors.WARNING+"?... give me value,outfile      -f t3a  -f t3a,a.txt" + Bcolors.ENDC )
        # -S a,T3 ... save to textfile the value
        #
        #
        print()
        if config.DEBUG: print(Bcolors.OKGREEN + "D... PROJECTILE   :", in1 + Bcolors.ENDC )
        if nu1 is not None: nu1.pprint()
        if config.DEBUG: print( Bcolors.OKGREEN +  "D... E=           :", energy,"  (MeV if not said different)" )
        if config.DEBUG: print( Bcolors.OKGREEN +  "D... TARGET       :", in2 + Bcolors.ENDC )

        if nu2 is not None:         nu2.pprint()

        # print( Bcolors.OKGREEN +  "D... Thickness   =:", t )
        if config.DEBUG: print( Bcolors.OKGREEN +  "D... OUTGOING 1   :" , outpart+ Bcolors.ENDC)

        if nu3 is not None:         nu3.pprint()

        if config.DEBUG: print( Bcolors.BOLD +  "D... Angle       =:", str(angle) + Bcolors.ENDC)
        if config.DEBUG: print( Bcolors.BOLD +  "D... Excitation  =:", xcitation,"MeV"+ Bcolors.ENDC )
        if config.DEBUG: print( Bcolors.BOLD +  "D... Outputfile,V=:", "None"+ Bcolors.ENDC )
        #react( a,b,  c,d, TKE=1, theta=10, ExcT=0 , silent=0):
        #res=kin.react( nu1,nu2,nu3,nu4, TKE=TKE, ExcT=excitation, theta=th,silent=1)

        coul=rolfs.CoulombBarrier( nu1.A, nu1.Z, nu2.A, nu2.Z )
        if config.DEBUG: print(Bcolors.OKGREEN + "D... Coulomb (Rolfs) =: {:.3f} MeV".format( coul/1000)+ Bcolors.ENDC )
        coulrolfs = coul/1000;

        #  for gamma or e+e- there was some option!?!?!
        nu4=isotope.create( nu1.A +  nu2.A - nu3.A, nu1.Z +  nu2.Z - nu3.Z  , debug=debug)
        # When this is None????

        if (nu4 is None) or (nu4.A == 0 and nu4.Z <  0):#is None:
            sys.exit()
        if nu4.A == 0 and nu4.Z == 0:#is None:
            #
            # NO particle 4 ?????? FUSSION   -o compoundNucleus
            #
            if config.DEBUG:print(Bcolors.WARNING+"Cannot calculate 2nd outgoing: fussion instead:"+ Bcolors.ENDC )
            Q= (nu1.mex+nu2.mex-nu3.mex)/1000
            #print("Q(gs2gs)= {:10.4f} MeV".format( Q  ) ) # same as q
            if config.DEBUG:print("D... E*({})~ {:10.4f} MeV + TKECMS (not Etot_CMS)!!!".format( nu3.name, Q  ) )

            # ********************************************   -o compoundNucleus
            #done beforenu4=isotope.create( 0, 0 , debug=True) # see 0 0
            #print("... exciton:", nu4)
            #nu4=isotope.create( 0, 0 , debug=debug)

            res=react( nu1,nu2,nu3,nu4, TKE=energy, ExcT=xcitation, theta=angle,silent=0, coul=coulrolfs, nu3name=nu3.name)

            #res=kinematics._REACT( nu1.amu, nu1.mex, nu2.amu, nu2.mex,
            #            nu3.amu, nu3.mex, nu4amu,  nu4mex,
            #                       TKE=e, theta=a, ExcT=x, silent=False)
            #res=kinematics._REACT( nu1.amu, nu1.mex, nu2.amu, nu2.mex,
            #            nu3.amu, nu3.mex, nu4amu,  nu4mex,
            #                       TKE=e, theta=a, ExcT=x, silent=False)
            if not res is None:
                EXC=res[4]+Q
                print(Bcolors.OKGREEN+ "E*({}) = {:.3f} MeV".format( nu3.name, EXC)+ Bcolors.ENDC  )
                if config.DEBUG: print(Bcolors.WARNING+"D... needs to be verified"+ Bcolors.ENDC )
            else:
                if config.DEBUG: print(Bcolors.WARNING+"D... impossible reaction"+ Bcolors.ENDC )

        else:
            # WHY THIS??
            if config.DEBUG: print(Bcolors.OKGREEN +   "D... OUTGIONG 2   :" + Bcolors.ENDC )
            if config.DEBUG: nu4.pprint()
            if config.DEBUG: print(Bcolors.OKGREEN +   "D... KINEMATICS   :" + Bcolors.ENDC )
            outfile = ""
            if isinstance(f,tuple):
                outfile=f[1]
                f=f[0]

            # ********************************************
            res=react( nu1,nu2,nu3,nu4, TKE=energy, ExcT=xcitation, theta=angle ,output=f,silent=0, coul=coulrolfs, nu3name=nu3.name)

            if outfile!="":
                with open(outfile,"a") as fil:
                    fil.write(str(res)+"\n")
            #res=kinematics._REACT( nu1.amu, nu1.mex, nu2.amu, nu2.mex,
            #            nu3.amu, nu3.mex, nu4.amu,  nu4.mex,
            #                       TKE=e, theta=a, ExcT=x, silent=True)

            if not f is None:
                print(res,file=sys.stdout)




#print("i... module  kinematics  is being loaded", file=sys.stderr)
if __name__ == "__main__":
    #print("D... in main of project/module:  nuphy2/kinematics ")
    #print("D... version :", __version__ )
    #Fire( printc_code )
    Fire( main )
