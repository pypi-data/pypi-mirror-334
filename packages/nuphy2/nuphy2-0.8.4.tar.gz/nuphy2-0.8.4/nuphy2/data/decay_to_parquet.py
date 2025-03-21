#!/usr/bin/env python3
"""
 This reads all txt files lara decay and creates parquet file with df
CATCHES:
  Ra-266D is skipped
  dE - where None - is set 1
  dI - where None - is set I
"""
from fire import Fire
import glob
import pandas as pd
from console import fg,bg
OUTFILE = 'decay_lara.parquet'
DECAYPATH = "./decay"
DECAYSUFF = ".lara.txt"
SLASH = ""
if DECAYPATH[-1] != "/":
    SLASH = "/"



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


def get_isotopes():
    """
    glob DIR , get all isotopes in the list
    """
    li = glob.glob( f"{DECAYPATH}{SLASH}*{DECAYSUFF}")
    li = [ x.lstrip(DECAYPATH).rstrip(DECAYSUFF) for x in li ]
    # li = sorted( [ f"{x.split('-')[1]}{x.split('-')[0]}" for x in li ])
    return li


def load_one_isotope(iso):
    """
    load TXT  for 1 isotope;
    some have no lines
    return LIST - 1 line is 1 element
    """
    nogamma = "Ca-45 P-33 Se-79 Ni-63 S-35 He-6 C-14 Rb-87 P-32 Sr-90 Pb-209 Ru-106 H-3"
    #if iso in nogamma:   return {}
    # if iso=="Ra-226D": return {}

    with open(f"{DECAYPATH}{SLASH}{iso}{DECAYSUFF}") as f:
        res = f.readlines()
    res = [x.strip("\n") for x in res]

    hf = [1,1]
    data = []
    datsec = False
    for i in res: # go for each line
        if i.find("Half-life (s)")>=0:
            print(i)
            hf = i.split(";")
            hf = [x.strip() for x in hf]
            hf.pop(0)
            #print(hf)
            if "E" in hf[0]:
                hf = [ float(x.split("E")[0])*pow(10,float(x.split("E")[1])) for x in hf ]
            else:
                hf = [ float(x) for x in hf]

        if datsec: # transition data
            data.append(i)
        if i.find("-"*10)>=0: # flag ON
            datsec = True

    if not datsec:
        return {},[]

    data.pop(0)
    data.pop(-1)
    #data.pop(0)
    #print(res)
    #return {}
    return data,hf



def line_to_list(line0):
    """
    ONE LINE - E dE I dI ->>> to a list, cut the end, translate to float
    """
    line = line0.split(";")[:5]
    line = [ x.strip() for x in line ]
    #print(line)

    # E dE I dI
    line[0] = round(100*float(line[0]))/100 # e
    if len(line[1])>0:  #  de
        line[1] = float(line[1])
    else:
        line[1] = 1

    if len(line[2])>0: # I
        line[2] = float(line[2])

    if len(line[3])>0: # dI
        line[3] = float(line[3])

    if line[4] == "a":
        return []
    return line[:-1]



def data_to_table( data ):
    """
    input: list of lines for one isotope
    output: list of lists ....
           translate semicolon separated values to pandas
    """
    lis = []
    for i in data:
        res = line_to_list( i )
        if len(res)>0:
            lis.append(res)
        #print(res)
    return lis




def main():
    print()
    res = get_isotopes()
    print("D...  decay isotopes in database:",len(res))
    df = pd.DataFrame( columns=["A","Z","ele","name","T12","dT12","E","dE","I","dI"])

    for i in  res:
        print("D... ",i, end=" ")

        #if i.find("Sb")>=0:    break


        if i=="Ra-226D":
            continue
        name = f"{i.split('-')[1]}{i.split('-')[0]}"
        a = i.split("-")[1]
        print(a) #
        if a.find("m")>0:
            a=int(a[:-1])
        else:
            a=int(a)
        e = i.split("-")[0]
        z = elements.index(e)
        dta,hf = load_one_isotope(i)
        print(hf)
        lis = data_to_table(dta)
        for i in lis:
            if len(i)!=4:
                print("X... not 4 columns", i)
            #print([a,z,e,name,*i])
            df.loc[len(df)] = [a,z,e,name,hf[0],hf[1],*i]
            #print(df.loc[len(df)-1])


    print()

    df['dI'] = pd.to_numeric(df['dI'], errors='coerce')
    df['dI'] = df['dI'].mask(df['dI'].isna(), df['I'])

    # df['dI'] = df['dI'].astype(float)
    #print( df.loc[ df["I"]>1 ].sort_values( ["dI"] ) )
    df = df.sort_values( ["E","A","Z"] )
    df.reset_index(drop=True, inplace=True)

    print("i... saving")
    df.to_parquet(OUTFILE)
    print("i... parquet saved")
    print(df)
        #print(lis)
        #break


def nicetime(t):
    suff = "s"
    if t>60:
        suff = "m"
        t = t/60
    if t>60:
        suff = "h"
        t = t/60
    if t>24:
        suff = "d"
        t = t/24
    if t>365:
        suff = "y"
        t = t/365

    if t>1e9:
        suff = "Gy"
        t = t/1e9
    if t>1e6:
        suff = "My"
        t = t/1e6
    if t>1e3:
        suff = "ky"
        t = t/1e3
    return f"{t:.2f} {suff}"



def candidates( dfo, e, de , t12low = 10, etrsh = 70, itrsh = 1):
    df = dfo
    df = df.loc[ df["I"]>itrsh ]
    df = df.loc[ df["E"]>etrsh ]
    df = df.loc[ (df["E"]>e-de) & (df["E"]<e+de) ]
    df = df.loc[ df["T12"]>t12low ]

    # susp = list(df['name'].values.tolist())

    for index, row in df.iterrows():
        currint = row['I']
        currene = row['E']
        currname  = row['name']
        print( f"{fg.white}{currname}    {nicetime(row['T12'])} {fg.default}")
        dfsel = dfo.loc[ (dfo['name']==currname) & (dfo['I']>=currint/3) ]
        for i2,r2 in dfsel.iterrows():
            if r2['E']==currene:
                print(f"{fg.green}", end = "")
            print(f"     {r2['E']:9.2f}  {r2['I']:7.2f}"  )
            if r2['E']==currene:
                print(f"{fg.default}", end = "")
        print( )



def load( E, dE=1):
    """
    verify the parquet
    """
    #E = 121
    dfo = pd.read_parquet(OUTFILE)
    # dfo = dfo.loc[ dfo["E"]>70 ]

    candidates( dfo , E, dE)

    #pd.set_option("display.max_rows", None, "display.max_columns", 7)
    #df = df.sort_values( ["E","A"] )


    #print(df)


if __name__=="__main__":
    Fire({"parq":main,
          "load":load}
         )
