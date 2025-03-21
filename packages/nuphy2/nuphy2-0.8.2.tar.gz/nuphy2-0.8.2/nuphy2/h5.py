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
import nuphy2.isotope as isotope
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
#------------------------------------ things for h5
import matplotlib.cm as cm #  colors for h5

from scipy.optimize import curve_fit # fir gauss Eremnant
from scipy.stats import norm         # norm distribution 4 fit



    ###############################################################  STORE
    #
    #   (UN) store  and   plot
    #
    #####################################
    # graph: help:  x,y,z,yz,xz,xy,cos==cosyz cosy cosz cosx  list==view, dee , e
def main(Store="", graph="", printvar="all" ,randomize_yz=0., fwhm=0,  savefig="", debug=False):
    """
    H5 DRAW SRIM:
    Parameters file[,set1,...|all]  [e,x,y,z,cos,view,dee]  [all,none]
    """
    global print
    print=super_print(debug)(print)

    if Store=="":
        files=glob.glob("*.h5")
        for i in files:
            print("i... GLOBBED FILE=",i)
            main(i)
        sys.exit(0)


    stor=Store.split(',')   # stor list = 0,1,2,3,4,5
    print("D... ####",stor)


    if graph!="" and len(stor)==1:
        print("X... you need to put  {},all; I DO IT ", stor[0] )
        stor.append('all')


    seznam=[]      # this is some di9rty trick to plot "before"
    seznamname=[]  # i will zip it with seznam
    colorfiles=[]  # color to files
    #
    # jaka je myslenka? appendnout i fily?
    #
    nfiles=0 # first file we wait to open
    pd_file=None
    #
    # IDEA: create seznam of  DATA ! (pandas)
    #
    if (len(stor)>1) and (graph==""):  #  plots was not asked, but set is demanded
        graph="view"

    if (len(stor)>1) and (graph!=""):  #  plots were asked
        print("D... multiple elements with file, plots were asked",len(stor), stor)
        # # EXTRA CASES: ALL
        # if stor[0]=='all':
        #     ##del( stor[1])
        #     for i,v in enumerate(sorted(pd_file.keys())):
        #         seznam.append(i)
        #     #print( "D...",seznam )
        # EXTRA CASES: 0-7 ########
        for i in stor: # command
            print("D... next store key==","/{}/ of {}".format(i,len(stor)) ) ### FILE AND HAS A .
            #if (os.path.isfile( i )) and (i.find('.')>0):
            if (os.path.isfile( i )) :
                print("D... isfile YES:", i , file=sys.stderr )
                pd_file = pd.HDFStore( i )
                print("D... detected filename shoud be open now:",i  , file=sys.stderr )
                nfiles+=1  # increment counter, color
            elif i=="all":
                print("D... all keyword detected:", i , file=sys.stderr )
                for i,v in enumerate(sorted(pd_file.keys())):
                    print("   D... appending:", i,v , file=sys.stderr )
                    seznam.append( pd_file[v] )
                    seznamname.append( v )
                    colorfiles.append( nfiles ) # every key I append the "nfiles"=> each file has a color

            else:
                print("D... one keyword is:", i)
                ran=i.split("-")
                if len(ran)>1:
                    for j in range(int(ran[0]),int(ran[1])+1):
                        keyname=pd_file.keys()[int(j)]
                        seznam.append( pd_file[keyname] )  # append df
                        seznamname.append( keyname )
                        colorfiles.append( nfiles ) # every key I append the "nfiles"=> each file has a color

                    print("D...appended dashed list...",seznam , file=sys.stderr )
                elif len(ran)==1:
                    #if not(pd_file) in locals():
                    if pd_file is None:
                        print("X... NO FILE OPENED (is None)", i , file=sys.stderr )
                        quit()
                    else:
                        #print(i, pd_file.keys()[0] )
                        keyname=pd_file.keys()[ int(i) ]
                        seznam.append( pd_file[ keyname ] )
                        seznamname.append( keyname )
                        colorfiles.append( nfiles ) # every key I append the "nfiles"=> each file has a color
                        #print("D... appended single number...",seznam )
                        #print("D... ")

        ######################################################
        #print(seznam)
        if seznam==[]:
            # list only
            print("\n",file=sys.stderr)
            for i in pd_file.keys():
                print(  i, file=sys.stderr )
            print("\n",file=sys.stderr)
            quit()



        #==========seznam is CREATED==================================
        #print("D... =================================== plot section:" , file=sys.stderr )
        #print("D... =================================== plot section:" , file=sys.stderr )
        #print("D... =================================== plot section:" , file=sys.stderr )
        IMPLANT=False # it was crashing
        plots=[]
        fig=plt.figure( figsize=(12,6))
        ax=fig.add_subplot(111)
        #========= i want to plot dE histogram with convolution fwhm
        plotme=False
        if nfiles>1:
            #print(nfiles," +1 ... more Files ============================== x colors " , file=sys.stderr )
            colors = cm.rainbow(np.linspace(0, 1, nfiles+1 ))
            print("DCOL...", colors)
            print("DCOL... file number:", colorfiles)
            # colorfiles ==== number of file
            colorfiles=[ colors[i] for i in colorfiles ] # i change the 0,1,2 for colors
            colors=colorfiles
            print("DCOL...", colors)
        else:
            #print(len(seznam)," +2 ... one File-colors ============================== x colors " , file=sys.stderr )
            colors = cm.rainbow(np.linspace(0, 1, len(seznam)+2 )) # one filename always
        print("D... LENCOLORS=",len(colors)," colors=", colors , "\n"  )
        #colorfiles HERE TODO
        #if nfiles==1:
        #colors=colors[1:]

        #hot = plt.get_cmap('hot')
        #cNorm  = colors.Normalize(vmin=0, vmax=len(uniq))
        #scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=hot)
        ######colors=['k','r','b','g','y','m'] # every file diff color





        #print("D.... parse ZIP", file=sys.stderr)
        #============================================= PLOT LOOP ==========START
        # do here, later it wouldbe mess
        xdivkov = 1
        xunit = "um"

        for df,dfname in zip(seznam,seznamname):
            print("____________", dfname[:80])
            print("D...  ******:", dfname    )
            print("D... ", df    )
            #print(df, len(df))
            # print( "DFNAME  inx=",  inx, "  seznam[inx]=",seznam[inx]  , file=sys.stderr )
            # dfname=sorted(pd_file.keys())[ int(seznam[inx]) ]

            # print('o... openning: ', dfname ,"  with -g = /", args.graph,"/"  ,
            #       "  with -p = /", args.printvar,"/"  ,
            #       file=sys.stderr )
            # # dataframe: get it
            # df=pd_file[dfname]
            # #==================
            # # here i can do fit?
            # =============================== DECIDE ON WHAT IS THERE
            IMPLANT=False
            PASSTHROUGH=False
            # i can have combined dfs ---------------------
            #e=df[ df['e'].notnull() ]['e'] #
            #x=df[ df['x'].notnull() ]['x'] # always nonnull
            if  'e' in df.keys() and len( df[ df['e'].notnull() ]['e']  ) > 0: # e is always there?
                #print("$$$ PASS", len(e))
                e=df[ df['e'].notnull() ]['e']
                #print("E",e)
                PASSTHROUGH=True
                ni=dfname.split("_n")[1].split("_ei")[0].replace("_",".")
                ni=int(ni)

                dfzeroe = df[ df['e'] <  1e-4]
                if len(dfzeroe) > 0:
                    print("$$$ $$$ IMPLANT")
                    #print(df)
                    #print(df[ df['e'] == 0 ])
                    #sys.exit(0)
                    print("X... problem with number of points",len(e),"vs N=",ni)
                    IMPLANT=True
                    depth=df[ df['x'].notnull() ]['x']
                    #print("X",depth)
                    print("X... x data length==",len(depth) )
            elif len(df) > 0:# 'x' in df.keys() and len(x) > 0:
                print("$$$ IMPLANT    ", len(df))
                print("D... SETTING THE ENERGY TO fake ZERO BEGIN"   )
                IMPLANT=True
                df['e']=1e-6+0*df['x']
                #print(df)
                e=df['e']
                depth=df[ df['x'].notnull() ]['x']
            else:
                print("S$$ BROKEN PASS and IMPLANT")
                print(df)
                sys.exit(0)
                #print("XX",depth)

                #print("X... SETTING THE ENERGY TO fake ZERO END"  , file=sys.stderr )






            #print("D... SUDDENLY PRINTING GREY    before")

            nbins = 20

            #n, bins, patches = plt.hist(e,nbins, density=True,facecolor = 'grey', alpha = 0.5, label='before')
            #if PASSTHROUGH:
            #if IMPLANT:
            #plt.cla()
            #print(pars)
            #print(cov)
            #
            #######################  PRINT OUT LOSSES AND MEANS.....
            #

            if (printvar=="all"):
                if PASSTHROUGH:
                    n, bins = np.histogram(e,nbins, density=True)
                    centers = (0.5*(bins[1:]+bins[:-1]))
                    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), centers, n, p0=[e.mean(),e.std()])
                    print("D... energy  e ",pars )
                    #print("________________________________________________")
                    #print("# use  -p help    for options")
                    print("   Emean {:9.5f}           sigma {:8.5f}  ".format(e.mean(),e.std()))
                    print("   E_FIT={:9.5f} {:8.5f}  sigma={:8.5f} {:6.5f}".format(
                        pars[0],  math.sqrt(cov[0,0]) ,
                        e.std() , math.sqrt(cov[1,1]) ) ) # FIT ...........
                    print("   Emin= {:9.5f}           Emax= {:8.5f}  ".format(e.min(),e.max()))
                    # ------------- statistics end
                if IMPLANT:
                    n, bins = np.histogram(depth,nbins, density=True)
                    centers = (0.5*(bins[1:]+bins[:-1]))
                    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), centers, n, p0=[depth.mean(),depth.std()])
                    print("D... implant x ",pars)
                    print("   Xmean {:9.5f}           sigma {:8.5f}  ".format(depth.mean(),depth.std()))
                    print("   X_FIT={:9.5f} {:8.5f}  sigma={:8.5f} {:6.5f}".format(
                        pars[0],  math.sqrt(cov[0,0]) ,
                        depth.std() , math.sqrt(cov[1,1]) ) )
                    print("   Xmin= {:9.5f}           Xmax= {:8.5f}  ".format(depth.min(),depth.max()))

            if (printvar=="help"):
                print("HELP...  basic description:  -p emean,estd (straggling sigma), emedian ")
                print("HELP...  basic description:  -p eini, einistd (should be 0?) ")
                print("HELP...  fitted values    :  -p efit, eerr(mean error),esigma(sigma error)")
                print("HELP...  x and de         :  -p xmean, xstd,  de (losses), destd (sigma of losses)")
                print("HELP...  plain data       :  -p data_e (remaining energies),  data_yz (two columns y z)")
                # easiest fit # (mu, sigma) = norm.fit( e ) # fills histogram
            elif printvar=="none":
                print()
            else:
                plist=printvar.split(",")
                for p in plist:
                    print("D... printing:", p)
                    #=========  e was specially defined.... =======
                    if p.lower()=="data_e":
                        # print all rows and dont print index nor header nor footer
                        pd.set_option('display.max_rows', None)
                        print( e.to_string(header=None,index=None) ) # no Name, DTYPE
                    if p.lower()=="data_yz":
                        # print all rows and dont print index nor header nor footer
                        pd.set_option('display.max_rows', None)
                        print( df[ ['y','z'] ].to_string(header=None,index=None) ) # no Name, DTYPE

                    if p.lower()=="emean" or p.lower()=="e" :
                        print( e.mean() )
                    if p.lower()=="emedian" :
                        print( e.median() )
                    if p.lower()=="estd":
                        print( e.std() )

                    if p.lower()=="de" :
                        print( df['eini'].mean() - e.mean() )
                    if p.lower()=="destd" :
                        print( math.sqrt( df['eini'].std()*df['eini'].std()  + e.std()*e.std() ) )

                    if p.lower()=="eini" :
                        print( df['eini'].mean() )
                    if p.lower()=="einistd" :
                        print( df['eini'].std() )

                    if p.lower()=="efit":
                        print( pars[0] )
                    if p.lower()=="eerr":
                        print(  math.sqrt(cov[0,0])  )
                    if p.lower()=="esigma":
                        print( math.sqrt(cov[1,1]) )

                    if p.lower()=="xmean" or p.lower()=="x":
                        print( df['x'].mean() )
                    if p.lower()=="xstd":
                        print( df['x'].std() )
                    #if p.lower()=="xstd":
                    #    print( df['x'].std() )
                    # and we can continue

                print("D.... printed:", plist)




            #==================  if fwhm .... CONVOLUTE;
            #       yz ... scatter;  cosy cosz ...angles
            print("D... GRAPH section:", graph)
            if graph=="help": #=======
                print("--graph:  x y z yz xz xy cos ==cosyz cosy cosz cosx dee  view ==list")

            if graph=="x": #======= implantation plot
                print("D... graphing  ",graph)

                if max(df['x']) > 10000:
                    xdivkov = 1000
                    xunit = "mm"

                ax.set_xlim(0, max(df['x']) / xdivkov)  # Set x-limits to determine graph size
                n, bins, patches = ax.hist( df['x'] / xdivkov, 20, alpha=0.3,label=dfname, color=list(colors[0]) )
                # Calculate bar width as 2% of x-axis size
                xlim = ax.get_xlim()

                FUN = True
                if FUN:
                    bar_width = 0.01 * (xlim[1] - xlim[0])  # 2% of the x-axis size
                    ### Update the width of each bar
                    for patch in patches:
                        patch.set_width(bar_width)

                colors=colors[1:] #  remove the first color
                plotme=True
                ax.set_xlabel(f"x implant [{xunit}]")

            if graph=="y": #======= implantation plot
                print("D... graphing  ",graph)
                ax.hist( df['y'], bins=20, ec='k',alpha=0.3,label=dfname)
                plotme=True
                ax.set_xlabel("y implant [um]")

            if graph=="z": #======= implantation plot
                print("D... graphing  ",graph)
                ax.hist( df['z'], 20, ec='k',alpha=0.3,label=dfname)
                plotme=True
                ax.set_xlabel("z implant [um]")

                #ax.scatter( df['z']/1e+4, df['y']/1e+4,alpha=0.3,label=dfname+' [um]' )
            if graph=="yz": #======= scatter plot  Y Z
                print("D... graphing  ",graph)
                if float(randomize_yz)>0.:
                    df['zybar1']=np.random.normal( -float(randomize_yz)/2, float(randomize_yz)/2 ,  len(df) )
                    df['zybar2']=np.random.normal( -float(randomize_yz)/2, float(randomize_yz)/2 ,  len(df) )
                    df['z']=df['z']+df['zybar1']
                    df['y']=df['y']+df['zybar2']
                ax.scatter( df['z'], 7*df['y'], marker=".",alpha=0.3,label=dfname )
                ax.set_xlabel("z implant [um]") #ok x==z scat(z,y)
                ax.set_ylabel("y implant [um]") #ok y==y
                plotme=True

            if graph=="xz": #======= scatter plot  Y Z
                print("D... graphing  ",graph)
                ax.scatter( df['z'], 7*df['x'], marker=".",alpha=0.3,label=dfname )
                ax.set_xlabel("z implant [um]") #ok x==z scat(z,y)
                ax.set_ylabel("x implant [um]") #ok
                plotme=True

            if graph=="xy": #======= scatter plot  Y Z
                print("D... graphing  ",graph)
                ax.scatter( df['y'], 7*df['x'], marker=".",alpha=0.3,label=dfname )
                ax.set_xlabel("y implant [um]") #ok x==z scat(z,y)
                ax.set_ylabel("x implant [um]") #ok
                plotme=True

            #=============================================================== COS
            if IMPLANT and graph.find("cos")>=0:
                print("X... gonna crash now, implants do not have COS....")
            if (graph=="cos") or (graph=="cosyz")  : #======= scatter plot cosy
                print("D... graphing  ",graph)
                if  not IMPLANT:
                    ax.scatter( (np.pi/2-np.arccos(df['cosz'].astype(np.float64))),
                                (np.pi/2-np.arccos(df['cosy'].astype(np.float64))),
                                alpha=0.3, label=dfname )
                    ax.set_xlabel("acosz [rad]") #ok x==z scat(z,y)
                    ax.set_ylabel("acosy [rad]") #ok y==y

                    plotme=True
                else:
                    print("!... no cos in implantation...")

            if graph=="cosy" : #======= plot cosy
                print("D... graphing  ",graph)
                if  not IMPLANT:
                    ax.hist( df['cosy'], 20, ec='k',alpha=0.3,label=dfname)
                    ax.set_xlabel("cosy ") #ok x==z scat(z,y)

                    plotme=True
                else:
                    print("!... no cos in implantation...")

            if graph=="cosz" : #======= plot cosz
                print("D... graphing  ",graph)
                if  not IMPLANT:
                    ax.hist( df['cosz'], 20, ec='k',alpha=0.3,label=dfname)
                    ax.set_xlabel("cosz ") #ok x==z scat(z,y)

                    plotme=True
                else:
                    print("!... no cos in implantation...")

            if graph=="cosx" : #======= plot cosx
                print("D... graphing  ",graph)
                if  not IMPLANT:
                    ax.hist( df['cosx'], 20, ec='k',alpha=0.3,label=dfname)
                    ax.set_xlabel("cosx ") #ok x==z scat(z,y)
                    plotme=True
                else:
                    print("!... no cos in implantation...")


                    #                if graph=="cosz" and  'e' in df.keys(): #======= scatter plot cosy cosz
                    #                    if  'e' in df.keys():
                    #                        ax.hist( df['cosz'], 20, ec='k',alpha=0.3,label=dfname+' implant [rad]')
                    #                        ax.set_xlabel("cosz [rad]") #ok x==z scat(z,y)
                    #                        plotme=True
                    #                    else:
                    #                        print("!... no cos in impplantanion")



            ###### test de x e ##############
            #if args.graph=="dee" and  'e' in df.keys(): #======= dE  vs  E
            #
            # i want to draw  Y: loss   X: total E
            #
            # ----------------------------------------  dee-----START--
            if graph=="dee": #======= dE  vs  E
                print("D... graphing  ",graph)
                # de x e   , i need to know e
                if  IMPLANT:# IF IMPLANT: SET E(remaining)=0
                    print("D... IMmplant: settnig E==0")
                    df['e']=df['x']*0
                #
                ni=dfname.split("_n")[1].split("_ei")[0].replace("_",".")
                ni=int(ni)
                ei=dfname.split("_ei")[1].split("_ef")[0].replace("_",".")
                ei=float(ei)
                fw=float( dfname.split("_f")[1].replace("_",".") )  # simulated fwhm
                #print("DEBUG ei ",ei,"  fw=", fw )
                df['ei']=df['e']*0. + ei  # create DF ei to plot
                df['de']=df['ei']-df['e']
                print("$$$... DF E_i={:.3f} E_mean={:.3f} dE_mean={:.3f}  #N={}".format(
                                      df['ei'].mean(),df['e'].mean(),df['de'].mean(), ni   )
                )


                # i create 3 gauss distributions
                #
                #
                df['fwhmi']=np.random.normal( 0.0, fw/2.355 ,  len(df) ) # fwhm in simulation
                df['fwhm1']=np.random.normal( 0.0, float(fwhm)/2.355 ,  len(df) ) # parameter
                df['fwhm2']=np.random.normal( 0.0, float(fwhm)/2.355 ,  len(df) )
                ## x...E (has -f scatter from Ei + -f now)  vs.  y...dE (has automatic scatter + -f now)
                # DRAWING  EI x  Ei-E
                #print("D... C========", len(colors),"====" )
                #print("D... C========", len(colors),colors[0],"====" )
                print("D... C========", len(colors),colors[0],"====", list(colors[0]) , "====", set(colors[0] ) )
                ax.scatter( df['ei']+df['fwhm1']+df['fwhmi'],  # use initial(beam) fwhm and parameter fwhm
                            df['fwhm2']+df['de'],              # only parameter fwhm
                            marker=".",
                            #color=[0.7, 0.3, 0.1,  0.2],
                            color=list(colors[0]) ,
                            alpha=0.9, label=dfname+' [MeV]' )
                colors=colors[1:] #  remove the first color
                ax.set_xlabel("E_total(=initial) [MeV]")
                ax.set_ylabel("dE [MeV]")


                plotme=True
            # ----------------------------------------  dee-----END --


            # ------------------------------------  view -----  text data
            if (graph=="view") or (graph=="viewall"): #======= VIEW DATA
                print("D... view:")
                pd.set_option('display.max_colwidth', None)

                if graph=="viewall":
                    pd.set_option('display.max_rows', None)


                print(df)

            try:
                floatfwh=float(fwhm)
            except:
                floatfwh=-1


            #========= fwhm>0
            #if floatfwh>=0.: #====== GENERATE GAUSS == fwhm=2.355sigma

            # ------------------------------------  view -----  text data
            if graph=='e':
                print("D... graphing classical E:  ", graph)

                if PASSTHROUGH:
                    #print("...... MEAN ENERGY MODE")
                    print('i...  mean before convolution: {:.3f} {:.4f}'.format(df['e'].mean(),df['e'].std() ))
                    df['fwhm']=np.random.normal( 0.0, float(fwhm)/2.355 ,  len(df) )
                    df['e']=df['e']+df['fwhm']
                    print('i...  mean with   convolution: {:.3f} {:.4f}'.format(df['e'].mean(),df['e'].std() ))
                    ax.hist( df['e'], 20, ec='k',  alpha=0.3,label=dfname )
                    ax.set_xlabel("E [MeV]")
                    plotme=True
                elif floatfwh>0:
                    print(" ... ... IMPLANT, but fwhm defined:MEAN ENERGY MODE")
                    df['fwhm']=np.random.normal( 0.0, float(fwhm)/2.355 ,  len(df) )
                    ENE=dfname.split('_')[-4]+'.'+dfname.split('_')[-3]
                    ENE=float(ENE[1:])
                    df['e']=ENE+df['fwhm']
                    print('i...  mean with   convolution: {:.3f} {:.4f}'.format(df['e'].mean(),df['e'].std() ))
                    ax.hist( df['e'], 20, ec='k',alpha=0.3,label=dfname)
                    ax.set_xlabel("E [MeV]")
                    plotme=True

                #if IMPLANT:
                #    print(" ... ... IMPLANT MODE")
                #    ax.hist( df['x'], 20, ec='k',alpha=0.3,label=dfname+' [um]')
                #    ax.set_xlabel("depth [um]")
                #    plotme=True
            # ************* END OF ALL GRAPH **********************
            # ************* END OF ALL GRAPH **********************
            # ************* END OF ALL GRAPH **********************
            #print("D... ================================== Graph SUBsection END", file=sys.stderr)

        ####################### FINALY SHOW PLOT
        if plotme:
            print("D... plot section")
            #ax.legend( loc=4 , fontsize="x-small" )
            #???ax.legend.draggable()
            # Shrink current axis by 20%
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])
            ax.legend( loc=2, fontsize="x-small",bbox_to_anchor=(1.01, 1.01) )
            plt.rc('grid', linestyle="dotted", color='black')
            plt.grid()
            if savefig!="":
                plt.savefig( savefig )
            else:
                plt.show()
        print("D... FILE CLOSED")
        pd_file.close()
    ####### JUST LIST IF NO ELEMENTS
    else:
        print("D... NO PLOTS or NO STATS ASKED ")
        if (os.path.isfile( stor[0] )) :
            print("D... isfile YES:", stor[0] )
            pd_file = pd.HDFStore( stor[0] )
            print("D... detected filename shoud be open now:",  stor[0]  )
            nfiles+=1  # increment counter, color
            for i,v in enumerate(sorted(pd_file.keys())):
                print("{:03d} {}".format(i,v) )

            print("D... FILE CLOSED")
            pd_file.close()


#     else:
#         print('!... filename missing: use -S; open an item by specifying  line number after comma')
#         print("""
# STORE HELP:
#         - the SRIM simulations data are stored in Data Frame files - .hdf5 format
#         - each simulation is represented by one record in the file
#         - each simulation can be plotted with matplotlib facility from here:

#         # PLOT energy, yz position, x implant.depth, ...
#    nuphy  hdf5 -S ~/srim.hdf5,0,1 -g e
#    nuphy  hdf5 -S ~/srim.hdf5,0,1 -g yz
#    nuphy  hdf5 -S ~/srim.hdf5,0,1 -g x
#    nuphy  hdf5 -S ~/srim.hdf5,all -g cos
#    nuphy  hdf5 -S ~/srim.hdf5,all -g cosy
#    nuphy  hdf5 -S ~/srim.hdf5,all -g cosz
#    nuphy  hdf5 -S ~/srim.hdf5,all -g dee
# #? nuphy  hdf5 -S ~/srim.hdf5,0-4 -g 0.100
#         #COLORS 4 EACH FILE:
#    nuphy  hdf5 -S cu_t1.hdf5,all,cu_t2.hdf5,all  -g dee
#  """)



if __name__=="__main__":
    Fire(main)
