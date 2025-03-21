#!/usr/bin/env python3
# -fire CLI
from fire import Fire

from nuphy2.version import __version__
from nuphy2.prj_utils import get_file_path

from nuphy2 import config

from nuphy2.prj_utils import fail
from nuphy2.prj_utils import Bcolors
#from nuphy2.prj_utils import super_print
# print("D... isotope - all nuphy prj  imported")

#import pkg_resources  # tobeable toreaddatainpackage  "pip3 install setuptools"

#assert
#print("XX", pkg_resources.   )
#print("XX", pkg_resources.resource_exists('nuphy2', 'data/nubase2016.txt') )
#assert pkg_resources.resource_exists('data', 'nubase2016.txt')
#print("XX", pkg_resources.resource_exists('nuphy2', 'nubase2016.txt') )

#DEBUG=False
#if DEBUG:print(" D... module nuphy2/react is being run")

# this stopped to work....
#DB_FILE = pkg_resources.resource_filename('nuphy2','data/nubase2016.txt')
#print("D1...", DB_FILE)


DB_FILE = get_file_path("nubase2016.txt")


#= pkg_resources.resource_filename(
#    pkg_resources.Requirement.parse('nuphy2'),
#    'data/nubase2016.txt'
#)


#print("D... datafile", DB_FILE)
#DB_FILE = pkg_resources.resource_filename('nuphy2','data/nubase2016.txt')
#print("D3...", DB_FILE)

with open(DB_FILE) as f:
    masstable=f.read().strip()
masslist=masstable.split('\n')
#if DEBUG:print(" D... module nuphy2/react is in memory")


#====================================================

def func():
    #if DEBUG:print(" D... function defined in nuphy2:react")
    return True

def test_func():
    #if DEBUG:print(" D... test function ... run pytest")
    assert func()==True

#=======================================================
def isfloat(value):
    ok=False
    try:
        float(value)
        ok=True
    except ValueError:
        return False
    return ok

def test_isfloat():
    assert isfloat(1.1)==True
    assert isfloat("1.1")==True
    assert isfloat("w1.1")==False
    assert isfloat(1)==True


def isint(value):
    ok=False
    try:
        i=int(value)
        if str(i)==str(value):
            ok=True
    except ValueError:
        return False
    return ok



def test_isint():
    assert isint(3)==True
    assert isint(3.1)==False
    assert isint("4")==True
    assert isint("w4")==False

#===============================================
elements=['n','H','He','Li','Be','B','C','N','O','F','Ne',
          'Na','Mg','Al','Si','P','S','Cl','Ar',
          'K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr',
          'Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe',
          'Cs','Ba',
          'La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf',
          'Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi',
          'Po','At','Rn','Fr','Ra','Ac', 'Th','Pa','U',
          'Np','Pu','Am','Cm','Bk','Cf','Es',
          'Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt',
          'Ds','Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og']; #110-118


densities=[0,0.00008988,0.0001785,
0.534,1.85,2.34,2.267,0.0012506,0.001429,0.001696,0.0008999,#Ne
0.971,1.738,2.698,2.3296,1.82,2.067,0.003214,0.0017837,#Ar
0.862,1.54,2.989,4.540,6.0,7.15,7.21,7.86,8.9,8.908,8.96,7.14,
5.91,5.32,5.72,4.79,3.12,0.003733,
1.63,2.54,4.47,6.51,8.57,10.22,11.5,12.37,12.41,12.02,10.5,8.65,
7.31,7.31,6.68,6.24,4.93,0.005887,
1.87,3.59,6.15,
6.77,6.77,7.01,7.3,7.52,5.24,7.9,8.23,8.55,8.8,9.07,9.32,6.9,9.84,
13.31,16.65,19.35,21.04,22.6,22.4,21.45,19.32,13.55,
11.85,11.35,9.75,9.3,7.000,0.00973,#...At,Rn
1.87,5.5,10.07,
11.72,15.37,18.95,20.45,19.84,13.69,#Th...Am
13.51,14.79,15.1,8.84,#Cm...Es99
9.7,10.3,9.9,15.6,23.2,29.3,35.0,37.1,40.7,37.4,#Fm...Mt109
34.8,28.7,23.7,16,14,13.5,12.9,7.2,5.0#Ds110...Og118
];

gaseous=[1 ,1 ,1 ,0 ,0 ,0 ,0 ,1 ,1 ,1 ,1 , #NFNe
         0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 , #CLAr
         0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 , #Kr
         0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 , #Xe
         0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 , #Rn
         0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ]

molarweights=[1,1.0079,4.0026,
6.941,9.01218,10.811,12.0107,14.0067,15.9994,18.998,20.1797,
22.98977,24.305,26.9815,28.0855,30.97376,32.065,35.453,39.948,
39.0983,40.078,44.9559,47.867,50.9415,51.996,54.938,55.845,58.933,58.693,63.546,65.409,
69.723,72.64,74.9216,78.96,79.904,83.8,
85.4678,87.62,88.906,91.224,92.9064,95.94,98,101.07,102.9055,106.42,107.8682,112.411,
114.818,118.71,121.76,127.6,126.9045,131.293,
132.9055,137.327,139.9055,
140.116,140.9077,144.24,145,150.36,151.964,157.25,158.925,162.5,164.9303,167.259,168.9342,173.04,174.967,
178.49,180.9479,183.84,186.207,190.23,192.217,195.078,196.9665,200.59,
204.3833,207.2,208.9804,209,210,222,#At,Rn
223,226,227,#Fr,Ra,Ac
232.0381,231.0359,238.0289,237,244,243,#Th..Pu,Am
247,247,251,252,257,258,259,266,267,268,269,270,277,#...Hs108
278,281,282,285,286,289,290,293,294,294#....Ts117,Og118
]



alliso={
0 : [1] ,
1 : [1, 2, 3, 4, 5, 6, 7] ,
2 : [3, 4, 5, 6, 7, 8, 9, 10] ,
3 : [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] ,
4 : [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16] ,
5 : [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ,
6 : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23] ,
7 : [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25] ,
8 : [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28] ,
9 : [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31] ,
10 : [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34] ,
11 : [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37] ,
12 : [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40] ,
13 : [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43] ,
14 : [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45] ,
15 : [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47] ,
16 : [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49] ,
17 : [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51] ,
18 : [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53] ,
19 : [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56] ,
20 : [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58] ,
21 : [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61] ,
22 : [38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64] ,
23 : [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67] ,
24 : [42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70] ,
25 : [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72] ,
26 : [45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75] ,
27 : [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77] ,
28 : [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80] ,
29 : [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82] ,
30 : [54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85] ,
31 : [56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87] ,
32 : [58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90] ,
33 : [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92] ,
34 : [64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95] ,
35 : [67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98] ,
36 : [69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101] ,
37 : [71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103] ,
38 : [73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107] ,
39 : [75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109] ,
40 : [77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112] ,
41 : [79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115] ,
42 : [81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118] ,
43 : [83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121] ,
44 : [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124] ,
45 : [88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127] ,
46 : [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129] ,
47 : [92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132] ,
48 : [94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134] ,
49 : [96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137] ,
50 : [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139] ,
51 : [103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141] ,
52 : [105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143] ,
53 : [107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145] ,
54 : [109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148] ,
55 : [111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152] ,
56 : [113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154] ,
57 : [116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156] ,
58 : [119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158] ,
59 : [121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160] ,
60 : [124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162] ,
61 : [126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164] ,
62 : [128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166] ,
63 : [130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168] ,
64 : [133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170] ,
65 : [135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172] ,
66 : [138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174] ,
67 : [140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176] ,
68 : [142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178] ,
69 : [144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181] ,
70 : [148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185] ,
71 : [150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188] ,
72 : [153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190] ,
73 : [155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194] ,
74 : [157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197] ,
75 : [159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199] ,
76 : [161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203] ,
77 : [164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205] ,
78 : [166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208] ,
79 : [169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210] ,
80 : [171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216] ,
81 : [176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218] ,
82 : [178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220] ,
83 : [184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224] ,
84 : [186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227] ,
85 : [191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229] ,
86 : [193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231] ,
87 : [197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233] ,
88 : [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235] ,
89 : [205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237] ,
90 : [208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239] ,
91 : [211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241] ,
92 : [215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243] ,
93 : [219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245] ,
94 : [227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247] ,
95 : [229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249] ,
96 : [231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252] ,
97 : [233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254] ,
98 : [237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256] ,
99 : [239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258] ,
100 : [241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260] ,
101 : [245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262] ,
102 : [248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264] ,
103 : [251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266] ,
104 : [253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268] ,
105 : [255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270] ,
106 : [258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273] ,
107 : [260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275] ,
108 : [263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277] ,
109 : [265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279] ,
110 : [267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281] ,
111 : [272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283] ,
112 : [276, 277, 278, 279, 280, 281, 282, 283, 284, 285] ,
113 : [278, 279, 280, 281, 282, 283, 284, 285, 286, 287] ,
114 : [284, 285, 286, 287, 288, 289] ,
115 : [287, 288, 289, 290, 291] ,
116 : [289, 290, 291, 292, 293] ,
117 : [291, 292, 293, 294] ,
118 : [293, 294, 295] ,
}





def hf_to_factor(halflife, uniti):
    if (uniti.strip()  == 'Zy'):
        halflife=halflife*365*24*3600*1e+24
    if (uniti.strip()  == 'Zy'):
        halflife=halflife*365*24*3600*1e+21
    if (uniti.strip()  == 'Ey'):
        halflife=halflife*365*24*3600*1e+18
    if (uniti.strip()  == 'Py'):
        halflife=halflife*365*24*3600*1e+15
    if (uniti.strip()  == 'Ty'):
        halflife=halflife*365*24*3600*1e+12
    if (uniti.strip()  == 'Gy'):
        halflife=halflife*365*24*3600*1e+9
    if (uniti.strip()  == 'My'):
        halflife=halflife*365*24*3600*1e+6
    if (uniti.strip()  == 'ky'):
        halflife=halflife*365*24*3600*1e+3
    if (uniti.strip()  == 'y'):
        halflife=halflife*365*24*3600
    if (uniti.strip()  == 'd'):
        halflife=halflife*24*3600
    if (uniti.strip()  == 'h'):
        halflife=halflife*3600
    if (uniti.strip()  == 'm'):
        halflife=halflife*60
    if (uniti.strip()  == 'ms'):
        halflife=halflife*1e-3
    if (uniti.strip()  == 'us'):
        halflife=halflife*1e-6
    if (uniti.strip()  == 'ns'):
        halflife=halflife*1e-9
    if (uniti.strip()  == 'ps'):
        halflife=halflife*1e-12
    if (uniti.strip()  == 'fs'):
        halflife=halflife*1e-15
    if (uniti.strip()  == 'as'):
        halflife=halflife*1e-18
    if (uniti.strip()  == 'zs'):
        halflife=halflife*1e-21
    if (uniti.strip()  == 'ys'):
        halflife=halflife*1e-24
    return halflife

#--------------------------- CLASS CONTAINING ALL
#--------------------------- CLASS CONTAINING ALL
#--------------------------- CLASS CONTAINING ALL
#--------------------------- CLASS CONTAINING ALL
#--------------------------- CLASS CONTAINING ALL
#--------------------------- CLASS CONTAINING ALL
#--------------------------- CLASS CONTAINING ALL
#
# spin, parity, halflife NOR DONE
#
class Isotope:
    mex = 0.0
    dmex = 0.0
    spin = 0
    halflife = None
    stable = False
    IS = 0.0 # abundance
    name = ''
    namesrim = ''
    A = 0
    Z = 0
    N = 0
    spin = 9999.
    parity = 0.0
    amu = 0.0
    isodensity = 0.0
    #    isodensity2=0.0
    abundances=[]
    avgmass = 0 # nat element avg A
    isodebug = False

    def __init__(self,A,Z,name, debug=False):
        #global print
        self.isodebug = debug
        #print=super_print(self.isodebug)(print)

        self.A,self.Z,self.name=A,Z,name
        self.N=A-Z
        #DB_FILE = pkg_resources.resource_filename('nuphy2',
        #                                          'data/nubase2016.txt')
        #with open(DB_FILE) as f:
        #    masstable=f.read().strip()
        #masslist=masstable.split('\n')
        stables=[]
        grounds=[]
        Zisot=[]
        #print(masstable)
        #if DEBUG:print(" D.. masses loaded ... ", len(masslist),'lines')
        found=False
        zminmax={}
        for li in masslist:
            #=============  SELECTION CRITERIA ===== GS ONLY=========
            if ( li[7] == '0' ):  #-------- only ground states ..."0"  nonzero: 8==>Li"i"
                AA,ZZ=int(li[:3]),int(li[4:7])
                if not ZZ in zminmax: #===attempt to collect all isotopes (later to incorp)
                    zminmax[ZZ]=[]
                zminmax[ZZ].append(AA)
                #--- decode 1st comment (can be IS) ABUNDANCE IS=92.41 7Li
                ISlis=li[110:].split(';')[0].split(" ")
                IS=ISlis[0]
                dIS=0
                if len(ISlis)>1:dIS=ISlis[1]


                #------------if our isotope:==== GET MEX DMEX IS
                #==================================== MY ISOTOPE
                if AA==A and ZZ==Z:
                    found=True
                    #if DEBUG:print(li)
                    self.mex=float( li[17:24]+'.'+li[25:29] ) #@24...# or .
                    self.dmex=float( li[30:33]+'.'+li[34:38] )
                    if IS[:3]=="IS=":self.IS=IS[3:]
                    else: self.IS=0
                    hfl=li[60:78]
                    if hfl.find("stbl")>=0:
                        self.halflife=0
                        self.stable=True
                    else:
                        #print( "DDD... ",li[60:69] )
                        ha= (li[61:64]+'.'+li[65:69]).strip()
                        if ha[0]==">":
                            qhalflife= float( ha[1:] )
                        elif ha[0]=="<":
                            qhalflife= float( ha[1:] )
                        elif ha==".":
                            qhalflife= None
                        elif ha.find("u.st")>=0:
                            qhalflife= None
                        else:
                            qhalflife= float( ha )
                            #print(  li[60:64]+'.'+li[65:69] )
                        tunit=li[69:71]
                        #if  len( li[72:78].strip() )>0:
                        #    qdhalflife=float( li[72:78] )
                        #else:
                        #    qdhalflife=float( 0 )

                        if (tunit=="Gy")or(tunit=="Py")or(tunit=="Zy")or(tunit=="Ey"):
                            self.stable=True
                        self.halflife=hf_to_factor(qhalflife, tunit)
                        #print( " {} {} ... {} sec".format(qhalflife, tunit, self.halflife) )
                #===================================== END OF MY ISOTOPE


                #-------- continue with stables ----
                if IS[:3]=="IS=": # ONLY STABLES - or Gy
                    #print(li, " ::::",IS,dIS)
                    stables.append(li)
                    #------- isotopes -----
                    if Z==ZZ: # My Z
                        Zisot.append( [AA, float(IS.split("=")[1])] )
                        #print(li)
                grounds.append(li) # every [7] 0
#                if AA==A and ZZ==Z:
#                    print( mex )
        #print(Zisot)
        self.amu= (self.mex/1000.  + self.A * config.AMU_UNIT)/config.AMU_UNIT;
        #self.amu=int(self.amu*1000000)/1000000.# BAD BOY!!!
        self.abundances=Zisot
        self.avgmass=0 # calculate over ABU
        for aa,abu in Zisot:
            self.avgmass=self.avgmass+aa*abu/100.
        #https://en.wikipedia.org/wiki/Semi-empirical_mass_formula
        #if self.avgmass==0 :
        #    print("XXX Z/ZZ/A/AA: ",Z,ZZ , A, AA )
        if self.avgmass==0 and Z==43: # Tc
            self.avgmass=98
        if self.avgmass==0 and Z==61: #Pm
            self.avgmass=145
        if self.avgmass==0 and Z==84: #po
            self.avgmass=209
        if self.avgmass==0 and Z==85: #at
            self.avgmass=210
        if self.avgmass==0 and Z==86: #rn
            self.avgmass=211
        if self.avgmass==0 and Z==87: #fr
            self.avgmass=212
        if self.avgmass==0 and Z==88: #ra
            self.avgmass=226
        if self.avgmass==0 and Z==89: #ac
            self.avgmass=227
        if self.avgmass==0 and Z==91:#pa
            self.avgmass=231
        if self.avgmass==0 and Z==93:#np
            self.avgmass=237
        if self.avgmass==0 and Z==94:#pu
            self.avgmass=239
        if self.avgmass==0 and Z==95:#am
            self.avgmass=234
        if self.avgmass==0 and Z==96:#cm
            self.avgmass=245
        if self.avgmass==0 and Z==97:#bc
            self.avgmass=247
        if self.avgmass==0 and Z==98:#cf
            self.avgmass=249
        if self.avgmass==0 and Z==99:#es
            self.avgmass=252
        if self.avgmass==0 and Z==100:#fm
            self.avgmass=257
        if self.avgmass==0 and Z==101:#md
            self.avgmass=258
        if self.avgmass==0 and Z==102:#no
            self.avgmass=228
        if self.avgmass==0 and Z==103:#?????
            self.avgmass=230
        if self.avgmass==0 and Z==104:
            self.avgmass=232
        if self.avgmass==0 and Z==105:
            self.avgmass=234
        if self.avgmass==0 and Z==106:
            self.avgmass=236
        if self.avgmass==0 and Z==107:
            self.avgmass=238
        if self.avgmass==0 and Z==108:
            self.avgmass=240
        if self.avgmass==0 and Z==109:
            self.avgmass=242
        if self.avgmass==0 and Z==110:
            self.avgmass=244
        if self.avgmass==0 and Z==111:
            self.avgmass=246
        if self.avgmass==0 and Z==112:
            self.avgmass=246
        if self.avgmass==0 and Z==113:
            self.avgmass=250
        if self.avgmass==0 and Z==114:
            self.avgmass=252
        if self.avgmass==0 and Z==115:
            self.avgmass=254
        if self.avgmass==0 and Z==116:
            self.avgmass=256
        if self.avgmass==0 and Z==117:
            self.avgmass=258
        if self.avgmass==0 and Z==118:
            self.avgmass=260
        #self.avgmolarm=molarweights[Z]#
        self.molarm=molarweights[Z]# elemental
        #i think not correct:
        #self.isodensity2=densities[Z]/molarweights[Z]*self.amu

        self.eledensity=densities[Z]
        if A>0:
            self.namesrim=elements[Z].lower()+str(A)
        else:
            self.namesrim=elements[Z].lower()
        # if not found:self.name="NotExists" # but natFe
        self.gas=gaseous[Z]
        if A==1 and Z==0: #-neutron
            self.isodensity=0
            return
        if self.A > 0:
            if self.gas==1:
                self.isodensity=int((densities[Z]/self.avgmass*self.A)*10000000.)/10000000
            else:
                self.isodensity=int((densities[Z]/self.avgmass*self.A)*1000.)/1000
        else:
            # gamma e+e- ee exciton
            self.isodensity = 0
####################
        # PRINT LIST OF Z
        #print("{")
        #for k in sorted( zminmax.keys() ):
        #    print(k,":",zminmax[k],",")
        #print("}")
        ######## OTHER OFFLINE STUFF
#                #print(flo, int(li[0:3]), int(li[4:7])  , li)
#                if isfloat( flo ):
#                        massnp[ int(li[0:3]), int(li[4:7]) ] = float(flo)




    def pprint(self, prn=True):

        #global print
        #print=super_print(self.isodebug)(print)

        #print("")
        #    if az.name!="NotExists":
        if config.DEBUG: print( "D...   ISO: name={}/{}\t mex[keV]={} +- {} \tidens={} \tamu={:.8f}  \tabund={} ".format(
            self.name, self.namesrim,self.mex, self.dmex,
        self.isodensity,
#        self.isodensity2, #
        self.amu,
        self.IS
    ) )
        text=" ELM: MM={} \tavgA={:14.5f} \t dens={} \tgas={} \tabu={}".format(
        self.molarm,
        self.avgmass,
        self.eledensity,
        self.gas,
        self.abundances)
        if prn:
            if config.DEBUG:
                print("D...", text)
        #else:
        #    return text


    # works when pprint returns string
    #def __str__(self):
    #    return self.pprint(False)




################
#
# END OF CLASS #
#
################





#------------------------------ CREATE ISOTOPE RETURN CLASS INSTANCE
#------------------------------ CREATE ISOTOPE RETURN CLASS INSTANCE
#------------------------------ CREATE ISOTOPE RETURN CLASS INSTANCE
#------------------------------ CREATE ISOTOPE RETURN CLASS INSTANCE

# when  using in FIRE : return_object=False
# everywhere else :  return_object=False
#def create_fire(*args, **kwargs):
def create_fire(isotope_name_mass, debug=True):
    """
    This creates an isotope, use e.g. Ni56
    """
    #kwargs['return_object'] = False # I force DEBUG this way
    create(isotope_name_mass, debug=debug)#*args, **kwargs)
    return
    # # ======+++++++++++++++++++++ example how to create something:
    # kwargs['return_object'] = True # true mean real
    # print("abundances = {")
    # n = 0
    # for e in elements:
    #     if e == "n":
    #         continue
    #     n+=1
    #    # print( e)
    #     x = create( e )
    #     if len(x.abundances)>0:
    #         for i in x.abundances:
    #             print( f"'{e}{i[0]}' : {i[1]}, " )
    #     #if n>10:break
    # print("} # abundances")



# ===================================== USED BY CREATE_FIRE


# ============================================================
#
# ------------------------------------------------------------
def create(*args, **kwargs ):
    """
    This creates an isotope, use e.g. Ni56
    idea to return whatever   ???
    there was an idea if returns None for 4. part it is fussion... a0 z0
    """
                           # every call should explicitelly
    #DEBUG = False

    ppr = False

    return_object = True  # az object is returned by default
    if 'return_object' in kwargs: # however - if somebody wants:
        return_object = kwargs['return_object']
        ppr = return_object
        if kwargs['return_object'] == False:
            kwargs['debug'] = True # no sense otherwise

    if 'debug' in kwargs: #
        if kwargs['debug'] == True:
            config.DEBUG = True

    #global print
    if 'debug' in kwargs:
        #print=super_print(kwargs['debug'])(print)
        ##print("debug==", kwargs)
        ##print("=================+++",kwargs)
        ppr = kwargs['debug']
    else: # NO DEBUG - means object should be back
        ##print("no debug given")
        #print=super_print(False)(print)
        pass

    #A==0 ... nat
    #if DEBUG:print(" D... isotope arguments=",args)
    A,Z,N=0,0,None
    if len(args)==0:
        print("X... NO ARGUMENT given, try Ni56")
        return None


    # STRANGE ----
    if args[-1]=="pprint":
        ppr=True
        args=args[:-1]


    # manually care about neutron HERE
    if (args[0]=="n1") or (args[0]=="1n"):
        A,z,N=1,0,1
    elif len(args)==2:
        if isint(args[0]) and isint(args[1]):
            A,Z=int(args[0]),int(args[1])
            if Z>A: A,Z=Z,A
            N=A-Z
            if Z==0 and A>1:
                # jsut some errro
                return None
    elif len(args)==1 and isint(args[0]):
        A,Z=0, int(args[0])
    elif len(args)==1: # 22Ne 22ne  ne    ne22
        name=args[0]
        for i in range(len(args[0])):
            if not isint( args[0][i]):break
        if i>0: # ----22ne
            A=int(args[0][:i])
            Zb=args[0][i:].capitalize()
        else: #--try numbers from backside
            for i in range(len(args[0])-1,-1,-1):
                if not isint( args[0][i]):break
            if i!=len(args[0])-1: # ---ne22
                A=int( args[0][i+1:])
                Zb=args[0][:i+1].capitalize() # search index
            else:
                Zb=args[0].capitalize() # search index
                A=0  # ?
        try:
            Z=elements.index( Zb )
        except:
            Z=999
        if not A==0:
            N=A-Z

    #---- combine name ---knowing A and Z MAYBE FOR FUSSION???? :)))
    if A==0 and Z==0:
        print("i... 0 0  element doesnt exist, fussion? e+e- (ee) ? gamma ?")
        az = Isotope(0, 0, "exciton" )
        return az #None
    if (Z < 0) or (A < 0):
        print(f"i... {A} {Z}   element doesnt exist, None")
        #az = Isotope(0, 0, "exciton" )
        return None

    #----  -----------------------
    if Z>len(elements):
        print(f"X... element {Z} doesnt exist")
        return None
    # A is not molarmass
    #if A==0:A=molarweights[Z]
    #if isint(A):
    if A!=0:
        name=str(A)+elements[Z]
    else:
        name="nat"+elements[Z]

    #------------  HERE I HAVE Element and A,Z ---I define NAME!
    if 'debug' in kwargs:
        #print("D...   debug given", kwargs)
        az=Isotope(A,Z,name, debug=kwargs['debug'])
    else:
        az=Isotope(A,Z,name, debug=False)
    if ppr:   # same as debug now
        #print("printing start")
        az.pprint()
        #print("pprinting done")
    #print(" D... isotope generated", az)
    if return_object:
        return az
    print("i... nothing returned from the function")



def test_create():
     i=create("C")
     assert i.name=="natC"
     i=create(6)
     assert i.name=="natC"
     i=create(16,8)
     assert i.name=="16O"
     j=create("16O")
     assert j.name=="16O"
     j=create("22ne")
     assert j.name=="22Ne"
     j=create("ne")
     assert j.name=="natNe"
     j=create("NE")
     assert j.name=="natNe"
     j=create("1n") # neutron problem
     assert j.name=="1n"
     j=create("n1")
     assert j.name=="1n"
     j=create("n14") # srim notation
     assert j.name=="14N"
     j=create()
     assert j==None





def createmore(*args):
    outl=[]
    for i in args:
        outl.append( create(i) )
    return outl



def test_createmore():
    o16,h2,f19,h1,f20=createmore("o16","h2","f19","h1","f20")
    assert o16.name=="16O"
    assert f20.name=="20F"
    assert h2.name=="2H"
    assert h1.name=="1H"



# def createall( maxz=34 ):
#     #DB_FILE = pkg_resources.resource_filename('nuphy2',
#     #                                          'data/nubase2016.txt')
#     #with open(DB_FILE) as f:
#     #    masstable=f.read().strip()
#     #masslist=masstable.split('\n')
#     zmm={}
#     for li in masslist:
#         if ( li[7] is '0' ):
#             #-------- only ground states ..."0"
#             AA,ZZ=int(li[:3]),int(li[4:7])
#             if not ZZ in zmm:
#                 zmm[ZZ]=[]
#             if li[24]!="#" and ZZ<maxz:
#                 zmm[ZZ].append(AA)
#                 #mex=float( li[17:24]+'.'+li[25:29] )
#             #print( li[24] )
#     #print(zmm.keys())
#     for k in zmm.keys():
#         for i in zmm[k]:
#             a=create( i, k)
#             foo = a.namesrim
#             #print(foo)
#             globals()[foo]=a
#             #print(".")
#     o16.pprint()

#=========================================================

if __name__=="__main__":
    #if DEBUG:
    #print("D... in main of project/module:  nuphy2/isotope ")
    #if DEBUG:print("D... version :", __version__ )
    Fire({"cr":create_fire
    }
    )

    # #print("gaseous=[", end="")
    # for i in range(len(densities)):
    #     if densities[i]<0.1: g=1
    #     else: g=0
    #     print(g,gaseous[i],elements[i],densities[i] )
    #     #print(g,",", end="" )
    # #print("]")
