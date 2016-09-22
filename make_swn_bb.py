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

rundir = os.path.basename(os.path.normpath(os.getcwd()))

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

print >>f, """CGRID REGULAR 548297 4366242 0.0 36750 77700 735 1554 36 0.04 3.0

INPGRID BOTTOM REGULAR 548297 4366242 0 735 1554 50 50 EXC 23.5811
READINP BOTTOM 1 '../bbtg10m_50x50_te.bot' 1 0 FREE

"""

f.write("WIND " + str(runargs.wind_speed) + " " + str(runargs.wind_dir) + " \n\n")

f.write("\n")

f.write("$ Vegetation\n")

if runargs.veg_on == True:
    
    f.write("READINP NPLANTS 1 '../bb_wetext_50m.wet' 1 0 FREE\n")
    # use mildly smooth wetland extent
    # f.write("READINP NPLANTS 1 '../bb_wetext_50m_5x5.wet' 1 0 FREE\n")
    
    if not hasattr(runargs, 'veg_height'):
        runargs.veg_height = 0.25
    if not hasattr(runargs, 'veg_diam'):
        runargs.veg_diam = 0.015
    if not hasattr(runargs, 'veg_nstems'):
        runargs.veg_nstems = 821
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
        
f.write("$ Output\n")

f.write("SPECOUT 'COMPGRID' SPEC1D ABS '/clay/usgs/users/dnowacki/bb/" + rundir + "/spec.nc' \n")

f.write("BLOCK 'COMPGRID' NOHEADER '/clay/usgs/users/dnowacki/bb/" + rundir + "/hsig.nc' LAY 3 HSIG 1. \n")
f.write("BLOCK 'COMPGRID' NOHEADER '/clay/usgs/users/dnowacki/bb/" + rundir + "/tm01.nc' LAY 3 TM01 1. \n")
f.write("BLOCK 'COMPGRID' NOHEADER '/clay/usgs/users/dnowacki/bb/" + rundir + "/wlen.nc' LAY 3 WLEN 1. \n")
f.write("BLOCK 'COMPGRID' NOHEADER '/clay/usgs/users/dnowacki/bb/" + rundir + "/ubot.nc' LAY 3 UBOT 1. \n")
f.write("BLOCK 'COMPGRID' NOHEADER '/clay/usgs/users/dnowacki/bb/" + rundir + "/botlev.nc' LAY 3 BOTLEV 1. \n")
f.write("$ BLOCK 'COMPGRID' NOHEADER '/clay/usgs/users/dnowacki/bb/" + rundir + "/xp.nc' LAY 3 XP 1. \n")
f.write("$ BLOCK 'COMPGRID' NOHEADER '/clay/usgs/users/dnowacki/bb/" + rundir + "/yp.nc' LAY 3 YP 1. \n")

f.write("$ Can't use NetCDF for some variables \n")

f.write("BLOCK 'COMPGRID' NOHEADER '/clay/usgs/users/dnowacki/bb/" + rundir + "/nplant.mat' LAY 3 NPLANT 1. \n")
f.write("BLOCK 'COMPGRID' NOHEADER '/clay/usgs/users/dnowacki/bb/" + rundir + "/dissip.mat' LAY 3 DISSIP 1. \n")
f.write("BLOCK 'COMPGRID' NOHEADER '/clay/usgs/users/dnowacki/bb/" + rundir + "/disbot.mat' LAY 3 DISBOT 1. \n")
f.write("BLOCK 'COMPGRID' NOHEADER '/clay/usgs/users/dnowacki/bb/" + rundir + "/diswcap.mat' LAY 3 DISWCAP 1. \n")

print >>f, """$ Computation
TEST 1,0
PROP BSBT
NUMERIC STOPC NPNTS 98.0
COMPUTE

STOP
"""

f.close()
