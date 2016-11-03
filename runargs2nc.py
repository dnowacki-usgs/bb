#!/usr/bin/env python

import netCDF4
import os
import imp
from pylab import genfromtxt

# get the run configuration
bname = os.path.splitext(os.path.basename("runargs.py"))[0]
runargs = imp.load_source(bname, "runargs.py")

rg = netCDF4.Dataset('runargs.nc', 'w', format='NETCDF4')

acc = genfromtxt("ACCURACY.txt")

for d in dir(runargs):
    if '__' not in d: 
        at = getattr(runargs, d)
        t = type(at)
	print d, t, at
        if t is bool:
            setattr(rg, d, str(at))
        else:
            setattr(rg, d, at)
#        setattr(rg, d, getattr(runargs, d))
        #print getattr(runargs, d), type(getattr(runargs, d))
	#print type(getattr(runargs, d)) is bool

setattr(rg, 'accuracy', acc[1])

rg.close()
