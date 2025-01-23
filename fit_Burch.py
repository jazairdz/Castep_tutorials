#!/usr/bin/python3
# Matt Probert 21/02/2017

# simple script to load a text file of Vol (A^3) vs E (eV)
# and do a Burch-Murnaghan EOS fit

from scipy.optimize import leastsq
import numpy as np
import matplotlib.pyplot as plt
import sys

#get EV filename and load data - file must be 2 columns containing volume and energy
fname=input('Enter name of (vol,energy) file to load : ')
#fname=sys.argv[1]
vols, energies = np.loadtxt(fname,unpack=True)

#initial values [E0, B0, B', V0] from starting point as a basic guess
param0 = [ energies[0], 200, 2.0, vols[0]]

def Murnaghan(params, vol):    #EOS from Phys. Rev. B 28, 5480 (1983)
    E0, B0, BP, V0 = params    #unpack params
    E = E0 + B0 * vol / BP * (((V0 / vol)**BP) / (BP - 1) + 1) - V0 * B0 / (BP - 1.0)
    return E

def residuals(pars, y, x):
    res =  y - Murnaghan(pars, x)
    return res

#do the non-linear fit
params,success = leastsq(residuals, param0, args=(energies, vols))
if (not success):
    print('Failed to fit Burch-Murnaghan curve')
    exit()

#standard CASTEP units has V in ang^3 and E in eV
#and B=V*d2E/dV^2 so convert to SI B->B*1.602E-19/10E-30 = B*1.602E11 Pa = B*1.602E2 GPa

print("Burch-Murnaghan fit parameters:")
print("E0 = %10.4f eV"%(params[0]))
print("B0 = %10.4f eV.ang^-3"%(params[1]))
print("B' = %10.4f "%(params[2]))
print("V0 = %10.4f ang^3"%(params[3]))
print("")
print("Bulk modulus = %10.4f GPa"%(params[1]*1.602E2))
print("")
print("Graph of data and fit saved as BM_curve.png - please check all is OK")

#plot the raw data and fitted curve on top to file as a cross-check
plt.plot(vols,energies, 'ro')

x = np.linspace(min(vols), max(vols), 50)
y = Murnaghan(params, x)
plt.plot(x, y, 'k-')

plt.xlabel('Volume')
plt.ylabel('Energy')
plt.savefig('BM_curve.png')

print("Plot of fit saved as BM_curve.png")

