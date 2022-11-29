import sys
import os
import requests
import math
import numpy as np
from numpy import linalg as LA
from sgp4.api import Satrec
from sgp4.api import jday
from sgp4.api import days2mdhms
from matplotlib import pyplot as plt

##########################################################################################################
# UT1-UTC

# retrieving UTC times data points
JD_sat=np.loadtxt('JD.dat')

# retrieving conversion data for UTC > UT1 conversion
if (os.path.isfile('./convTable.dat'))==False:
    r = requests.get("https://maia.usno.navy.mil/ser7/finals2000A.daily", allow_redirects=True)
    open('convTable.dat', 'wb').write(r.content)

# iterating on tabulated data to retreive error
error=np.zeros(np.size(JD_sat))
for i in range (np.size(JD_sat)):
    flag=0
    file=open('convTable.dat', 'r')
    while flag==0:
        line=file.readline()
        # print(line[7:15])
        JD=float(line[7:15])+2400000.5
        error[i]=float(line[58:68])
        if JD==JD_sat[i]:
            flag=1
            file.close()
np.savetxt('error.dat', error) # error between UTC and UT1 (in seconds) for each julian date in the input file
plt.plot(JD_sat,error)
plt.savefig('UT1-UTC_error.jpg')

##########################################################################################################

# LEAP SECONDS

# retrieving data for UTC > GPS conversion
if (os.path.isfile('./leapSeconds.dat'))==True:
    file=open('leapSeconds.dat', 'r')
else:
    r = requests.get("https://maia.usno.navy.mil/ser7/tai-utc.dat", allow_redirects=True)
    open('leapSeconds.dat', 'wb').write(r.content)
    file=open('leapSeconds.dat', 'r')

# retrieving total time discrepancy with GPS
last_line=file.readlines()[-1]
time_diff=(float(last_line[38:49])-19)+((JD_sat[i]-2400000.5-float(last_line[59:65]))*float(last_line[72:79]))
print('The time discrepancy with GPS is: ', time_diff, 's')
