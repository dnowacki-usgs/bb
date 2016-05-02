#!/usr/bin/env python

# Generate SWAN .swn input file

import argparse
import math
import imp
import os
import sys

parser = argparse.ArgumentParser(description='Generate a SWAN .swn file')
parser.add_argument("--cfgfile")
parser.add_argument("--outfile")

args = parser.parse_args()

if not (args.cfgfile or args.outfile):
    parser.error("--cfgfile and --outfile both required")

# need to import this way to get it from directory it is called from, 
# not from the directory where the binary is

bname = os.path.splitext(os.path.basename(args.cfgfile))[0]
runargs = imp.load_source(bname, args.cfgfile)

# get the run number from the path. this might be dangerous, but oh well
# lastdir = os.path.basename(os.path.normpath(os.getcwd()))
# runno = lastdir[-2:]

f = open(args.outfile, 'w')

print >>f,  """PROJECT 'BB' ' '
 'Barnegat Bay'
 'Bathymetry: from BB terrain model'
 'Stationary mode'

MODE STATIONARY TWODIMENSIONAL
"""

f.write("SET LEVEL " + str(runargs.level) + " DEPMIN 0.10 INRHOG 1 NAUTICAL\n\n")

print >>f, """CGRID REGULAR 548272 4366217 0.0 36800 77730 735 1554 36 0.04 3.0

INPGRID BOTTOM REGULAR 548272 4366217 0 735 1554 50 50
READINP BOTTOM 1 '../bb_z2.bot' 1 0 FREE

"""

f.write("WIND " + str(runargs.wind_speed) + " " + str(runargs.wind_dir) + " \n\n")

f.write("\n")

f.write("$ Vegetation\n")

if runargs.veg_on == True:
    
    
    f.write("READINP NPLANTS 1 '../bb_wetl_ext.ext' 1 0 FREE\n")
    
    if not hasattr(runargs, 'veg_height'):
        runargs.veg_height = 1.0
    if not hasattr(runargs, 'veg_diam'):
        runargs.veg_diam = 0.015
    if not hasattr(runargs, 'veg_nstems'):
        runargs.veg_nstems = 400
    if not  hasattr(runargs, 'veg_drag'):
        runargs.veg_drag = 1.0
    
    print "Drag:", runargs.veg_drag
    
    f.write("VEGETATION " + str(runargs.veg_height) + " " + str(runargs.veg_diam) + " " + \
        str(runargs.veg_nstems) + " " + str(runargs.veg_drag) + "\n\n")

f.write("$ Physics\n")
f.write("GEN3 AGROW\n")
f.write("BREAK\n")
f.write("WCAP\n")
f.write("TRIAD\n\n")

if runargs.friction_on == True:
    if runargs.friction_type == 'Madsen':
        f.write("FRICTION MADSEN " + str(runargs.madsen_kn) + "\n")
    elif runargs.friction_type == 'Collins':
        f.write("FRICTION COLLINS " + str(runargs.collins_cfw) + "\n")
    elif runargs.friction_type == 'JONSWAP':
        f.write("FRICTION JONSWAP CONSTANT " + str(runargs.jonswap_cfjon) + "\n")
    elif runargs.friction_type == 'RIPPLES':
        f.write("FRICTION RIPPLES " + str(runargs.ripples_diam) + "\n")

# f.write("FRICTION JONSWAP CONSTANT 0.18\n")
        
print >>f,  """$ Output

BLOCK 'COMPGRID' NOHEADER 'hsig.nc' LAY 3 HSIG 1.
BLOCK 'COMPGRID' NOHEADER 'tm01.nc' LAY 3 TM01 1.
BLOCK 'COMPGRID' NOHEADER 'wlen.nc' LAY 3 WLEN 1.
BLOCK 'COMPGRID' NOHEADER 'ubot.nc' LAY 3 UBOT 1.
BLOCK 'COMPGRID' NOHEADER 'botlev.nc' LAY 3 BOTLEV 1.
BLOCK 'COMPGRID' NOHEADER 'xp.nc' LAY 3 XP 1.
BLOCK 'COMPGRID' NOHEADER 'yp.nc' LAY 3 YP 1.
SPECOUT 'COMPGRID' SPEC2D ABS 'spec.nc' 
$ Can't use NetCDF for some variables
BLOCK 'COMPGRID' NOHEADER 'nplant.mat' LAY 3 NPLANT 1.
BLOCK 'COMPGRID' NOHEADER 'dissip.mat' LAY 3 DISSIP 1.
BLOCK 'COMPGRID' NOHEADER 'disbot.mat' LAY 3 DISBOT 1.
BLOCK 'COMPGRID' NOHEADER 'diswcap.mat' LAY 3 DISWCAP 1.

$ Computation
TEST 1,0
PROP BSBT
NUMERIC STOPC NPNTS 98.0
COMPUTE

STOP
"""

f.close()