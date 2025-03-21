#!/usr/bin/env python3

import scipy.integrate as integrate


################################
# i need interpolation now.... #
#https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html
import matplotlib.pyplot as plt

from scipy import interpolate
import scipy.interpolate # FOR isinstance()
#import scipy.interpolate
import numpy as np


import NuPhyPy.db.readnubase as db
import NuPhyPy.srim.srim as sr
import NuPhyPy.srim.sr as srin



def rrate( xs,  Nbeam,  NtargetS):
    """
    Nr = Nbeam * xs * Ntarget/S
    xs in barns
    Ntarget/S => calculate outside with Na /Mm * m/S ;  m/S == rho_S
    Ntarget/S=Na * n /S = Na * m/S  * Mm   ; where  mols= n=m/Mm
    Y = Nr/Nbeam = xs * NtargetS
    returns rrate  yield
    """
    sigma_cm2=xs*1E-24
    # creating isotope HERE
    #rho_S,just_rho,Mm_amu=get_thick_rho( args.material , args.thickness, args.density )
    ###print("D... material thickness=",  rho_S," mg/cm2")
    #rho_S = rho_S  /1e+3 # mg -> g/cm2
    Na=6.0221409E+23   #  Avogadro at/ mol   or 1e+26/kmol
    #print(Na)
    #Mm=Mm_amu    # molar weight -  isotopic should be:== Mm_amu

#    print("DEBUG... {:.3E}  {:.3E}  Na {:.3E}  {:.3E}  {:.3E}  ".format(Nb , rho_S ,Na ,Mm ,sigma) )
    #Nbpz=Nbp/Zin

    print("_"*30, "  rrate:", "_"*10)
    rrate=Nbeam * sigma_cm2 * NtargetS
    print("")
    print("Beam      {:10.4g} cps   ;    I={:.4g} puA".format( Nbeam , Nbeam*1.602176e-19*1e+6) )
    carb=NtargetS/Na*12/2.267
    wate=NtargetS/Na*18/1.000
    print("Ntarget/S {:10.4g} atoms ; if Carbon: d={:10.4g} cm ( {:10.4g} um )".format( NtargetS , carb, carb*10000) ) #carbon
    print("Ntarget/S {:10.4g} atoms ; if Water   d={:10.4g} cm ( {:10.4g} um )".format( NtargetS , wate, wate*10000) ) #h2o
    print("XS=   {:10.4g} mbarns    ;".format( xs*1000 ) )
    print("")
    print("Reaction rate: {:.4g} cps".format(rrate))
    print("Reaction rate: {:.4g} cps/sr".format(rrate/4/3.1415926 ))
    #if args.angle!=0:
    #    sr=float(args.angle)
    sr=6/180/180 # steradian
    print("Reaction rate: {:.4g} cps to {:.3g} Sr; [6mm2@18cm]  Sr(==S/r^2)".format( rrate/4/3.1415926*sr  ,sr ) )
    yieldc=NtargetS * sigma_cm2 
    print("Yield classic: {:.3g} %".format( yieldc*100 ) )
    if NtargetS * 1e-24 *100 >1:
        print("                  consider thick target calculation")
    print("Thin Coverage: {:.3g} %".format( NtargetS * 1e-24 *100  ) )
    print("_"*30)

    return rrate, yieldc

    




def get_yield_integrated( fix_cs , Nbeam,  dedx , Emax, Emin):
    ##############################
    #  integral function
    #
    #    def get_tcks(x): # get splined values for X #
    #        resu=interpolate.splev(x, tcks, der=0)
    #        return resu
    print("        energy integ.range:{} {}".format(Emax, Emin))
    beam_cps=1.123e+13 # 6.242e+14 # just 100uA
    Mm=25.9826      # gram/mol
    NA=6.022E+23    # atoms/mol
    Na=NA

    
    
    def get_tcks_inverse( e , xs=None): # get splined values for X #
        
        #resu=-1.0*1E+15  / interpolate.splev(x, tcks, der=0)
        #resu=-1.0*1E+15  / interpolate.splev(x, dedx, der=0)
        if e<min(dedx.x):
            e=min(dedx.x)
        if e>max(dedx.x):
            e=max(dedx.x)
        resu=-1.0* 1E+15  / (  dedx( e ) *1e-6 )  # I think MeV and MeV axes
        if not xs is None:
            xse=xs(e)*0.001 #  from  mb (TENDL) to barns
            if xse<0:xse=0
            resu=resu* xse #
            #print(e, xse)
        #print(e)
        return resu
    

    #print( dedx )
    #print( ".... dE/dx value at 1.0MeV" , dedx(1.10)  ,"  eV/10^15 atoms/cm2" )
    #print( ".... dx/dE value at 1.0MeV" , get_tcks_inverse(1.0) , "MeV/10^15 at/cm2" )
    
    # integration
    #result,dres = integrate.quad( get_tcks, Emax, Emin )
    #print("INTEGRAL== {:.3E} (dE/dx)".format( result ) )
    result,dres = integrate.quad( get_tcks_inverse, Emax, Emin )
    
    print(".... INTEGRAL==   {:.3E} dx/dE (not dependent on ev,MeV)".format( result ) )
    #print("_"*30)
    print("_"*30, "  yield integrated:", "_"*10)

    #print( "STR",type(fix_cs) ,isinstance(fix_cs,scipy.interpolate.interpolate.interp1d))
    
    if isinstance(fix_cs, scipy.interpolate.interp1d ):
        #print("i... TENDL integrated cross sections....")
        print("              TENDL integrated cross sections")
        result,dres = integrate.quad( get_tcks_inverse, Emax, Emin ,args=(fix_cs,) )
        Yield=  1E-24*result # target thickness is defined by energy loss

    else:
        print("      fixed cross section     ")
        Yield=fix_cs*1E-24   *result # target thickness is defined by energy loss
        print("XS=        {} mbarns".format( fix_cs*1000) )
    
    
    #print("\n")
    #print("INTEGRAL== {:.3E} ==part.conc/ (particle VOl density normaliz.)".format( part_vol_density_norm*result ) )
    print("Yield   ==   {:.4g} %".format( Yield*100 ) )
    print("YIELD   ==   {:.6g} ".format( Yield) )
    print("Beam         {:.4g} cps   ;    I={:.4g} puA".format( Nbeam , Nbeam*1.602176e-19*1e+6) )
    print("RRATE   ==   {:.6g} per second  ".format( beam_cps* Yield ) )
    day=beam_cps* Yield*3600*24
    molday=day/Na
    print("RRATE   ==   {:.6g} per day  {:.4g} mol/day".format( day, molday ) )
    print("_"*30)
    
    # tendays=beam_cps* Yield*3600*24*10
    # print("per 10 days= {:.6g}".format(tendays) )
    # print("Molar masss= {:.6g}; atoms per gram {:.3E}".format( Mm, NA/Mm) )
    # print("mass produced = {:8.4g} mg".format(tendays/NA*Mm *1000) )
    # print("                {:8.4g} ug".format(tendays/NA*Mm *1000000) )
    return Yield








if __name__ == "__main__":
    print("running yield.py as main")
    
    xs,Nbeam,Ntarget=0.1,  1.123e+13, 1.2e+21 
    rrate( xs, Nbeam, Ntarget )


    h1=db.isotope(1,1)  # incomming ion
    #h2=db.isotope(2,1)  # incomming ion
    TRIMIN,SRIN=sr.PrepSrimFile( ion=h1, energy=5.8, angle=0., number=100, mater='c', thick=13, dens=-11  )

    
    dedx,kevnum,mevmg=srin.run_sr_exe( SRIN )  # This returns loss tables BUT ALSO COEF!
    tcks=srin.srinterpolate( dedx , plot=False) # i take eV/ 10+15 atoms
    
    Emax,Emin = 18,17.414  #  100um  Carbon
    Emax,Emin = 8, 6.7537  #  105um  Carbon
    Emax,Emin = 4, 1.223   #  105um  Carbon
    
    get_yield_integrated( xs , Nbeam  ,tcks, Emax, Emin)


    
    
    xs,Nbeam,Ntarget=0.1,  1.123e+13, 2.515e+22 
    rrate( xs, Nbeam, Ntarget )

    h1=db.isotope(1,1)  # incomming ion
    #h2=db.isotope(2,1)  # incomming ion
    TRIMIN,SRIN=sr.PrepSrimFile( ion=h1, energy=5.8, angle=0., number=100, mater='c', thick=13, dens=-11  )

    
    dedx,kevnum,mevmg=srin.run_sr_exe( SRIN )  # This returns loss tables BUT ALSO COEF!
    tcks=srin.srinterpolate( dedx , plot=False) # i take eV/ 10+15 atoms
    
    Emax,Emin = 24,10.828  #   2.21mm   Carbon
    #Emax,Emin = 8, 6.7537  #  105um  Carbon
    #Emax,Emin = 4, 1.223   #  105um  Carbon
    
    get_yield_integrated( xs , Nbeam  ,tcks, Emax, Emin)
