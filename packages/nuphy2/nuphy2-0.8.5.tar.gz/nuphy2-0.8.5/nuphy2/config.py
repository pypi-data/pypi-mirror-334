#!/usr/bin/env python3

import sys # print stderr

from fire import Fire

from fire import Fire
from nuphy2.version import __version__

DEBUG = False
# AMU_UNIT = 931.49403 #I HAD AN ERROR !!!!!!
# https://physics.nist.gov/cgi-bin/cuu/Value?muc2mev
#
AMU_UNIT = 931.49410372  # + -0.000 000 29


def main():
    print(f"i... config")

if __name__ == "__main__":
    Fire(main)
