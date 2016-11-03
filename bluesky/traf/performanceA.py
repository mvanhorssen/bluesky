#performanceA.py
import numpy as np
###########################################################################
#Nominal Parameters

#Based on B747 - KLM - LVNL's TP
nom_climb=250. # [kts] climb speed CAS
nom_cruise_M=0.85 # [-] cruise speed Mach
nom_cruise_spd=510. # [kts] cruise speed TAS
nom_CAS_TOD_almost_IAF=286. # [kts] descent speed CAS
nom_CAS_almostIAF_IAF=250. # [kts] descent speed CAS


nom_CAS_IAF_FAF=225. # [kts] descent speed CAS
nom_CAS_FAF_RWY=158. # [kts] descent speed CAS

###########################################################################
#Minimum flying speeds

#Assumed 10% speed reduction where possible
speed_reduction = 0.9

min_climb=nom_climb*1. # No speed reductions during climb
min_cruise_M=nom_cruise_M*speed_reduction #10% speed reduction possible (judgement)
min_cruise_spd=nom_cruise_spd*speed_reduction #10% speed reduction possible (judgement)
min_CAS_TOD_almost_IAF=nom_CAS_TOD_almost_IAF*speed_reduction #10% speed reduction possible (judgement)
min_CAS_almostIAF_IAF=nom_CAS_almostIAF_IAF*speed_reduction #10% speed reduction possible (judgement)

min_CAS_IAF_FAF=nom_CAS_IAF_FAF #Project assumption: no delay absorption in TMA
min_CAS_FAF_RWY=nom_CAS_FAF_RWY #Project assumption: no delay absorption in TMA
###########################################################################
CAS_holding=min_CAS_almostIAF_IAF #CAS speed in holding
###########################################################################

CD_0=0.019945 #[BADA]
CD_2=0.049033 #k [BADA]
WingSurface=511.23 #Wing surface [BADA]
mass_nominal=285700. #Nominal mass [BADA] 
###########################################################################
