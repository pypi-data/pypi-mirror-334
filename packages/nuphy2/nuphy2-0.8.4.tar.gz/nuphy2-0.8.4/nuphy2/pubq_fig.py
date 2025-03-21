#!/usr/bin/env python3
#
import os
import stat


# runpairs
# runall
# Front03.py
# mksvg

#  it seems that I use function prep( fname, fin ) and address files fname*:
# - rng  (10 lines, the last 2 are labels)
#         figxy size 2;
#         xrng 2; yrng 2; logx 1; logy 1; labels 2
# - a.mplstyle (sizes of all)
# - fname.csv (1st line columnNames: x,Solid,Dashed ...
#             ... points  pairs (midpoint and err)  qint (else cubic) noint (no interp)
#             ... red blue black solid dashed dotted dashdot label marker
#             ...  dsome is ERROR
# - OPT fname_points.csv
#
#  and lists: colorwheel, dashesStyles; markers
#
#
#   # rng - size and ranges
    # png - background
    # csv - data
#
#  1. when fin is 'test' -USES   fname_.png THAT IS TRIMMED TO AXES!!!!! as BACKGROUND
#  2. saves as fname__.png
#
# HERE ARE EXAMPLES CSV
# x,marker^markerblackpairs1labelMeissner et al.,x,bluepairs2labelOhsaki et al.,x,redmarkeromarkerpairs3labelVaughn et al.
#x,solidlabelTotal capture,dashed1label,dashed2label
#x,Solid,Dashed
#x,qintredSolidlabeltotal,qintDashedlabeldirect capture,qintDottedlabelresonance
#x,nointSolid,nointdashdot1,nointDotted1,nointSolid2,nointDashdot
#x,qintsolid,qintdashed,qintredSolid,qintdotted,qintdashdot
#x,points
#x,nointSolid,nointdashed,nointdotted
#x,pairs2,x,points1
#x,solid,dashed,dashdot,points
#x,points2  (down(
#x,points1  (up)
#x,solid1,solid2,dashed1,dashed2
#x,points,x,pairs2
#x,solid1,dashed1a,dashed1b,solid2,dashed2a,dashed2b
#x,pairs2,pairs
#x,markeromarkerpairs1,x,markeromarkerpairs2,x,markeromarkere1points
#x,non,e1points,non
#x,pairs1,pairs2,pairs3
#x,pairs1,e1points,pairs2
#x,redSolidlabelWiescher et al.label,reddashedlabellabel,reddashed2labellabel,SolidlabelBuckner et al.label,bluedashdotlabelScaled Coulomblabel,blueSolidlabelCoulomb potentiallabel,dashedlabelPerrey & Perey potentiallabel,dottedlabelhard sphere potentiallabel
#
#
#
#
#http://aeturrell.com/2018/01/31/publication-quality-plots-in-python/
#also nice : https://turnermoni.ca/python2.html https://www.bastibl.net/publication-quality-plots/ https://github.com/jbmouret/matplotlib_for_papers#a-publication-quality-figure
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import pandas as pd
#turrell

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter,AutoMinorLocator
import matplotlib as mpl


import matplotlib.image as mpimg

from fire import Fire

from scipy.interpolate import make_interp_spline,make_lsq_spline, BSpline
from scipy.interpolate import interp1d
from scipy.interpolate import UnivariateSpline # better spline? same....oversplined

import importlib # add __file__ module....
from PIL import Image

import sys


amplstyle = """
xtick.labelsize: 16
ytick.labelsize: 16
font.size: 16
figure.autolayout: True
axes.titlesize : 16
axes.labelsize : 16
lines.linewidth : 2
lines.markersize : 4
legend.fontsize: 12
mathtext.fontset: stix
font.family: STIXGeneral
"""











def initialize():
    print("""
TYPICAL WORKFLOW:
 - extract all images from pdf
 - copy useful to imgs2
 - improve and transjpg them to imgs3

CREATING FILES:
1_extract_imgs


""")


    bash1_extract = """#!/bin/bash

mkdir -p imgs1;
mkdir -p imgs2_select


for i in *.pdf; do
    bname=`basename $i .pdf`
    echo ========================== $bname

    pdfimages -all $i  ./imgs1/$bname
done

ls ./imgs1/
echo +===================
ls ./imgs2_select
"""


    bash2_nice = """#!/bin/bash
#  take care about images, make bigger, brighter fillwhite
echo STARTING resize and nice ============================================

mkdir -p imgs3_res
mkdir -p imgs4_nice

for i in imgs2_select/*.jpg; do
    echo ____________________ $i

    bname=`basename $i .jpg`

    convert $i  -resize 1048x  ./imgs3_res/${bname}.jpg
done
echo IN DIR ./imgs3_res/
ls ./imgs3_res/


echo Starting morgify =====================================================

for i in imgs3_res/*.jpg; do
    echo _______________________ $i

    bname=`basename $i .jpg`


    mogrify -despeckle -fuzz 5% -fill white -opaque white -gamma 0.8  -depth 6 -path ./imgs4_nice/ -format jpg $i



    # echo mogrify -despeckle -fuzz 5% -fill white -opaque white -gamma 0.8  -depth 6 -path ../figuresjj -format jpg ../figuresjj/$i

done
echo  IN DIR ./imgs4_nice
ls  ./imgs4_nice

"""

    bash3_engauge = """#!/bin/bash

help{
echo ______________________________ engauge_digitizer
echo TUTORIAL:
echo ... name DATA as:  solid,dashed,dashdot,dotted,redsolid   greenpoints1,points2,pairs,pairsym
echo ...
echo EXPORT FORMAT:
echo ... USE raw x,y for all exports
echo ...
echo ... for points and pairsym - use  RELATIONS
echo ... for curves use functions
}

help
engauge
help

"""


    bash4_runpairs = """
#!/bin/bash
#
# take all jpg
# tail it side by side with montage
# save _XX.png
# CREATE GLOBAL VIEW SHEET
#

for file in *.jpg; do
  fname=`basename $file .jpg`
   echo  $file "   "  ${fname}__.png ... ${fname}_XX.png
   montage -geometry 1000x -mode concatenate $file ${fname}__.png -tile 2x ${fname}_XX.png
done

n=`ls -1 *_XX.png | wc -l`
echo $n XX files present
 montage -mode concatenate *_XX.png -tile 1x3 out.png

"""

    for i in [ "bash1_extract","bash2_nice","bash3_engauge", "bash4_runpairs" ]:
        with open(i,"w") as f:
            f.write( f"{locals()[i]}" )

        st = os.stat(i)
        os.chmod(i, st.st_mode | stat.S_IEXEC)
    return



def datasci():
    """https://towardsdatascience.com/an-introduction-to-making-scientific-publication-plots-with-python-ea19dfa7f51e
    """
    # Collect all the font names available to matplotlib
    font_names = [f.name for f in fm.fontManager.ttflist]
    #print(font_names)
    # Edit the font, font size, and axes width
    #mpl.rcParams['font.family'] = 'Prusia'
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.linewidth'] = 1

def p4astro():
    """
    #https://python4astronomers.github.io/plotting/publication.html
    """
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')
    fig = plt.figure(figsize=(4, 3) , dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    plt.plot([1, 2, 3, 2])
    ax.set_xlabel('E$_{cm}$ (MeV)')
    ax.set_ylabel('S Factor (keV*b)')
    #plt.rc('text', usetex=True)





#def aeturrell( xrng, yrng ):
def prep( fname , background = False, ini=False):
    """
    Plot Publicable Figure.

    Use csv data and rng def. file to plot Pub Figure.
    Based on http://aeturrell.com/2018/01/31/publication-quality-p

    TWO CSV: x.csv for curves and x_points.csv for points
    CURVES: solid,dahsed,dotted...
    exported as raw x,y function-smooth

    POINTS: pairs is down-up pair for Y-error
     exported as raw x,y ;  relation -straight

    :param fname: filename without extension, csv and rng is used
    :param clean: default use background of the image __.png.
    :param ini: Create three bash files to extract PDF, ResizeMorg and Engauge
    :return: Plots __.jpg file
    """


    # rng - size and ranges
    # png - background
    # csv - data
    #=============================== READ PLOT REGION============


    if ini:
        initialize()
        sys.exit(0)


    ok=False
    try:
        print("i... ", fname+".rng")
        with open( fname+".rng") as f:
            rngs=f.readlines()
        ok=True
    except:
        print("D......... NO RNG FILE")
        print("""echo "5
5
0
100
0.005
1e+2
0
1
theta (deg)
arb.units">  a.rng
        """)
    if not ok : sys.exit(1)# quit()

    rngs=[ i.strip() for i in rngs]
    for i in range(len(rngs)-2): # the last 2 lines are not float, but labels
        rngs[i]=float(rngs[i])
    print("i...RNG:", rngs )
    figxy,xrng,yrng,logx,logy=rngs[:2],rngs[2:4],rngs[4:6], rngs[6], rngs[7]
    labelxy=rngs[8:10] # the last 2 lines are not float, but labels
    print("i...AXE:",xrng, yrng)
    #removed from a.mplstyle figure.figsize: 5,3.4

    #========================================================END








    #===============================================READ STYLE====
    if not os.path.exists("a.mplstyle"):
        print("X.... a.mplstyle  NOT PRESENT.... I create one")
        with open("a.mplstyle", "w") as f:
            f.write(amplstyle)
        # sys.exit(1)
    plt.style.use( 'a.mplstyle')
    # Make some style choices for plotting
    colourWheel =['#329932',
            '#ff6961',
            'b',
            '#6a3d9a',
            '#fb9a99',
            '#e31a1c',
            '#fdbf6f',
            '#ff7f00',
            '#cab2d6',
            '#6a3d9a',
            '#ffff99',
            '#b15928',
            '#67001f',
            '#b2182b',
            '#d6604d',
            '#f4a582',
            '#fddbc7',
            '#f7f7f7',
            '#d1e5f0',
            '#92c5de',
            '#4393c3',
            '#2166ac',
            '#053061']
    dashesStyles = [[3,1],
            [1000,1],
            [2,1,10,1],
            [4, 1, 1, 1, 1, 1]]
#    df=pd.DataFrame( [[1,2,3],[2,3,1]] )
# Point to the data fileName = 'rftxlicp1017unlinked.xls'
    plt.close('all')


    linethick=1
    alphaVal=1
    fig, ax = plt.subplots( figsize=( figxy ) ,dpi=300)

#    ax.plot(df.index,
#                df,
#            #                    color=colourWheel[j%len(colourWheel)],
#                linestyle = '-',
#            #                    dashes=dashesStyles[j%len(dashesStyles)],
#                lw=linethick,
#                #label=df.columns,
#                alpha=alphaVal)
#    ax.set_xlabel('')

    ax.yaxis.set_major_formatter( ScalarFormatter() )
    ax.yaxis.major.formatter._useMathText = True
    #==============number of minor ticks=================
    ax.yaxis.set_minor_locator(  AutoMinorLocator(2))
    ax.xaxis.set_minor_locator(  AutoMinorLocator(2))
    #ax.yaxis.tick_right() # right side coordinates
    #    nameOfPlot = 'GDP per hour (constant prices, indexed to 2007)'
    #------------ylabel rotation and position ------------------------
    #plt.rcParams['axes.linewidth'] = 2
    #ax.yaxis.set_label_coords(0.63,1.01)
    #plt.ylabel(nameOfPlot,rotation=0)


    if logy:
        plt.yscale('log')
    if logx:
        plt.xscale('log')
    #plt.xlim([0, 0.7])
    #plt.ylim([1e-3, 1e+1])
    plt.xlim( xrng )
    plt.ylim( yrng )


    #    x = np.linspace( xrng[0], xrng[1]   , 300)
    #    ax.plot(x, ((0.8*x)**(-0.01))-0.9, color='0.50', ls='dotted' ,lw=2)
    #    ax.plot(x, 0.1-0.1*x, color='0.50', ls='dotted' ,lw=2)
    #    ax.plot(x, x**1.2+0.1 , color='k', ls='solid' ,lw=2)

    fif = fname+".csv"
    fif_curves = []
    fif_points = []
    isbroke = False
    frst = True
    if os.path.isfile(fif):
        with open(fif) as f:
            alli = f.readlines()
        alli = [x.strip() for x in alli]
        for i in alli:
            if len(i)<1:
                isbroke = True
                frst = True
                print(i,"                  <<<<<< BREAK")
            else:
                if frst:
                    print(i)
                    frst = False
                if isbroke:
                    fif_points.append(i)
                else:
                    fif_curves.append(i)
    else:
        print("X...   NO CSV FILE")
        sys.exit(1)

    if isbroke: # two new csv created
        #print(fif_curves)
        print("i... SAVING CURVES", len(fif_curves) )
        with open(fname+"_curves.csv","w") as f:
            f.write( "\n".join(fif_curves) )
        print("i... SAVING POINTS", len(fif_points))
        with open(fname+"_points.csv","w") as f:
            f.write( "\n".join(fif_points) )
    #sys.exit(0)

    legend=False
    markers=['o','s','^','x','D']
    #======================== TWO POSSIBLE FILES ===============
    #  curves/     ...  column "points"
    if isbroke:
        files=[fname+"_curves.csv", fname+"_points.csv"]
    else: # classical
        files=[fname+".csv", fname+"_points.csv"]

    print("D... GOTO FILES:", files)
    for fif in files:
        #=============================== READ  DATA ============
        if os.path.isfile(fif):
            df=pd.read_csv(fif)
            print(df,df.columns)
        else:
            print("!...   NO CSV FILE, I continue")
        #========================================================END
        if os.path.isfile(fif):
            realx='x'

            # check columns
            for icol in df.columns:
                if icol.find("x")==0:
                    pass
                elif icol.lower().find("points")>=0:
                    pass
                elif icol.lower().find("pairs")>=0: # midp, max error def
                    pass
                elif icol.lower().find("pairsym")>=0: # symetric error def
                    pass
                elif icol.lower().find("qint")>=0:
                    pass
                elif icol.lower().find("solid")>=0:
                    pass
                elif icol.lower().find("dashed")>=0:
                    pass
                elif icol.lower().find("dotted")>=0:
                    pass
                elif icol.lower().find("dashdot")>=0:
                    pass
                elif icol.lower().find("label")>=0:
                    print("X... not label BUT Label")
                    sys.exit(1)
                elif icol.lower().find("marker")>0:
                    print("X... not marker BUT Marker")
                    sys.exit(1)
                else:
                    print("X...  not points nor pairs .... some problem somewehere in csv")
                    sys.exit(1)


            for icol in df.columns:
                if icol.find('x')==0:
                    realx=icol
                    continue
                if icol=='none':continue
                print("D... ###############plotting column", icol ,"####################")
                #------------ here I must create new DF :  remove all Nan values...
                dfn=df[ (pd.notnull( df[icol] ) ) &(  pd.notnull( df[ realx ] ) ) ].copy()
                dfn.reset_index(drop=True, inplace=True)

                print(dfn)
                print("----------------it was dfn _______ life begins for: ", realx,icol)
                #------------ from here, dfn

                color='k'
                label=icol
                # default: no maker no line; err1=> nothing
                ls=''
                marker=""
                yerr=None
                #----------------- spline for curves -------- BUT NOT For POINTS ---------
                if (icol.lower().find("points")<0) and (icol.lower().find("pairs")<0):


                    # Creating the knots
                    print( "D... length of points:",len(dfn) )
                    # knots=len(dfn)-5
                    if icol.lower().find("qint")>=0:
                        print("D...  quadratic  QINT")
                        k=2
                    else:
                        print("D...  CUBIC by DEFAULT")
                        k=3
                    # t_int  = np.linspace(dfn[ realx ].min(),dfn[ realx ].max(),knots) #int.knots
                    # t_begin= np.linspace(dfn[ realx ].min(),dfn[ realx ].min(),k)
                    # t_end  = np.linspace(dfn[ realx ].max(),dfn[ realx ].max(),k)
                    # t = np.r_[t_begin,t_int,t_end]
                    # print("... knots: ",t)
                    xnew = np.linspace(dfn[ realx ].min(),dfn[ realx ].max(),300)
                    spl = make_interp_spline( dfn[ realx ],dfn[icol], k=k) #BSpline object
                    #spl = make_lsq_spline( dfn[ realx ],dfn[icol], t, k=k) #BSpline object
                    #spl=interp1d( dfn[ realx ],dfn[icol] , kind="cubic")
                    #spl=UnivariateSpline( dfn[ realx ],dfn[icol] )
                    #spl.set_smoothing_factor(0.5)
                    power_smooth = spl(xnew)
                    if icol.lower().find("noint")>=0:
                        print("D...  LINEAR CONNECTIONS, no interpolation !!!! ")
                        xnew=dfn[ realx ]
                        power_smooth=dfn[ icol ]
                    #ax.plot( dfn['x'], dfn[ icol ] , color='k', ls=icol ,lw=1, kind='quadratic')


                #-------------------------------------------------------------------
                if icol.lower().find("points")>=0:    #points ... no smoothing
                    ls=""
                    marker=markers.pop(0)
                    xnew=dfn[realx]
                    power_smooth=dfn[icol]
                    #
                    #  e1 removed????
                    #
#                    if icol.find("e1")>=0:
#                        yerr=power_smooth*0.+0.1
                    #yerr=power_smooth*0.14*(xnew/50)
                    #plt.errorbar(xnew, power_smooth, yerr = yerr , marker=marker,
                    #             ls=ls, color=color,
                    #             solid_capstyle='projecting', capsize=4, lw=1)


                if icol.lower().find("pairs")>=0:     #points ... no smoothing
                    ls=""
                    marker=markers.pop(0)
                    #dfpa=df[ pd.notnull(df[icol] ) ] # NEW df
                    dfpa=dfn
                    #
                    # starts with 0=> evens;  -1==look forward
                    #
                    # ---- MIDPOINT AND HIorLOW ==== NORMAL
                    dfpa['d'+icol]=abs(dfpa[icol].shift(-1) -dfpa[icol]) # put paired
                    dfpa2=dfpa[dfpa.index % 2 ==0 ]      # new df; starts with #0!!!

                    if icol.lower().find("pairsym")>=0:
                        # I can try reconstruct as if low-hi was entered => midpoint
                        dfpa2[icol] = (dfpa2[icol]*2+dfpa2["d"+icol])/2
                        dfpa2["d"+icol] = dfpa2["d"+icol]/2


                    print(dfpa2)
                    print("__________ it was dfpa2 :column=",icol," ___________")
                    xnew=dfpa2[realx]
#                    if icol.find("l0.")>=0:
#                        dfpa2['x']=dfpa2['x']-0.01
                    power_smooth=dfpa2[icol]
                    yerr=dfpa2['d'+icol]
#                    if icol.find("m3")>=0:
#                        print("D............ multiplying by 3X")
#                        power_smooth=power_smooth*3
#                        yerr=yerr*3+0.1
                #---------------------------------------------COLORS
                if icol.lower().find("red")>=0:
                    color='r'
                    print("D... color red")
                if icol.lower().find("blue")>=0:
                    color='blue'
                    print("D... color blue")
                if icol.lower().find("green")>=0:
                    color='green'
                    print("D... color green")
                if icol.lower().find("black")>=0:
                    color='k'
                    print("D... color black")
                #---------------------------------------------LINES
                if icol.lower().find("solid")>=0:
                    ls='solid'
                if icol.lower().find("dashed")>=0:
                    ls='dashed'
                if icol.lower().find("dotted")>=0:
                    ls='dotted'
                if icol.lower().find("dashdot")>=0:
                    ls='dashdot'
                #---------------------------------------------- LABEL
                if icol.find("Label")>=0:
                    # LABEL AT THE END???? OR BETWEEN!
                    label=icol.split('Label')[1]
                    legend=True
                #---------------------------------------------- spec.marker
                if icol.lower().find("Marker")>=0:
                    # LABEL AT THE END????
                    marker=icol.split('Marker')[1]
                    #legend=True


                #====================================================PLOT=============
                if yerr is None:
                    ax.plot( xnew, power_smooth , color=color, marker=marker, ls=ls ,lw=1 , label=label, ms=5)
                else:
                    ax.errorbar(xnew, power_smooth ,yerr,  color=color, marker=marker, ls=ls ,lw=1 , label=label, ms=5, solid_capstyle='projecting', capsize=4)




    #================ axes labels  x,y
    ax.set_xlabel( labelxy[0])
    ax.set_ylabel( labelxy[1])

    #####ax.set_yticklabels(horizontalalignment = "left")
    ax.tick_params(which="major",direction="in", length=9)  #major+minor
    ax.tick_params(which="minor",direction="in", length=4)  #major+minor
    #ax.minortick_params(direction="in")
    #ax.xaxis.set_ticks_position('both')  # Adding ticks to both top and bottom
    #ax.xaxis.set_tick_params(direction='in', which='bottom')  # The bottom will maintain the de

    #plt.savefig(os.path.join(dirFile,'ProdCountries.pdf'),dpi=300)
    #plt.show()


    #=============== extracode
    if os.path.isfile(fname+".py"):
        module = importlib.import_module(fname, package=None)
        module.plot_extra(plt)

    if legend:
        print("i... legend")
        ax.legend(frameon=False, loc='upper left',ncol=1,handlelength=4)
        #plt.gca().legend(('y0','y1'))

    #========================================= BACKGROUND MAKES BIG CHANGES====
    #======================================what you want, do before=============
    if background:# =="test":
        print("i... BACKGROUND IMAGE MAGICK")
        #============================= IMAGE BACKGROUND MAGIC
        #--------image background-----------------------
        #print( xrng+yrng )
        ax.set_zorder(2)
        ax.set_facecolor('none')
        ax_tw_x = ax.twinx()
        ax_tw_x.axis('off')
        ax2 = ax_tw_x.twiny()

        bgname=fname+"_.png"
        print("D...   reading",bgname)
        img=mpimg.imread( bgname )  #  import matplotlib.image as mpimg
        if len(img.shape)==2: # BW image! Convert to RGB
            print( "D... BG IMAGE SHAPE ... ",type(img), "shape=",img.shape  )
            #print(img, "TWODIMS")
            img2=np.zeros( (img.shape[0],img.shape[1],3) )+1 # create ones
            for i in range(len(img)):
                #print("I: ",i , "/", len(img)  )
                for j in range(len( img[i])):
                    #print("J: ",i,j, img[i][j])
                    img2[i][j]=img2[i][j]* img[i][j] # create gray
            img=img2
        #print("---------------")
        #print(img)
        print( "D... BG IMAGE SHAPE ... ",type(img), "shape=",img.shape  )
        if len(img.shape)==3:
            #print(img)
            for i in img:
                for j in i:
                    if j[0]+j[1]+j[2]<3*0.9:
                        j[0]=1.
                        j[1]=0.5
                        j[2]=0
        # if len(img.shape)==2: # BW image!
        #     for i in img:
        #         for j in i:
        #             if j<0.9:
        #                 j=0.3
        #             #print(j)


        #print(img)
        print("D... showing at axis 2")
        ax2.imshow(img, aspect='auto', extent=xrng+yrng, zorder=-1, alpha=1)
        ax2.axis('off')
#============================ END OF BACKGROUND.....now only plot============


    plt.savefig(fname+"__.png")
    print(f"i...  original figure ...  {fname}.png")
    print(f"i...  background      ...  {fname}_.png")
    print(f"i...  new figure      ...  {fname}__.png")

    #print("i...  {fname}_.png}")
#p4astro()
#aeturrell( [0, 0.7], [1e-3, 1e+1] )

if __name__=="__main__":
    Fire(prep)
