#!/usr/bin/env python3
"""
BASED ON
#https://scipython.com/book2/chapter-8-scipy/problems/p82/modelling-a-radioactive-decay-chain/


 This is the first working  ODE equation based test/simulation of activation
 - SPLIT  activation and decay ! for stability, else it breaks
 - TODO: make it usable
 - see the references at end

1/ DEFINE THE DERIV (aderiv) FUNCTION to solve. (TODO:  use some external)
2/ enable randomization (seems done? i.e. span of values in the same plot )
   - also (mainly) helps to see/x-check the stability of solutions
"""



from fire import Fire
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import random


species = ['156Tbgs']
ln2 = 0.69314718055
# The decay processes and their indexes in the list of rate coefficients, k
# 0: 212Pb -> 212Bi + beta-
# 1: 212Bi -> 208Tl + alpha
# 2: 212Bi -> 212Po + beta-
# 3: 208Tl -> 208Pb + beta-
# 4: 212Po -> 208Pb + alpha

beta = 0
beta = 0.01
rate0 = 137   # talys
rate1 = 9.16  #
rate2 = 73.8
X0 = None
# k = [1.816e-05, 6.931e-05, 1.232e-4, 3.851e-3, 2.310]

# k = np.array( [128.4, 24.4, 5.3] ) # DECAY HALFLIVES
# k = k*3600
# k = 1/k * ln2

k = None
#k = [1/128.4*3600 *ln2,   1/24.4*3600 *ln2,   1/600 *ln2]

# def deriv(t, X):
#     """ Return dX/dt for each of the species. """
#     return (-k[0] * X[0],                               # 212Pb
#              k[0] * X[0] - k[1] * X[1] - k[2] * X[1],   # 212Bi
#              k[1] * X[1] - k[3] * X[2],                 # 208Tl
#              k[2] * X[1] - k[4] * X[3],                 # 212Po
#              k[3] * X[2] + k[4] * X[3]                  # 208Pb
#            )

# Cross sections HERE
# Irradiation structure HERE
def aderiv(t, X):
    """ Return dX/dt for each of the species. """
    global beta, rate0, rate1, rate2,k,X0
    # irradiate
    #beta = 0#.140#.13
    if t>0: # irradiation STOPPED
        rate0 =0
        rate1 =0
        rate2 =0

    r0  = rate0 - k[0] * X[0] + k[1] * X[1] + (k[2] * X[2])*(1-beta)
    r1  = rate1 - k[1] * X[1]
    r2  = rate2 - k[2] * X[2]

    return (r0, r1, r2)



def run_calc(activation = False, decay = False, ti = -60, tf = 3600):
    """
    run for parameter set
    """
    global beta,rate0,rate1,rate2,k,X0

    # I must split the activation to regions - sharp drop
    if activation and not decay:
        X0 = [0,0,0]
        tf = 0 # cut time
    elif decay and not activation:
        #print(f"i...   starting decay with X0:\n {X0}" )
        ti = 0 # start EoB
    else:
        print("X... BAD CALL FOR solve")
        return

    #t_eval = np.random.uniform(low=ti, high=tf, size=int(abs(ti-tf)/3 ) )
    t_eval = np.random.uniform(low=ti, high=tf, size=250  )

    # add zero TIME.
    t_eval = sorted( np.concatenate( (t_eval, [0] ) , axis = None )  )
    if not activation and decay:
        t_eval = sorted( np.concatenate( (t_eval, [tf] ) , axis = None )  )

    # LSODA - automatic stiffness detection and switching  # DOP853  BDF  Radau RK23  RK45
    max_step = 3600
    if activation: max_step = 1
    # limiting artol e-4 from 4 digits to xxx
    soln = solve_ivp(aderiv, (ti, tf), X0, method='LSODA',
                     t_eval = t_eval,
                     first_step = 0.1, max_step = max_step,
                     atol = 1e-4   , rtol = 1e-4
                     )
    t = soln.t
    X = soln.y

    return t, X



def main():
    global beta,rate0,rate1,rate2,k,X0
    print("_"*70)
    print("i... THIS SHOULD BE 1st REAL TRY FOR 156Gd")
    print("i... THIS SHOULD BE 1st REAL TRY FOR 156Gd")
    print("_"*70)
    print("")

    XX = []
    tt = []

    RANDOMIZE = 1 # RANDOM OR NOT

    rng = 1
    norm = 1 # normalize later inside
    if RANDOMIZE==1:
        rng = 100
    for i in range(rng):
        # PREPARATION FOR CALL:
        # - X0

        print(f"->>   {i:03d}",end="\r")
        beta = 0.0
        #beta = 0.14
        if RANDOMIZE==1: beta =  random.uniform( 0, 0.13)
        #beta = 0.0


        # 2044 level - beta branch 8/75  gamma534  25.66 13
        #brerr = ((8/75)**2 + (0.13/25.66)**2 )**0.5
        #brerr = 0.13/25.66
        brerr = 0

        # cross sections ======================================
        # talys
        RANDOMIZE1=0  # Dont randomize
        rate0 = random.gauss( 137,   13*RANDOMIZE1 )
        rate1 = random.gauss( 9.16,  1*RANDOMIZE1 )
        rate2 = random.gauss( 73.8,  7*RANDOMIZE1 )

        # halflives ===========================================
        # randomize
        k = np.array( [random.gauss( 128.4, (0.1/5.35)*128 *RANDOMIZE ),
                       random.gauss( 24.4,  1.0*RANDOMIZE ),
                       random.gauss( 5.3,   0.2*RANDOMIZE )
                       ] ) # DECAY HALFLIVES
        k = k*3600
        k = 1/k * ln2


        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++SOLVE+++
        t,X = run_calc( activation = True, ti = -15*60, tf = 4*24*3600)
        X0 = []
        for ix in X:
            X0.append( ix[-1] )
        # print("i...X0 for decay: \n*",X0)
        t2,X2 = run_calc( decay = True, ti = -15*60, tf = 160*3600)
        t = np.concatenate( (t,t2) , axis = None )
        X = np.concatenate( (X,X2) , axis = 1)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++SOLVE++

        tt.append(t)

        # NORMALIZATION HERE to reproduce the exp....
        if norm==1:
            kx = 1/(128.4 * 3600) * ln2
            #print(f"i... last time: {t[-1]} s  last X0 before norm: {X[0][-1]}")
            Css = 1.2 * np.exp(- kx *  t[-1])
            #print("i... Css for norm",Css)
            #norm = -np.log(Css/1.2)/kx / X[0][-1]
            norm = Css / X[0][-1]
            norm = 5.929858704829203e-06 # HARDWAY FOR beta == 0
            print("i... NORM = ",norm)
        X = X * norm
        if RANDOMIZE==1:  X = X*random.gauss( 1, brerr )
        XX.append(X)

        # ======================================= evaluation

        t = t/3600 # TO HOURS
        mm = ":"
        if RANDOMIZE==1:mm=","
        plt.plot(t, X[0],mm+"r"  )
        plt.plot(t, X[1],mm+"b"  )
        plt.plot(t, X[2],mm+"g"  )
        # plt.plot(t, X[0],",", label=r'$^{156g}Tb$'  )
        # plt.plot(t, X[1],",", label=r'$^{156m1}Tb$' )
        # plt.plot(t, X[2],",", label=r'$^{156m2}Tb$' )


    kx = 128.4
    kx = kx*3600
    kx = 1/kx * ln2
    t = tt[0]/3600
    print(f"i... last time: {t[-1]}h  last X0: {X[0][-1]}")
    print(f"i... last time: {t[-1]}h  last X1: {X[1][-1]}")
    print(f"i... last time: {t[-1]}h  last X2: {X[2][-1]}")
    Css = 1.2 * np.exp(- kx *  tt[0])     # all intermediates in steady-state
    #print(t)
    # print(Css)

    plt.plot(t , Css, c='k', ls=':', label='decay guess')

    plt.legend()
    plt.xlabel(r'$t\;[\mathrm{hours}]$')

    #plt.ylabel(r'arb. units')
    plt.ylabel(r'arb. units; beta decay= '+f"{int(beta*100):02d}%")
    #plt.yscale('log')
    plt.grid()

    if beta == 0 and RANDOMIZE==0:
        plt.savefig("beta00.png")
    elif RANDOMIZE == 0:
        plt.savefig(f"beta{int(beta*100):02d}.png")
    else:
        plt.savefig("beta_rand.png")

    plt.show()

if __name__=="__main__":
    Fire(main)






#https://radioactivedecay.github.io/overview.html
#https://pypi.org/project/radioactivedecay/
#https://scipython.com/book2/chapter-8-scipy/problems/p82/modelling-a-radioactive-decay-chain/
#https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3
#https://github.com/Rolleroo/decaychain
#https://github.com/bjodah/batemaneq
