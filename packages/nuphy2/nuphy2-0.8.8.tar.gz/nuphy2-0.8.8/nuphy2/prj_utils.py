#!/usr/bin/env python3
"""
This is a package to:
 -  systematically load data that are localy here.
 -  replace print function to
     - remove debug  D...
     - print i... stuff to stderr
     - ...
"""

# deprecated
# import pkg_resources  # to be able to read data in package
# better
import importlib_resources


from fire import Fire
import sys
import builtins as __builtin__



class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def fail(t):
    print("")
    print(t)
    sys.exit()

def get_file_path(filename, pkg="nuphy2"):
    """
    returns full path to data stored in nuphy2/data
    """
    # print("D... ",pkg)
    # this retuns like string, BUT TYPE is important
    #par = pkg_resources.Requirement.parse( pkg )
    #print("D... par=", par) # for nuphy2 returns "nuphy2"
    #print("parse_package=",par,type(par),"      search_filename=",filename)
    #ret = pkg_resources.resource_filename(par,
    #                                    'data/'+filename )
    #print("D... pkgresource=", ret)
    ret = importlib_resources.files("nuphy2").joinpath("data/"+filename)
    return ret



def super_print(debug=True):
    '''filename is the file where output will be written'''
    def wrap(func):
        '''func is the function you are "overriding", i.e. wrapping'''
        def wrapped_func(*args,**kwargs):
            '''*args and **kwargs are the arguments supplied
            to the overridden function'''

            #use with statement to open, write to, and close the file safely
            #with open(filename,'a') as outputfile:
            #    outputfile.write(*args,**kwargs)
            #now original function executed with its arguments as normal

            if len(args)>0:
                #print(type(args[0]), args[0])
                if (isinstance(args[0], str)) and (args[0].find("D...")>=0):
                    if not debug:
                        return
            if 'file' in kwargs:
                __builtin__.print(*args, **kwargs )
            else:
                __builtin__.print(*args, **kwargs, file=sys.stderr)
            return #func(*args,**kwargs)
        return wrapped_func
    return wrap

#USE AS print = super_print('output.txt')(print)
#     print = super_print('output.txt')(print)





if __name__=="__main__":
    Fire(get_file_path)
