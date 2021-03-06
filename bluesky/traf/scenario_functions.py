#scenario_functions.py
import numpy as np
from math import *
from ..tools.aero import *
from ..tools.geo import rwgs84, qdrdist
import random

def FlightInfo(FlightID,lines):
    segments=[]
    origin=[]
    destination=[]
    actype=[]
    timeb=[]
    FLb=[]
    CallSign=[]
    Dateb=[]
    LATb=[]
    LONb=[]
    Sequence=[]
    
    for line in lines:
        item=line.strip().split(" ")
        if item[16].strip()==FlightID:
            segments.append(item[0].strip().upper())
            origin.append(item[1].strip().upper())
            destination.append(item[2].strip().upper())
            actype.append(item[3].strip().upper())
            timeb.append(item[4].strip().upper())
            FLb.append(item[6].strip().upper())
            CallSign.append(item[9].strip().upper())
            Dateb.append(item[10].strip().upper())
            LATb.append(minutedecimale2degree(float(item[12].strip().upper()))) # Degree
            LONb.append(minutedecimale2degree(float(item[13].strip().upper()))) # Degree
            Sequence.append(item[17].strip().upper())
    return segments,origin,destination,actype,timeb,FLb,CallSign,Dateb,LATb,LONb,Sequence    

def find_TMAroute(TMAroutesfilecontent,IAF,runway): # 1 runway assigned to 1 IAF 
    TMAroute=[] 
    for line in TMAroutesfilecontent:
            item=line.strip().split(",")
        
            if item[0]==IAF and item[1]==runway:
                item1=item[2]
                item2=item1.strip().split("-")
                for z in range(len(item2)):
                    TMAroute.append(item2[z])
    return TMAroute # In order of IAF-runway vector
   
def obtain_TMAwpt_data(wptname,wptdatabasecontent):
    wptLAT=[]
    wptLON=[]    
    
    for line in wptdatabasecontent:
        item=line.strip().split(",")
              
        if item[0].strip().upper()==wptname:
            if item[6].strip().upper()=='NL' or item[6].strip().upper()=='BE' or item[6].strip().upper()=='UK' or item[6].strip().upper()=='GM': # Check that waypoint in NL, BE, UK or GM (to be relevant)
                wptLAT=item[2].strip().upper()
                wptLON=item[3].strip().upper()                

                break 
           
    return wptLAT,wptLON

def obtain_apt_data(airport,airportdatabasecontent):
    aptLAT=[]
    aptLON=[]    
    
    for line in airportdatabasecontent:
        item=line.strip().split(",")
              
        if item[0].strip().upper()==airport:
                aptLAT=item[2].strip().upper()
                aptLON=item[3].strip().upper()                
   
    return aptLAT,aptLON       

class Route_outside_TMA:
    def __init__(self):
        self.waypoints=[] # List of all waypoints
        self.LAT=[] # Latitude of each waypoint
        self.LON=[] # Longitude of each waypoint
        self.FL=[] # Altitude at each waypoint
        self.spd=[] # CAS
        self.spd_TAS=[] # TAS
        self.whichIAF=[] # IAF
        self.IAF_LAT=[] # IAF latitude
        self.IAF_LON=[] # IAF longitude
        self.whichRWY=[] # RWY
        self.almostIAF=[] # Almost IAF
        self.almostIAF_LAT=[] # Almost IAF latitude
        self.almostIAF_LON=[] # Almost IAF longitude
        self.dist=[] # Distance in between waypoints
        self.heading=[] # Heading between waypoints
        self.totdist=[] # Total distance to RWY
        self.dist_to_IAF=[] # Total distance to IAF
        self.flpathangle=[] # Flight path angle [deg]
        self.phase=[] # Phase of flight (climb, cruise, descent)
        self.loc=[] # Location of aircraft (before or after TOD)
        self.estFT=[] # Estimated flying time (per leg)
        self.totestFT=[] # Total estimated flying time outside TMA
        self.estFT_to_CBAS=[] # Estimated flying time to CBAS, per waypoint
        self.estFT_to_IAF=[] # Estimated flying time to IAF, per waypoint
        self.estFT_to_RWY=[] # Estimated flying time to RWY, per waypoint
        self.directdist_RWY=[] # Direct distance to runway        
        self.minspd=[] # Minimum CAS that can be flown
        self.minspd_TAS=[] # Minimum TAS that can be flown        
        self.estmaxFT=[] # Maximum flying time per leg (minimum speed)
        self.totestmaxFT=[] # Total maximum flying time outside TMA (minimum speed)
        self.estmaxFT_to_IAF=[] # Maximum flying time to IAF, per waypoint
        self.estmaxFT_to_RWY=[] # Maximum flying time to RWY, per waypoint        
        self.maxposs_spddelabs_segment=[] # Maximum delay that can be absorbed by speed reduction (flying at minimum speed) w.r.t. nominal speed, per segment
        self.maxposs_spddelabs_to_IAF=[] # Maximum delay until IAF that can be absorbed by speed reduction (flying at minimum speed) w.r.t. nominal speed, per segment
        self.maxposs_spddelabs_to_RWY=[] # Maximum delay until RWY that can be absorbed by speed reduction (flying at minimum speed) w.r.t. nominal speed, per segment
        self.maxposs_spddelabs_total=[] # Total maximum delay that can be absorbed by speed reduction (flying at minimum speed) w.r.t. nominal speed
        self.estminFT=[] # Minimum FT per leg
        
    def addwpt(self,wptname,wptLAT,wptLON,wptFL):
        self.waypoints.append(wptname)
        self.LAT.append((wptLAT)) # Degree
        self.LON.append((wptLON)) # Degree
        self.FL.append(wptFL)
		
    def calc_dist_and_heading(self):
        for k in range(len(self.waypoints)):
           if k<(len(self.waypoints)-1):
               self.dist.append(qdrdistA(self.LAT[k],self.LON[k],self.LAT[k+1],self.LON[k+1]))
               
               temp1,temp2=qdrdist(self.LAT[k],self.LON[k],self.LAT[k+1],self.LON[k+1])            
               if temp1<0:
                    temp1=temp1+360.
               self.heading.append(temp1)                    
               del temp1,temp2
                
        self.totdist=np.sum(self.dist) 
       
        for k in range(len(self.waypoints)):
           if k==0:
               self.dist_to_IAF.append(self.totdist)
           elif k>0: 
               self.dist_to_IAF.append(self.dist_to_IAF[-1]-self.dist[k-1])
               
    def delete_tooshort_legs(self):
        for k in range(len(self.waypoints)):
            if k<(len(self.waypoints)-1) and k>0: # Never delete first waypoint
                if (self.dist[k]<3. or (self.dist[k]<8. and (abs(self.heading[k]-self.heading[k-1])>40.))) and self.waypoints[k] != 'WPT_CBAS' and self.waypoints[k] != 'WPT_almost_IAF':
                    del self.waypoints[k]
                    del self.LAT[k]
                    del self.LON[k]
                    del self.FL[k]
                    
        del self.totdist
        self.dist_to_IAF=[]
         
        self.dist=[]
        self.heading=[]
		
    def findFlightPathAngle(self):
        for k in range(len(self.waypoints)):        
            if k<(len(self.waypoints)-1):            
                self.flpathangle.append((180./np.pi)*np.arctan(((float(self.FL[k+1])-float(self.FL[k]))*100*ft)/(self.dist[k]*nm)))
            if k==(len(self.waypoints)-1):
                self.flpathangle.append(-300.0) # Random (wrong) value
                
    def delwpts_fromIAFonwards(self,idx):
        del self.waypoints[idx:]
        del self.LAT[idx:]
        del self.LON[idx:]
        del self.FL[idx:]
        del self.dist[idx:]
        del self.heading[idx:]
        del self.flpathangle[idx:]
     
    def findIAF(self,possible_IAFs):
        for k in range(len(possible_IAFs)):
            if possible_IAFs[k] in self.waypoints:
                self.whichIAF=possible_IAFs[k]
                
                idx=self.waypoints.index(self.whichIAF)
                self.IAF_LAT=self.LAT[idx]
                self.IAF_LON=self.LON[idx]
        
    def findalmostIAF(self):
        self.almostIAF=self.waypoints[-1]
        self.almostIAF_LAT=self.LAT[-1]
        self.almostIAF_LON=self.LON[-1]
        
    def findRWY(self,IAF,possible_IAFs,possible_runways,j):
        idx=possible_IAFs.index(IAF)
        
        if len(possible_runways[idx])<4: # Only 1 runway used by IAF
            self.whichRWY=possible_runways[idx]
        else: # Dynamic runway assignment
            temporrunways=possible_runways[idx]
            temporindex=temporrunways.index('-')
            # Determine which runways used by IAF
            runway1tempor=temporrunways[:temporindex]
            runway2tempor=temporrunways[(temporindex+1):]

            # Randomly assign runway            
            if j%2==0:
                temporfinalrunwayselection=runway1tempor
            elif j%2==1:
                temporfinalrunwayselection=runway2tempor
                
            self.whichRWY=temporfinalrunwayselection
            
            del temporindex,runway1tempor,runway2tempor,temporrunways,temporfinalrunwayselection
 
    def findPhase(self): 
         default='Ground'
         
         for j in range(len(self.waypoints)):
             if default=='Ground' and self.flpathangle[j]>0:
                 default='Climb'
               
             if (default=='Climb' and float(self.FL[j])>200) or (np.abs(self.flpathangle[j])<0.3 and default!='Descent'):
                 default='Cruise'
                 
             if j<(len(self.waypoints)-1):    
                 if default=='Cruise' and float(self.FL[j+1])<300 and self.flpathangle[j]<0.:
                     default='Descent'
                
             self.phase.append(default)
            
    def findLocation(self):
        default='BeforeTOD'
    
        for j in range(len(self.waypoints)):
            if default=='BeforeTOD' and self.phase[j]=='Descent':
                default='TOD_almostIAF'
            
            if self.waypoints[j]==self.almostIAF:
                default='AlmostIAF_IAF'
        
            self.loc.append(default)
	
    def calculate_Speeds(self,nom_climb,nom_cruise_M,nom_cruise_spd,nom_CAS_TOD_almost_IAF,min_climb,min_cruise_M,min_cruise_spd,min_CAS_TOD_almost_IAF): 
        for j in range(len(self.waypoints)):
            if j==0:
                # Nominal speed
                speed=nom_climb # First waypoint: climb speed
                alt = 0.5*(float(self.FL[j])+float(self.FL[j+1]))*100.*ft
                speed2=mpers2kts(vcas2tas(kts2mpers(speed),alt)) # Speed in TAS
                
                # Minimum speed
                speed3=min_climb
                speed4=mpers2kts(vcas2tas(kts2mpers(speed3),alt)) # Speed in TAS
                
            elif j<(len(self.waypoints)):
                if self.phase[j-1]=='Climb':
                    # Nominal speed
                    speed=nom_climb
                    alt = 0.5*(float(self.FL[j-1])+float(self.FL[j]))*100.*ft
                    speed2=mpers2kts(vcas2tas(kts2mpers(speed),alt)) # Speed in TAS
                
                    # Minium speed
                    speed3=min_climb
                    speed4=mpers2kts(vcas2tas(kts2mpers(speed3),alt)) # Speed in TAS
                    
                elif self.phase[j-1]=='Cruise' or self.phase[j-1]=='Descent':
                    alt = 0.5*(float(self.FL[j-1])+float(self.FL[j]))*100.*ft
                    # Nominal speed
                    calculated_cruise_TAS_kts1,calculated_cruise_CAS_kts1=determine_cruise_TAS_CAS(nom_cruise_spd,nom_cruise_M,float(self.FL[j])*100) # h in feet, TAS in kts; Calculate which is the cruise CAS to be inserted, such that neither the CAS nor M is violated
                    calculated_cruise_TAS_kts2,calculated_cruise_CAS_kts2=determine_cruise_TAS_CAS(nom_cruise_spd,nom_cruise_M,float(self.FL[j-1])*100) # h in feet, TAS in kts; Calculate which is the cruise CAS to be inserted, such that neither the CAS nor M is violated
                    
                    if calculated_cruise_TAS_kts1<=calculated_cruise_TAS_kts2:
                        speed=calculated_cruise_CAS_kts1
                        speed2=calculated_cruise_TAS_kts1
                    elif calculated_cruise_TAS_kts2<calculated_cruise_TAS_kts1:
                        speed=calculated_cruise_CAS_kts2
                        speed2=calculated_cruise_TAS_kts2

                    # Minimum speed
                    calculated_cruise_TAS_kts1,calculated_cruise_CAS_kts1=determine_cruise_TAS_CAS(min_cruise_spd,min_cruise_M,float(self.FL[j])*100) # h in feet, TAS in kts; Calculate which is the cruise CAS to be inserted, such that neither the CAS nor M is violated
                    calculated_cruise_TAS_kts2,calculated_cruise_CAS_kts2=determine_cruise_TAS_CAS(min_cruise_spd,min_cruise_M,float(self.FL[j-1])*100) # h in feet, TAS in kts; Calculate which is the cruise CAS to be inserted, such that neither the CAS nor M is violated
                    
                    if calculated_cruise_TAS_kts1<=calculated_cruise_TAS_kts2:
                        speed3=calculated_cruise_CAS_kts1
                        speed4=calculated_cruise_TAS_kts1
                    elif calculated_cruise_TAS_kts2<calculated_cruise_TAS_kts1:
                        speed3=calculated_cruise_CAS_kts2
                        speed4=calculated_cruise_TAS_kts2                    
                    
                    if self.phase[j-1]=='Descent' or self.loc[j]=='AlmostIAF_IAF':
                        # Nominal speed                        
                        speed=min(speed,nom_CAS_TOD_almost_IAF)
                        speed2=mpers2kts(vcas2tas(kts2mpers(speed),alt)) # Speed in TAS 

                        # Minimum speed
                        speed3=min(speed3,min_CAS_TOD_almost_IAF)
                        speed4=mpers2kts(vcas2tas(kts2mpers(speed3),alt)) # Speed in TAS

            self.spd.append(speed)
            self.spd_TAS.append(speed2)
            self.minspd.append(speed3)
            self.minspd_TAS.append(speed4)
    
    def estimate_flyingtimes(self,TMArouteobject):
        # Nominal flying times
        counter=0.

        for k in range(len(self.waypoints)):
            estimate=0.
            extra=0.
            if k==len(self.waypoints)-1: # Last waypoint outside TMA
                
                extratemp=((TMArouteobject.spd_TAS[0]-self.spd_TAS[k])**2)/(TMArouteobject.spd_TAS[0]+self.spd_TAS[k])
                extra=(+1)*(TMArouteobject.spd_TAS[0]>self.spd_TAS[k])*extratemp + (-1)*(TMArouteobject.spd_TAS[0]<self.spd_TAS[k])*extratemp
                
                estimate=(self.dist[k]/TMArouteobject.spd_TAS[0])*3600.+extra
                del extratemp,extra
                
            else:
                extratemp=((self.spd_TAS[k+1]-self.spd_TAS[k])**2)/(self.spd_TAS[k+1]+self.spd_TAS[k])
                extra=(+1)*(self.spd_TAS[k+1]>self.spd_TAS[k])*extratemp + (-1)*(self.spd_TAS[k+1]<self.spd_TAS[k])*extratemp
                
                estimate=(self.dist[k]/self.spd_TAS[k+1])*3600.+extra
                del extratemp,extra
                
            self.estFT.append(estimate)
            self.estminFT.append(estimate)
            
            counter=counter+estimate
            del estimate
            
        self.totestFT=counter
        
        for k in range(len(self.waypoints)):
           self.estFT_to_IAF.append(np.sum(self.estFT[k:]))
           self.estFT_to_RWY.append(self.estFT_to_IAF[-1]+TMArouteobject.totestFT)
        
        # Maximum flying times (flying at minimum speed)
        counter=0.
        
        for k in range(len(self.waypoints)):
            estimate=0.
            extra=0.
            if k==len(self.waypoints)-1: # Last waypoint outside TMA
                extratemp=((TMArouteobject.minspd_TAS[0]-self.minspd_TAS[k])**2)/(TMArouteobject.minspd_TAS[0]+self.minspd_TAS[k])
                extra=(+1)*(TMArouteobject.minspd_TAS[0]>self.minspd_TAS[k])*extratemp + (-1)*(TMArouteobject.minspd_TAS[0]<self.minspd_TAS[k])*extratemp
            
                estimate=self.dist[k]/TMArouteobject.minspd_TAS[0]*3600.+extra
                del extratemp,extra
                
            else:
                extratemp=((self.minspd_TAS[k+1]-self.minspd_TAS[k])**2)/(self.minspd_TAS[k+1]+self.minspd_TAS[k])
                extra=(+1)*(self.minspd_TAS[k+1]>self.minspd_TAS[k])*extratemp + (-1)*(self.minspd_TAS[k+1]<self.minspd_TAS[k])*extratemp
                
                estimate=self.dist[k]/self.minspd_TAS[k+1]*3600.+extra
                del extratemp,extra
                
            self.estmaxFT.append(estimate)
            counter=counter+estimate
            del estimate
        self.totestmaxFT=counter
        
        for k in range(len(self.waypoints)):
           self.estmaxFT_to_IAF.append(np.sum(self.estmaxFT[k:]))
           self.estmaxFT_to_RWY.append(self.estmaxFT_to_IAF[-1]+TMArouteobject.totestmaxFT)

                    
    def calc_directdist_wpt_RWY(self,TMArouteobject):
        for k in range(len(self.waypoints)):
            temp=qdrdistA(float(self.LAT[k]),float(self.LON[k]),float(TMArouteobject.LAT[-1]),float(TMArouteobject.LON[-1]))
            self.directdist_RWY.append(temp)
            del temp                    

    def calculate_maxpossible_spddelabs(self,TMArouteobject):
        for k in range(len(self.waypoints)):
            nomft=self.estFT[k] # Nominal FT for segment
            maxft=self.estmaxFT[k] # Maximum FT for segment
            delayabs=maxft-nomft # [s]; delay that can be absorbed by speed reduction in this segment
            self.maxposs_spddelabs_segment.append(delayabs)
            
        self.maxposs_spddelabs_total=np.sum(self.maxposs_spddelabs_segment)
        
        for k in range(len(self.waypoints)):
            self.maxposs_spddelabs_to_IAF.append(np.sum(self.maxposs_spddelabs_segment[k:]))
            self.maxposs_spddelabs_to_RWY.append(self.maxposs_spddelabs_to_IAF[-1]+TMArouteobject.maxposs_spddelabs_total)
	
    def find_almostIAF_waypoint(self):
		almostIAF_distance = 0.
		i = 1.
		temp_heading,temp0 = qdrdist(float(self.IAF_LAT),float(self.IAF_LON),float(self.LAT[-2]),float(self.LON[-2]))
		while almostIAF_distance < 15.:
			temp_LAT,temp_LON = pos_and_dist_and_bearing_2_newpos(float(self.IAF_LAT),float(self.IAF_LON),i,temp_heading,Rearth)
			almostIAF_distance = qdrdistA(float(temp_LAT),float(temp_LON),float(self.IAF_LAT),float(self.IAF_LON))
			temp_distance = i
			i = i+1
		temp_ratio = (temp_distance/temp0)
		temp_FL = float(90.) + temp_ratio * (float(self.FL[-1])-float(90.))
		self.waypoints.insert(-1, 'WPT_almost_IAF')
		self.LAT.insert(-1, temp_LAT)
		self.LON.insert(-1, temp_LON)
		self.FL.insert(-1, temp_FL)
	
    def find_CBAS_waypoint(self):
		for k in range(len(self.waypoints)):
			dist_to_RWY = qdrdistA(float(self.LAT[k]),float(self.LON[k]),float(52.309),float(4.764))
			CBAS_distance = 0.
			i = 1.
			temp_heading,temp0 = qdrdist(float(self.LAT[k]),float(self.LON[k]),float(self.LAT[k-1]),float(self.LON[k-1]))
			first_wpt = False
			if k==0 and ((self.whichIAF == 'ARTIP' and dist_to_RWY < 105.) or (self.whichIAF == 'RIVER' and dist_to_RWY < 85.) or (self.whichIAF == 'SUGOL' and dist_to_RWY < 93.)):
				first_wpt = True
				temp_heading,temp0 = qdrdist(float(self.LAT[k+1]),float(self.LON[k+1]),float(self.LAT[k]),float(self.LON[k]))
			if self.whichIAF == 'ARTIP' and dist_to_RWY < 105.:
				while CBAS_distance < 105.:
					temp_LAT, temp_LON = pos_and_dist_and_bearing_2_newpos(float(self.LAT[k]),float(self.LON[k]),i,temp_heading,Rearth)
					CBAS_distance = qdrdistA(float(temp_LAT),float(temp_LON),float(52.309),float(4.764))
					temp_distance = i
					i = i+1
				temp_ratio = (temp_distance/temp0)
				if first_wpt == True:
					temp_FL = float(self.FL[k]) + temp_ratio * (float(self.FL[k+1])-float(self.FL[k]))
					self.waypoints[k+1] = 'WPT_CBAS'
					self.LAT[k+1] = temp_LAT
					self.LON[k+1] = temp_LON
					self.FL[k+1] = temp_FL
				else:
					temp_FL = float(self.FL[k-1]) + temp_ratio * (float(self.FL[k])-float(self.FL[k-1]))
					self.waypoints[k] = 'WPT_CBAS'
					self.LAT[k] = temp_LAT
					self.LON[k] = temp_LON
					self.FL[k] = temp_FL
				del temp_LAT,temp_LON,temp_FL,temp_ratio
				break
			elif self.whichIAF == 'RIVER' and dist_to_RWY < 85.:
				while CBAS_distance < 85.:
					temp_LAT, temp_LON = pos_and_dist_and_bearing_2_newpos(float(self.LAT[k]),float(self.LON[k]),i,temp_heading,Rearth)
					CBAS_distance = qdrdistA(float(temp_LAT),float(temp_LON),float(52.309),float(4.764))
					temp_distance = i
					i = i+1
				temp_ratio = (temp_distance/temp0)
				if first_wpt == True:
					temp_FL = float(self.FL[k]) + temp_ratio * (float(self.FL[k+1])-float(self.FL[k]))
					self.waypoints[k+1] = 'WPT_CBAS'
					self.LAT[k+1] = temp_LAT
					self.LON[k+1] = temp_LON
					self.FL[k+1] = temp_FL
				else:
					temp_FL = float(self.FL[k-1]) + temp_ratio * (float(self.FL[k])-float(self.FL[k-1]))
					self.waypoints[k] = 'WPT_CBAS'
					self.LAT[k] = temp_LAT
					self.LON[k] = temp_LON
					self.FL[k] = temp_FL
				del temp_LAT,temp_LON,temp_FL,temp_ratio
				break
			elif self.whichIAF == 'SUGOL' and dist_to_RWY < 93.:
				while CBAS_distance < 93.:
					temp_LAT, temp_LON = pos_and_dist_and_bearing_2_newpos(float(self.LAT[k]),float(self.LON[k]),i,temp_heading,Rearth)
					CBAS_distance = qdrdistA(float(temp_LAT),float(temp_LON),float(52.309),float(4.764))
					temp_distance = i
					i = i+1
				temp_ratio = (temp_distance/temp0)
				if first_wpt == True:
					temp_FL = float(self.FL[k]) + temp_ratio * (float(self.FL[k+1])-float(self.FL[k]))
					self.waypoints[k+1] = 'WPT_CBAS'
					self.LAT[k+1] = temp_LAT
					self.LON[k+1] = temp_LON
					self.FL[k+1] = temp_FL
				else:
					temp_FL = float(self.FL[k-1]) + temp_ratio * (float(self.FL[k])-float(self.FL[k-1]))
					self.waypoints[k] = 'WPT_CBAS'
					self.LAT[k] = temp_LAT
					self.LON[k] = temp_LON
					self.FL[k] = temp_FL
				del temp_LAT,temp_LON,temp_FL,temp_ratio
				break
			del dist_to_RWY,temp_heading,temp0,CBAS_distance,i
	
    def remove_intermediate_waypoints(self):
        i = 0
        while i < len(self.waypoints):
            if (self.waypoints[i].find('!')  == 0) or (self.waypoints[i].find('$')  == 0):
				del self.waypoints[i]
				del self.LAT[i]
				del self.LON[i]
				del self.FL[i]
				i = 0
            else:
				i = i+1
				
    def estimate_flyingtime_CBAS(self):
		tempindex = self.waypoints.index('WPT_CBAS')
		for k in range(len(self.waypoints)):
			self.estFT_to_CBAS.append(np.sum(self.estFT[k:tempindex]))
                  
class Route_TMA:
    def __init__(self):
        self.waypoints=[] # List of all waypoints
        self.LAT=[] # Latitude of each waypoint
        self.LON=[] # Longitude of each waypoint
        self.FL=[] # Altitude at each waypoint
        self.spd=[] # CAS
        self.spd_TAS=[] # TAS
        self.dist=[] # Distance in between waypoints
        self.heading=[] # Heading between waypoints
        self.totdist=[] # Total distance to RWY
        self.dist_to_RWY=[] # Total distance to RWY
        self.whichFAF=[] # Final Approach Fix
        self.phase=[] # Phase of flight (climb, cruise, descent)
        self.loc=[] # Location of aircraft (before or after TOD)
        self.extrawpts=[] # Extra waypoints (add two waypoints of opposite TMA route, such that aircraft flies correctly over full normal trajectory). Aircraft never flies over these waypoints, but necessary to include them.
        self.extrawpts_LAT=[] # Extra waypoints latitude
        self.extrawpts_LON=[] # Extra waypoints longitude
        self.estFT=[] # Estimated nominal flying time (per segment)
        self.totestFT=[] # Total estimated nominal flying time
        self.estFT_to_RWY=[] # Estimated flying time to runway (per segment)
        self.minspd=[] # Minimum CAS speed
        self.minspd_TAS=[] # Minimum TAS speed        
        self.estmaxFT=[] # Maximum flying time (per segment), minimum speed
        self.totestmaxFT=[] # Total maximum estimated flying time (minimum speed)
        self.estmaxFT_to_RWY=[] # Maximum flying time to runway (minimum speed)        
        self.maxposs_spddelabs_segment=[] # Maximum delay that can be absorbed by speed reduction (flying at minimum speed) w.r.t. nominal speed, per segment
        self.maxposs_spddelabs_to_RWY=[] # Maximum delay until RWY that can be absorbed by speed reduction (flying at minimum speed) w.r.t. nominal speed, per segment
        self.maxposs_spddelabs_total=[] # Total maximum delay that can be absorbed by speed reduction (flying at minimum speed) w.r.t. nominal speed
        self.RWY_LAT=[] # Runway threshold latitude
        self.RWY_LON=[] # Runway threshold longitude
        self.IAF_LAT=[] # IAF latitude
        self.IAF_LON=[] # IAF longitude
        
    def addTMAwpt(self,wptname,wptLAT,wptLON):
        self.waypoints.append(wptname)
        self.LAT.append(wptLAT)
        self.LON.append(wptLON)
        
    def calc_dist_and_heading(self):
        for k in range(len(self.waypoints)):
           if k<(len(self.waypoints)-1):
                self.dist.append(qdrdistA(float(self.LAT[k]),float(self.LON[k]),float(self.LAT[k+1]),float(self.LON[k+1])))
                
                temp1,temp2=qdrdist(float(self.LAT[k]),float(self.LON[k]),float(self.LAT[k+1]),float(self.LON[k+1]))
                if temp1<0:
                    temp1=temp1+360.
                self.heading.append(temp1)
                del temp1,temp2
                
           elif k==(len(self.waypoints)-1):
                self.dist.append(0.0)
                self.heading.append(-1.0)
        self.totdist=np.sum(self.dist) 

        for k in range(len(self.waypoints)):
           if k==0:
               self.dist_to_RWY.append(self.totdist)
           elif k>0 and k<(len(self.waypoints)-1):
               self.dist_to_RWY.append(self.dist_to_RWY[-1]-self.dist[k-1])
           elif k==(len(self.waypoints)-1):
               self.dist_to_RWY.append(0.)
         
        self.IAF_LAT=self.LAT[0]
        self.IAF_LON=self.LON[0]   
        
        self.RWY_LAT=self.LAT[-1]
        self.RWY_LON=self.LON[-1]
         
    def findFAF(self):
        self.whichFAF=self.waypoints[-2]
    
    def findLocation(self):
        default='IAF_FAF'
    
        for j in range(len(self.waypoints)):
            self.phase.append('Descent') # Phase is always 'descent' in TMA 
            
            if default=='IAF_FAF' and self.waypoints[j]==self.whichFAF:
                default='FAF_runway'
                   
            self.loc.append(default)
            
    def calculate_altitudes(self):
        counter=0.
        for j in range(len(self.waypoints)):
            if j==0: #at IAF
                self.FL.append(90) # FL90/9000 ft at IAF
            else:
                temp=self.FL[0]-(counter/self.totdist)*self.FL[0]
                self.FL.append(temp)
                del temp
                
            counter=counter+self.dist[j]
            
    def calculate_Speeds(self,RouteOutsideTMA,speed_almostIAF_IAF,speed_IAF_FAF,speed_FAF_RWY,minspeed_almostIAF_IAF,minspeed_IAF_FAF,minspeed_FAF_RWY): # RouteOutsideTMA is object
        for j in range(len(self.waypoints)):
            if self.waypoints[j]==RouteOutsideTMA.whichIAF:
                self.spd.append(speed_almostIAF_IAF)
                self.minspd.append(minspeed_almostIAF_IAF)
            else:
                if self.loc[j-1]=='IAF_FAF':
                    self.spd.append(speed_IAF_FAF)
                    self.minspd.append(minspeed_IAF_FAF)
                elif self.loc[j-1]=='FAF_runway':
                    self.spd.append(speed_FAF_RWY)
                    self.minspd.append(speed_FAF_RWY)
                    
            alt = (0.5*float(self.FL[j-1])+float(self.FL[j]))*100.*ft
            speed2=mpers2kts(vcas2tas(kts2mpers(self.spd[j]),alt))
            speed3=mpers2kts(vcas2tas(kts2mpers(self.minspd[j]),alt))
            
            self.spd_TAS.append(speed2)
            self.minspd_TAS.append(speed3)
    
    def determine_extrawpts(self,runway,allrunways,allrunwaysopposite,TMAroutesdata,wptdatabasecontent):
        idx=allrunways.index(runway)
        opposite=allrunwaysopposite[idx]
        
        
        temp=find_TMAroute(TMAroutesdata,'RIVER',opposite) # RIVER IS TEMP. DOESN'T MATTER.

        self.extrawpts.append(temp[-2])
        self.extrawpts.append(temp[-1])
        
        for item in self.extrawpts:
            LATtemp,LONtemp=obtain_TMAwpt_data(item,wptdatabasecontent)
            self.extrawpts_LAT.append(LATtemp)
            self.extrawpts_LON.append(LONtemp)  
            del LATtemp,LONtemp
        del temp

    def estimate_flyingtimes(self):
            # Nominal flying speeds            
            counter=0.
            
            for k in range(len(self.waypoints)):
                estimate=0.
                extra=0.
                
                if k==len(self.waypoints)-1: # Last waypoint in TMA (i.e. the runway)
                    estimate=0.
                else:
                    extratemp=((self.spd_TAS[k+1]-self.spd_TAS[k])**2)/(self.spd_TAS[k+1]+self.spd_TAS[k])               
                    extra=(+1)*(self.spd_TAS[k+1]>self.spd_TAS[k])*extratemp + (-1)*(self.spd_TAS[k+1]<self.spd_TAS[k])*extratemp                    
                    
                    estimate=(self.dist[k]/self.spd_TAS[k+1])*3600.+extra
                    del extratemp,extra
                    
                self.estFT.append(estimate)
                counter=counter+estimate
                del estimate
            self.totestFT=counter
            
            for k in range(len(self.waypoints)):
                self.estFT_to_RWY.append(np.sum(self.estFT[k:]))
            
            # Minimum flying speeds
            counter=0.
            estimate=0.
            for k in range(len(self.waypoints)):
                if k==len(self.waypoints)-1: # Last waypoint in TMA (i.e. the runway)
                    estimate=0.
                else:
                    extratemp=((self.minspd_TAS[k+1]-self.minspd_TAS[k])**2)/(self.minspd_TAS[k+1]+self.minspd_TAS[k])               
                    extra=(+1)*(self.minspd_TAS[k+1]>self.minspd_TAS[k])*extratemp + (-1)*(self.minspd_TAS[k+1]<self.minspd_TAS[k])*extratemp                    
                    
                    estimate=self.dist[k]/self.minspd_TAS[k+1]*3600.+extra
                    del extratemp,extra
                    
                self.estmaxFT.append(estimate)
                counter=counter+estimate
                del estimate
            self.totestmaxFT=counter
            
            for k in range(len(self.waypoints)):
                self.estmaxFT_to_RWY.append(np.sum(self.estmaxFT[k:]))    
                
    def calculate_maxpossible_spddelabs(self):
        for k in range(len(self.waypoints)):
            nomft=self.estFT[k] # Nominal FT for segment
            maxft=self.estmaxFT[k] # Maximum FT for segment
            delayabs=maxft-nomft # [s]; delay that can be absorbed by speed reduction in this segment
            self.maxposs_spddelabs_segment.append(delayabs)
            
        self.maxposs_spddelabs_total=np.sum(self.maxposs_spddelabs_segment)
        
        for k in range(len(self.waypoints)):
            self.maxposs_spddelabs_to_RWY.append(np.sum(self.maxposs_spddelabs_segment[k:]))
            
class Flights:
    def __init__(self):
        self.FlightIdentifier=[] # Flight identifier
        self.CallSign=[] # Callsign
        self.ACtype=[] # Aircraft type
        self.Origin=[] # Departure airport
        self.OriginTime=[] # Departure time
        self.OriginDate=[] # Departure date
        self.Destination=[] # Destination airport
        self.Origin_LAT=[] # Departure latitude
        self.Origin_LON=[] # Departure longitude
        self.Destination_LAT=[] # Destination latitude
        self.Destination_LON=[] # Destination longitude
        self.Route_outside_TMA=[] # Route outside TMA
        self.Route_TMA=[] # Route inside TMA
        self.Total_flightplan_dist=[] # Total flight plan distance
        self.Direct_inbetween_dist=[] # Direct distance between airports
        self.SimTime=[] # Simtime
        self.Total_estFT=[] # Total estimated flying time
        self.Total_estmaxFT=[] # Total estimated maximum flying time
        self.Maxposs_spddelabs_total=[] # Maximum possible delay absorption due to speed reduction
        self.PreDepEstTime_at_CBAS=[] # Pre-departure estimate CBAS
        self.PreDepEstTime_at_IAF=[] # Pre-departure estimate IAF
        self.PreDepEstTime_at_RWY=[] # Pre-departure estimate RWY    
        self.StartHeading=[] # Heading at which aircraft is created
        self.PopupLabel=[] # Aircraft pop-up or not?        
        
    def create_flight(self,flightid,callsign,actype,origin,origintime,origindate,destination):
        self.FlightIdentifier.append(flightid)
        self.CallSign.append(callsign)
        self.ACtype.append(actype)
        self.Origin.append(origin)
        self.OriginTime.append(origintime)
        self.OriginDate.append(origindate)
        self.Destination.append(destination)
        self.Route_outside_TMA.append(Route_outside_TMA())
        self.Route_TMA.append(Route_TMA())
        self.SimTime.append(mmddhhmmss2s(origindate,origintime)) 
       
    def calculate_distances(self,j,AMANhorizon,Popupexclusionlist):
        temp1=self.Route_outside_TMA[j].totdist+self.Route_TMA[j].totdist
        self.Total_flightplan_dist.append(temp1)
        
        temp2=qdrdistA(float(self.Origin_LAT[j]),float(self.Origin_LON[j]),float(self.Destination_LAT[j]),float(self.Destination_LON[j]))      
        self.Direct_inbetween_dist.append(temp2)
        del temp1,temp2
        
        if self.Direct_inbetween_dist[-1] <= AMANhorizon and self.Origin[j] not in Popupexclusionlist:
            self.PopupLabel.append('POPUP')
            
        else:
            self.PopupLabel.append('NORMAL')
    
    def calculate_total_estFT(self,j):
        self.Total_estFT.append(self.Route_outside_TMA[j].totestFT+self.Route_TMA[j].totestFT)
        self.Total_estmaxFT.append(self.Route_outside_TMA[j].totestmaxFT+self.Route_TMA[j].totestmaxFT)

    def calculate_maxpossible_spddelabs(self,j):
        self.Maxposs_spddelabs_total.append(self.Route_outside_TMA[j].maxposs_spddelabs_total+self.Route_TMA[j].maxposs_spddelabs_total)
 
    def estimate_CBAS_IAF_runway_arrtimes(self,j):
        self.PreDepEstTime_at_CBAS.append(self.SimTime[j]+self.Route_outside_TMA[j].estFT_to_CBAS[0])
        self.PreDepEstTime_at_IAF.append(self.SimTime[j]+self.Route_outside_TMA[j].estFT_to_IAF[0])
        self.PreDepEstTime_at_RWY.append(self.SimTime[j]+self.Route_outside_TMA[j].estFT_to_RWY[0])

    def determine_start_heading(self,j):
        if len(self.Route_outside_TMA[j].waypoints)>=2:
            temp1,temp2=qdrdist(self.Route_outside_TMA[j].LAT[0],self.Route_outside_TMA[j].LON[0],self.Route_outside_TMA[j].LAT[1],self.Route_outside_TMA[j].LON[1])
            self.StartHeading.append(temp1)
            del temp1,temp2
        else:
            self.StartHeading.append(0.)
    
    def replace_flight(self,x,y,newCallSign): # Replace flight with index x by flight with index y.
        self.SimTime[x]=int(self.SimTime[x]+self.Total_estFT[x]-self.Total_estFT[y]) # Aircraft has to arrive at the same time (at the runway) as the original flight. Therefore the replacement flight needs to have a delayed SimTime

        self.CallSign[x]=newCallSign
        
        self.FlightIdentifier[x]=self.CallSign[x]+str(int(self.SimTime[x])) # Generate a unique flight identifier
        
        self.ACtype[x]=self.ACtype[y]
        self.Origin[x]=self.Origin[y]
        self.OriginTime[x]=self.OriginTime[y]
        self.OriginDate[x]=self.OriginDate[y]
        self.Destination[x]=self.Destination[y]
        self.Origin_LAT[x]=self.Origin_LAT[y]
        self.Origin_LON[x]=self.Origin_LON[y]
        self.Destination_LAT[x]=self.Destination_LAT[y]
        self.Destination_LON[x]=self.Destination_LON[y]
        self.Route_outside_TMA[x]=self.Route_outside_TMA[y]
        self.Route_TMA[x]=self.Route_TMA[y]
        self.Total_flightplan_dist[x]=self.Total_flightplan_dist[y]
        self.Direct_inbetween_dist[x]=self.Direct_inbetween_dist[y]
        self.Total_estFT[x]=self.Total_estFT[y]
        self.Total_estmaxFT[x]=self.Total_estmaxFT[y]
        self.Maxposs_spddelabs_total[x]=self.Maxposs_spddelabs_total[y]    
        self.StartHeading[x]=self.StartHeading[y] # Heading at which aircraft is created
        self.PopupLabel[x]=self.PopupLabel[y] # Aircraft pop-up or not?        
        
        self.PreDepEstTime_at_CBAS[x]=self.SimTime[x]+self.Route_outside_TMA[x].estFT_to_CBAS[0] # Update Pre-Departure Estimate Times (at CBAS)
        self.PreDepEstTime_at_IAF[x]=self.SimTime[x]+self.Route_outside_TMA[x].estFT_to_IAF[0] # Update Pre-Departure Estimate Times (at IAF)
        self.PreDepEstTime_at_RWY[x]=self.SimTime[x]+self.Route_outside_TMA[x].estFT_to_RWY[0] # Update Pre-Departure Estimate Times (at RWY)
        
def minutedecimale2degree(x):
    y=float(x)/60
    return y        

def mmddhhmmss2s(date,time): # Day in format yymmdd, time in format hhmmss
    secondsinday=24.0*3600.
    y=((float(date[2:4])-1.)*31.*secondsinday)+((float(date[4:])-1.)*secondsinday)+(float(time[0:2])*3600.+float(time[2:4])*60.+float(time[4:])) # Assumes a month has 31 days. 
    return y
    
def qdrdistA(latadeg,lonadeg,latbdeg,lonbdeg):
    """Lat/lon calculations using WGS84, calculate direction from A to B [deg] and the distance in meters"""

    # Conversion
    lata = radians(latadeg)
    lona = radians(lonadeg)
    latb = radians(latbdeg)
    lonb = radians(lonbdeg)

    # Constants
    reqtor = 3443.92  # Radius at equator in nm
    ellips = 4.4814724e-5   # Ellipsoid shape of earth WGS'84

    # Calculation of unit vectors
    londif = lonb-lona
    xa=cos(lata)
    # ya=cos(dlata)*0.0)
    za = sin(lata)
    xb = cos(latb)*cos(londif)
    yb = cos(latb)*sin(londif)
    zb = sin(latb)

    zave = (za+zb)/2.

    rprime = reqtor/sqrt(1. - ellips*zave*zave)

    # Distance over earth
    # Prevent domain errors due to rounding errors
    sangl2 = sqrt((xb-xa)*(xb-xa)+yb*yb+(zb-za)*(zb-za))*0.5
    angle = 2.*asin(min(1.,max(-1.,sangl2)))
    dist  = angle*rprime

    # True bearing from a to b
    cosqdr=(xa*zb - xb*za)
    sinqdr=yb

    if sinqdr*sinqdr+cosqdr*cosqdr > 0. :
        qdr=atan2(sinqdr,cosqdr)
    else:
        qdr=0.0

    if qdr <0:
        qdr=qdr+2.*pi

    # Unit conversion to degrees and meters
    distnm = dist
    return distnm

def pos_and_dist_and_bearing_2_newpos(LAT1,LON1,dist,bearing,R_Earth): # Degrees, distance in nm,R_Earth in m
    LAT1=np.deg2rad(LAT1) # Radians
    LON1=np.deg2rad(LON1) # Radians
    bearing=np.deg2rad(bearing) # Radians
    dist=dist*nm # m
    
    LAT2=np.arcsin(sin(LAT1)*np.cos(dist/R_Earth)+np.cos(LAT1)*sin(dist/R_Earth)*np.cos(bearing))
    LON2=LON1+np.arctan2(np.sin(bearing)*np.sin(dist/R_Earth)*np.cos(LAT1),np.cos(dist/R_Earth)-np.sin(LAT1)*np.sin(LAT2))

    LAT2=np.rad2deg(LAT2)
    LON2=np.rad2deg(LON2)   
    
    return LAT2,LON2

def find_holdingstack_center(R_stack,LAT_IAF,LON_IAF,heading_TMA): # R_stack in nm, degrees
    R_Earth=rwgs84(LAT_IAF) # m
    
    heading_perp=heading_TMA+90.
    if heading_perp>=360:
        heading_perp=heading_perp-360.
    
    CenterLAT,CenterLON=pos_and_dist_and_bearing_2_newpos(LAT_IAF,LON_IAF,R_stack,heading_perp,R_Earth)

    return CenterLAT,CenterLON,R_Earth,heading_TMA,heading_perp # Degree
    
def find_holdingstack_waypoints(R_stack,CenterLAT,CenterLON,TMAheading,headingperp,R_Earth): # nm and degree
    # Waypoint A (Center+R in heading of TMA)    
    A_LAT,A_LON=pos_and_dist_and_bearing_2_newpos(CenterLAT,CenterLON,R_stack,TMAheading,R_Earth)
    
    # Waypoint B (Center+R in heading perpendicular to TMA heading)
    B_LAT,B_LON=pos_and_dist_and_bearing_2_newpos(CenterLAT,CenterLON,R_stack,headingperp,R_Earth)
    
    # Waypoint C (Center+R in opposite heading of TMA heading)
    C_LAT,C_LON=pos_and_dist_and_bearing_2_newpos(CenterLAT,CenterLON,R_stack,TMAheading+180.,R_Earth)
    
    # Waypoint D (Center+R in opposite heading of perpendicular)
    D_LAT,D_LON=pos_and_dist_and_bearing_2_newpos(CenterLAT,CenterLON,R_stack,headingperp+180.,R_Earth)
    
    return A_LAT,A_LON,B_LAT,B_LON,C_LAT,C_LON,D_LAT,D_LON

def find_extraflying_waypoints_semicircles(almostIAF_LAT,almostIAF_LON,IAF_LAT,IAF_LON,extra_distance,TMAheading): # nm, degrees
    R_Earth=rwgs84(almostIAF_LAT) # m
    
    nominal_dist=qdrdistA(almostIAF_LAT,almostIAF_LON,IAF_LAT,IAF_LON) # nm
    
    nominal_heading,temp=qdrdist(almostIAF_LAT,almostIAF_LON,IAF_LAT,IAF_LON) # Degree
    del temp
    
    # Find center of 2 circles
    LAT_center1,LON_center1=pos_and_dist_and_bearing_2_newpos(almostIAF_LAT,almostIAF_LON,nominal_dist/4.,nominal_heading,R_Earth)
    LAT_center2,LON_center2=pos_and_dist_and_bearing_2_newpos(almostIAF_LAT,almostIAF_LON,3.*nominal_dist/4.,nominal_heading,R_Earth)
    
    # Find radius of semicircles
    R_circle=(nominal_dist+extra_distance)/(2*np.pi)    
    
    if TMAheading<=nominal_heading:
		# Waypoint A    
        A2_LAT,A2_LON=pos_and_dist_and_bearing_2_newpos(LAT_center1,LON_center1,R_circle,nominal_heading-90.,R_Earth)
        A3_LAT,A3_LON=pos_and_dist_and_bearing_2_newpos(LAT_center1,LON_center1,R_circle,nominal_heading-45.,R_Earth)
        
        # Waypoint B
        B_LAT,B_LON=pos_and_dist_and_bearing_2_newpos(almostIAF_LAT,almostIAF_LON,nominal_dist/2.,nominal_heading,R_Earth)    
    
        # Waypoint C
        C1_LAT,C1_LON=pos_and_dist_and_bearing_2_newpos(LAT_center2,LON_center2,R_circle,nominal_heading+135.,R_Earth)     
        C2_LAT,C2_LON=pos_and_dist_and_bearing_2_newpos(LAT_center2,LON_center2,R_circle,nominal_heading+90.,R_Earth)     
        
    elif TMAheading>nominal_heading:
        # Waypoint A
        A2_LAT,A2_LON=pos_and_dist_and_bearing_2_newpos(LAT_center1,LON_center1,R_circle,nominal_heading+90.,R_Earth)
        A3_LAT,A3_LON=pos_and_dist_and_bearing_2_newpos(LAT_center1,LON_center1,R_circle,nominal_heading+45.,R_Earth)
        
        # Waypoint B
        B_LAT,B_LON=pos_and_dist_and_bearing_2_newpos(almostIAF_LAT,almostIAF_LON,nominal_dist/2.,nominal_heading,R_Earth)    
    
        # Waypoint C
        C1_LAT,C1_LON=pos_and_dist_and_bearing_2_newpos(LAT_center2,LON_center2,R_circle,nominal_heading-135.,R_Earth)     
        C2_LAT,C2_LON=pos_and_dist_and_bearing_2_newpos(LAT_center2,LON_center2,R_circle,nominal_heading-90.,R_Earth)     
         
    return A2_LAT,A2_LON,A3_LAT,A3_LON,B_LAT,B_LON,C1_LAT,C1_LON,C2_LAT,C2_LON,nominal_heading  
    
def find_extraflying_waypoints_dogleg(almostIAF_LAT,almostIAF_LON,IAF_LAT,IAF_LON,extra_distance,TMAheading): # nm, degrees
    R_Earth=rwgs84(almostIAF_LAT) # m
    
    nominal_dist=qdrdistA(almostIAF_LAT,almostIAF_LON,IAF_LAT,IAF_LON) # nm
    
    nominal_heading,temp=qdrdist(almostIAF_LAT,almostIAF_LON,IAF_LAT,IAF_LON) # Degree
    del temp
    
    alpha=np.rad2deg(np.arccos((nominal_dist)/(nominal_dist+extra_distance)))
   
    if TMAheading<=nominal_heading:
		# Waypoint A
        A_LAT,A_LON=pos_and_dist_and_bearing_2_newpos(almostIAF_LAT,almostIAF_LON,(nominal_dist+extra_distance)/2.,nominal_heading+alpha,R_Earth)
        
    elif TMAheading>nominal_heading:
        # Waypoint A
        A_LAT,A_LON=pos_and_dist_and_bearing_2_newpos(almostIAF_LAT,almostIAF_LON,(nominal_dist+extra_distance)/2.,nominal_heading-alpha,R_Earth)

    return A_LAT,A_LON,alpha 
    
def kts2mpers(a):
    b=0.51444*float(a)
    return b

def mpers2kts(a):
    b=float(a)*1.94384449
    return b

def determine_cruise_TAS_CAS(TAS_cruise,M_cruise,h_cruise): # h in feet, TAS in kts; Calculate which is the cruise CAS to be inserted, such that neither the CAS nor M is violated
    alt=h_cruise*ft # h in feet, alt in m
    TAS_mps=vmach2tas(M_cruise,alt)
    TAS_kts =mpers2kts(TAS_mps)
    
    calculated_cruise_TAS_kts=min(TAS_cruise,TAS_kts) 
    calculated_cruise_TAS_mps=kts2mpers(calculated_cruise_TAS_kts)
    
    calculated_cruise_CAS_kts=mpers2kts(vtas2cas(calculated_cruise_TAS_mps,alt))
    
    return calculated_cruise_TAS_kts,calculated_cruise_CAS_kts  