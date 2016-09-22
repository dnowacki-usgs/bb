#!/usr/bin/env python

import os

n = 1

for level in [0.0, 0.5, 1.0, 1.5]:
    for veg_on in [True, False]:
        for wind_speed in [5, 10, 15]:
            for wind_dir in [0, 45, 90, 135, 180, 225, 270, 315]:    
    
                directory = 'run' + str(n).zfill(3)
                if not os.path.exists(directory):
                    os.makedirs(directory)
        
                print level, veg_on, wind_speed, wind_dir, directory
                f = open(directory + '/runargs.py', 'w')
    
                
                f.write("level = " + str(level) + "\n")
                f.write("wind_speed = " + str(wind_speed) + "\n")
                f.write("wind_dir = " + str(wind_dir) + "\n")
                f.write("veg_on = " + str(veg_on) + "\n")
                f.write("friction_on = True\n")
                f.write("friction_type = \"Madsen\"\n")
                f.write("madsen_kn = 0.0015\n")
            
                f.close()
    
                n = n + 1
