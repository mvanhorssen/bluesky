#functions_alexander.py

import numpy as np


kts 	= 0.514444 # m/s  1 knot
ft  	= 0.3048  # m     1 foot
fpm 	= ft/60. # feet per minute
inch 	= 0.0254 # m     1 inch
nm  	= 1852. # m       1 nautical mile
lbs 	= 0.453592 # kg  pound mass
g0  	= 9.80665 # m/s2    Sea level gravity constant
R   	= 287.05 # Used in wikipedia table: checked with 11000 m 
p0 		= 101325. # Pa     Sea level pressure ISA
rho0 	= 1.225 # kg/m3  Sea level density ISA
T0   	= 288.15 # K   Sea level temperature ISA
gamma 	= 1.40 # cp/cv for air
Rearth 	= 6371000.  # m  Average earth radius
Tstrat 	= 216.65 # K Stratosphere temperature ISA (Alexander)

def vtempA(alt):         # hinput [m]; in Kelvin
# Temp
    T = np.maximum(T0-0.0065*alt,Tstrat)

    return T

def vvsoundA(hinput):  # Speed of sound for given altitude h [m]; in m/s
    T = vtempA(hinput)
    a = np.sqrt(gamma*R*T)
    return a
    
def vmach2tasA(M,h): # true airspeed (tas) to mach number conversion
    a = vvsoundA(h)
    tas = M*a
    return tas
    
def kts2mpers(a):
    b=0.51444*float(a)
    return b
    
def mpers2kts(a):
    b=float(a)*1.94384449
    return b
    
def vtas2casA(tas,h):  # tas2cas conversion both m/s
    p,rho,T = vatmosA(h)
    qdyn    = p*((1.+rho*tas*tas/(7.*p))**3.5-1.)
    cas     = np.sqrt(7.*p0/rho0*((qdyn/p0+1.)**(2./7.)-1.))
    return cas
    
def vatmosA(alt): # alt in m

# Temp
    T = np.maximum(T0-0.0065*alt,Tstrat)

# Density
    rhotrop = rho0*(T/T0)**4.256848030018761 
    dhstrat = np.maximum(0.,alt-11000.)

    rho = rhotrop*np.exp(-dhstrat/(R*Tstrat/g0)) # = *g0/(287.05*216.65))

# Pressure
    p = rho*R*T

    return p,rho,T    

def vcas2tasA(cas,h):  #cas2tas conversion both m/s 
    p,rho,T = vatmosA(h)
    qdyn    = p0*((1.+rho0*cas*cas/(7.*p0))**3.5-1.)
    tas     = np.sqrt(7.*p/rho*((1.+qdyn/p)**(2./7.)-1.))
    return tas
 
def determine_cruise_TAS_CAS(TAS_cruise,M_cruise,h_cruise): #h in feet, TAS in kts; Calculate which is the cruise CAS to be inserted, such that neither the CAS nor M is violated
    alt=h_cruise*ft #h in feet, alt in m
    TAS_mps=vmach2tasA(M_cruise,alt)
    TAS_kts =mpers2kts(TAS_mps)
    
    calculated_cruise_TAS_kts=min(TAS_cruise,TAS_kts) 
    calculated_cruise_TAS_mps=kts2mpers(calculated_cruise_TAS_kts)
    
    calculated_cruise_CAS_kts=mpers2kts(vtas2casA(calculated_cruise_TAS_mps,alt))
    
    return calculated_cruise_TAS_kts,calculated_cruise_CAS_kts   

def veas2tasA(eas,h):   # equivalent airspeed to true airspeed
    rho = vdensityA(h)
    tas = eas*np.sqrt(rho0/rho)
    return tas
 
def vdensityA(alt):   # air density at given altitude h [m]
    p,r,T = vatmosA(alt)
    return r  
