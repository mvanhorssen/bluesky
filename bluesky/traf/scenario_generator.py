# scenario_generator.py
from ..settings import data_path
from scenario_functions import *
from performanceA import *
import random
import sys

##################################################################################### 
# sys.argv[1] = name
# sys.argv[2] = DatasetN
# sys.argv[3] = popup_scaling (100 = normal)
# sys.argv[4] = AMAN/EAMAN/XMAN250/XMAN350/XMAN450
# sys.argv[5] = ASAPBASIC/DYNAMIC/ASAPUPGRADE
# sys.argv[6] = Pre-departure_delay
# sys.argv[7] = approach_margin
##################################################################################### 
       
def scenario_creator(FlightID): #AllFlights.SimTime[idx]-simulation_start
    idx=AllFlights.FlightIdentifier.index(FlightID)
    outputfile.write('\n \n \n \n')
    outputfile.write('00:00:'+str(AllFlights.SimTime[idx]-simulation_start)+'>CRE '+str(AllFlights.CallSign[idx])+ ', '+'B744'+','+str(AllFlights.Route_outside_TMA[idx].LAT[0])+','+str(AllFlights.Route_outside_TMA[idx].LON[0]) + ',' + str(AllFlights.StartHeading[idx]) + ',0,' + str(AllFlights.Route_outside_TMA[idx].spd[0]) + '\n \n')  # B744 should be replaced with real aircraft type 
    # Example: 00:00:00.00>CRE TN748,B747, 51.934621,5.599594,45,0,200
    outputfile.write('00:00:'+str(AllFlights.SimTime[idx]-simulation_start)+'>ORIG '+str(AllFlights.CallSign[idx])+ ', '+ str(AllFlights.Origin[idx]) + '\n \n')   
    # Example: 00:00:00.00>ORIG,TN748,LFRS
    outputfile.write('00:00:'+str(AllFlights.SimTime[idx]-simulation_start)+'>DEST '+str(AllFlights.CallSign[idx])+ ', '+ str(AllFlights.Destination[idx]) + '\n \n')   
    # Example: 00:00:00.00>DEST,TN748,EHAM
        
    for k in range(len(AllFlights.Route_outside_TMA[idx].waypoints)):
        outputfile.write('00:00:'+str(AllFlights.SimTime[idx]-simulation_start)+'>ADDWPT '+str(AllFlights.CallSign[idx])+ ', '+ str(AllFlights.Route_outside_TMA[idx].LAT[k])+','+ str(AllFlights.Route_outside_TMA[idx].LON[k]) +','+ str(float(AllFlights.Route_outside_TMA[idx].FL[k])*100.) + ',' + str(AllFlights.Route_outside_TMA[idx].spd[k]) + '\n \n')       
                
        if k==0:
            outputfile.write('00:00:'+str(AllFlights.SimTime[idx]-simulation_start)+'>DIRECT '+str(AllFlights.CallSign[idx])+ ', '+ str(AllFlights.CallSign[idx])+'000' '\n \n')   
            # Example: 01:00:00.00>DIRECT,TN748,TN748000,0,220
    
    for k in range(len(AllFlights.Route_TMA[idx].waypoints)):
        outputfile.write('00:00:'+str(AllFlights.SimTime[idx]-simulation_start)+'>ADDWPT '+str(AllFlights.CallSign[idx])+ ', '+ str(AllFlights.Route_TMA[idx].LAT[k])+','+ str(AllFlights.Route_TMA[idx].LON[k]) +','+ str(float(AllFlights.Route_TMA[idx].FL[k])*100.) + ',' + str(AllFlights.Route_TMA[idx].spd[k]) + '\n \n')       
        
    # Add extra waypoints
    outputfile.write('00:00:'+str(AllFlights.SimTime[idx]-simulation_start)+'>ADDWPT ' +str(AllFlights.CallSign[idx]) + ', ' + str(AllFlights.Route_TMA[idx].extrawpts_LAT[1]) + ', ' + str(AllFlights.Route_TMA[idx].extrawpts_LON[1]) + ',' +  str(0.) + ',' + str(AllFlights.Route_TMA[idx].spd[-1]) + '\n \n')
    #outputfile.write('00:00:'+str(AllFlights.SimTime[idx]-simulation_start)+'>ADDWPT ' +str(AllFlights.CallSign[idx]) + ', ' + str(AllFlights.Route_TMA[idx].extrawpts_LAT[0]) + ', ' + str(AllFlights.Route_TMA[idx].extrawpts_LON[0]) + ',' +  str(0.) + ',' + str(AllFlights.Route_TMA[idx].spd[-1]) + '\n \n')
    
    outputfile.write('00:00:'+str(AllFlights.SimTime[idx]-simulation_start)+'>LNAV '+str(AllFlights.CallSign[idx])+ ', ON' '\n \n')   
    # Example: 00:00:00.00>LNAV,TN748,ON
    outputfile.write('00:00:'+str(AllFlights.SimTime[idx]-simulation_start)+'>VNAV '+str(AllFlights.CallSign[idx])+ ', ON')   
    # Example: 00:00:00.00>VNAV,TN748,ON
    
#####################################################################################  

popup_window = False

if popup_window is True:
	from Tkinter import *
	
	def print_text():
		print('Name: %s' % E_Name.get())
		print('Dataset: %s' % E_Dataset.get())
		print('Approach margin: %s' % E_approach_margin.get())
		print('Popup Scaling: %s' % E_popup_scaling.get())
		print('Arrival Manager: %s' % select_AMAN())
		print('Trajectory Predictor: %s' % select_TP())
		print('Pre-departure Delay: %s' % E_predep_delay.get())
		filename = E_Dataset.get()
		approach_margin = float(E_approach_margin.get())
		popup_scaling = float(E_popup_scaling.get())
		var_AMAN = select_AMAN()
		var_TP = select_TP()
		pre_departure_delay = float(E_predep_delay.get())
		master_quit()

	def select_AMAN():
		var_AMAN = ''
		if AMAN_var.get() == 0:
			var_AMAN = 'AMAN'
		if AMAN_var.get() == 1:
			var_AMAN = 'EAMAN'
		if AMAN_var.get() == 2:
			var_AMAN = 'XMAN'
		return var_AMAN
	
	def select_TP():
		var_TP = ''
		if TP_var.get() == 0:
			var_TP = 'ASAPBASIC'
		if TP_var.get() == 1:
			var_TP = 'DYNAMIC'
		if TP_var.get() == 2:
			var_TP = 'ASAPUPGRADE'
		return var_TP

	def master_quit():
		master.destroy()
	
	master = Tk()
	master.wm_title('Initialize AMAN variables')
	# Name Entry
	Label(master, text="Name").grid(row=0)
	E_Name = Entry(master)
	E_Name.insert(10, 'Name')
	E_Name.grid(row=0,column=1)
	# Dataset Entry
	Label(master, text="Dataset").grid(row=1)
	E_Dataset = Entry(master)
	E_Dataset.insert(10, 'Dataset1')
	E_Dataset.grid(row=1,column=1)
	# Approach Margin Entry
	Label(master, text="Approach Margin [sec]").grid(row=2)
	E_approach_margin = Entry(master)
	E_approach_margin.insert(10, '30')
	E_approach_margin.grid(row=2,column=1)
	# Popup Scaling Entry
	Label(master, text="Popup Scaling [%]").grid(row=3)
	E_popup_scaling = Entry(master)
	E_popup_scaling.insert(10, '100')
	E_popup_scaling.grid(row=3,column=1)
	# Arrival Manager Entry
	Label(master, text="Arrival Manager").grid(row=4)
	AMAN_var = IntVar()
	E_AMAN = Radiobutton(master, text='AMAN', variable = AMAN_var, value=0, command=select_AMAN)
	E_AMAN.grid(row=4,column=1)
	E_EAMAN = Radiobutton(master, text='E-AMAN', variable = AMAN_var, value=1, command=select_AMAN)
	E_EAMAN.grid(row=4,column=2)
	E_XMAN = Radiobutton(master, text='XMAN', variable = AMAN_var, value=2, command=select_AMAN)
	E_XMAN.grid(row=4,column=3)
	# Trajectory Predictor Entry
	Label(master, text="Trajectory Predictor").grid(row=5)
	TP_var = IntVar()
	E_TP_ASAPBASIC = Radiobutton(master, text='ASAP BASIC', variable = TP_var, value=0)
	E_TP_ASAPBASIC.grid(row=5,column=1)
	E_TP_DYNAMIC = Radiobutton(master, text='DYNAMIC', variable = TP_var, value=1)
	E_TP_DYNAMIC.grid(row=5,column=2)
	E_TP_ASAPUPGRADE = Radiobutton(master, text='ASAP UPGRADE', variable = TP_var, value=2)
	E_TP_ASAPUPGRADE.grid(row=5,column=3)
	# Pre-departure Delay Entry
	Label(master, text="Pre-departure Delay [sec]").grid(row=6)
	E_predep_delay = Entry(master)
	E_predep_delay.insert(10, '0')
	E_predep_delay.grid(row=6,column=1)

	Button(master, text='Quit', command=master_quit).grid(row=8,column=0)
	Button(master, text='Run', command=print_text).grid(row=8,column=1)

	master.mainloop()
	
print
print('*********************************************************************************************')
print('*********************************************************************************************')
print('********************************** AMAN Research Simulator **********************************')
print('*********************************************************************************************')
print('*********************************************************************************************')
print

if len(sys.argv)>2:
	var_name = ''
	var_txt = open('variables.txt','w')
	var_txt.write(sys.argv[1]+'\n') # Name
	var_txt.write(sys.argv[2]+'\n') # Dataset
	var_txt.write(sys.argv[3]+'\n') # popup_scaling
	var_txt.write(sys.argv[4]+'\n') # AMAN
	var_txt.write(sys.argv[5]+'\n') # Trajectory Predictor
	var_txt.write(sys.argv[6]+'\n') # Pre-departure delay
	var_txt.write(sys.argv[7]+'\n') # Approach margin
	var_txt.close()
	var_predeparture_delay = float(sys.argv[6])

if '--node' in sys.argv:
	var_txt = open('variables.txt','r')
	var_name = str(var_txt.readline()).rstrip()
	var_dataset = str(var_txt.readline()).rstrip()
	var_popup_scaling = float(var_txt.readline())
	var_AMAN = str(var_txt.readline()).rstrip()
	var_TP = str(var_txt.readline()).rstrip()
	var_predeparture_delay = float(var_txt.readline())
	var_approach_margin = float(var_txt.readline())
	var_txt.close()
	
if '--node' in sys.argv:
    if var_dataset==str('Dataset1'):
        filename='20150707_0400_0700UTC.so6'
        
    elif var_dataset==str('Dataset2'):
        filename='20150707Regulated1619UTC.so6'

    elif var_dataset==str('Dataset3'):
        filename='20150716Regulated58UTC.so6'

    elif var_dataset==str('Dataset4'):
        filename='20150716Regulated1619UTC.so6'
                
    elif var_dataset==str('Dataset5'):
        filename='20150807Regulated58UTC.so6'
                
    elif var_dataset==str('Dataset6'):
        filename='20150807Regulated1619UTC.so6'
                
    elif var_dataset==str('Dataset7'):
        filename='20150812Regulated58UTC.so6'
                
    elif var_dataset==str('Dataset8'):
        filename='20150812Regulated1619UTC.so6'
            
    elif var_dataset==str('Dataset9'):
        filename='20150901Regulated58UTC.so6'
        
    elif var_dataset==str('Dataset10'):
        filename='20150901Regulated1619UTC.so6'        
        
    elif var_dataset==str('Dataset11'):
        filename='20150914Regulated58UTC.so6'
        
    elif var_dataset==str('Dataset12'):
        filename='20150914Regulated1619UTC.so6'        
        
    elif var_dataset==str('Dataset21'):
        filename='20150707Regulated1013UTC.so6'       

    elif var_dataset==str('Dataset22'):
        filename='20150707Regulated1316UTC.so6'

    elif var_dataset==str('Dataset23'):
        filename='20150716Regulated1013UTC.so6'        

    elif var_dataset==str('Dataset24'):
        filename='20150716Regulated1316UTC.so6'    

    elif var_dataset==str('Dataset25'):
        filename='20150807Regulated1013UTC.so6'

    elif var_dataset==str('Dataset26'):
        filename='20150807Regulated1316UTC.so6'        

    elif var_dataset==str('Dataset27'):
        filename='20150812Regulated1013UTC.so6'

    elif var_dataset==str('Dataset28'):
        filename='20150812Regulated1316UTC.so6'

    elif var_dataset==str('Dataset29'):
        filename='20150901Regulated1013UTC.so6'

    elif var_dataset==str('Dataset30'):
        filename='20150901Regulated1316UTC.so6'

    elif var_dataset==str('Dataset31'):
        filename='20150914Regulated1013UTC.so6'

    elif var_dataset==str('Dataset32'):
        filename='20150914Regulated1316UTC.so6'
           
else:
    filename='20150707_0400_0700UTC.so6' # Traffic .so6 file to be simulated

intarrtime_AMAN_runway=100. # Specifies the inter-arrival time for each runway

if '--node' in sys.argv:
    approach_margin = float(var_approach_margin)
else:
    approach_margin = 30. # Approach margin [seconds]

if '--node' in sys.argv:
    if str(var_AMAN)=='AMAN':
        print
        print 'AMAN'
        print
        AMAN_horizon=120. # [nm]; Planning Horizon
        SARA_horizon=100. # [nm]; Active Advisory Horizon
        Take_into_account_schedule_horizon=250. # [nm]; From this horizon, aircraft are used for scheduling
        Freeze_horizon=120. # [nm]; Should be same as AMAN_horizon. Freeze Horizon (STA is semi-fixed now). Sufficient time necessary to process flights just outside Freeze_horizon: set (at least) 20 nm smaller than AMAN_horizon       
    elif var_AMAN=='EAMAN':   
        print
        print 'E-AMAN'
        print
        AMAN_horizon=200. # [nm]; Planning Horizon
        SARA_horizon=180. # [nm]; Active Advisory Horizon
        Take_into_account_schedule_horizon=300. # [nm]; From this horizon, aircraft are used for scheduling
        Freeze_horizon=200. # [nm]; Should be same as AMAN_horizon. Freeze Horizon (STA is semi-fixed now). Sufficient time necessary to process flights just outside Freeze_horizon: set (at least) 20 nm smaller than AMAN_horizon
    elif str(var_AMAN)=='XMAN250':   
        print
        print 'XMAN 250'
        print
        AMAN_horizon=250. # [nm]; Planning Horizon
        SARA_horizon=230. # [nm]; Active Advisory Horizon
        Take_into_account_schedule_horizon=300. # [nm]; From this horizon, aircraft are used for scheduling
        Freeze_horizon=250. # [nm]; Should be same as AMAN_horizon. Freeze Horizon (STA is semi-fixed now). Sufficient time necessary to process flights just outside Freeze_horizon: set (at least) 20 nm smaller than AMAN_horizon
    elif str(var_AMAN)=='XMAN350':   
        print
        print 'XMAN 350'
        print
        AMAN_horizon=350. # [nm]; Planning Horizon
        SARA_horizon=330. # [nm]; Active Advisory Horizon
        Take_into_account_schedule_horizon=400. # [nm]; From this horizon, aircraft are used for scheduling
        Freeze_horizon=350. # [nm]; Should be same as AMAN_horizon. Freeze Horizon (STA is semi-fixed now). Sufficient time necessary to process flights just outside Freeze_horizon: set (at least) 20 nm smaller than AMAN_horizon
    elif str(var_AMAN)=='XMAN450':   
        print
        print 'XMAN 450'
        print
        AMAN_horizon=450. # [nm]; Planning Horizon
        SARA_horizon=430. # [nm]; Active Advisory Horizon
        Take_into_account_schedule_horizon=500. # [nm]; From this horizon, aircraft are used for scheduling
        Freeze_horizon=450. # [nm]; Should be same as AMAN_horizon. Freeze Horizon (STA is semi-fixed now). Sufficient time necessary to process flights just outside Freeze_horizon: set (at least) 20 nm smaller than AMAN_horizon
else:    
    AMAN_horizon=200. # [nm]; Planning Horizon
    SARA_horizon=190. # [nm]; Active Advisory Horizon
    Take_into_account_schedule_horizon=250. # [nm]; From this horizon, aircraft are used for scheduling
    Freeze_horizon=200. # [nm]; Should be same as AMAN_horizon. Freeze Horizon (STA is semi-fixed now). Sufficient time necessary to process flights just outside Freeze_horizon: set (at least) 20 nm smaller than AMAN_horizon

#####
# Scenario editing
max_flpl_dist=700. # [nm]; flights with a flight plan distance larger than this value are replaced with a NORMAL flight (i.e. not a pop-up flight)

if '--node' in sys.argv:
    popup_scaling=float(var_popup_scaling)
else:
    popup_scaling=100. # [%]; increase/decrease number of pop-up flights

#####
# DO NOT EDIT
popup_scaling=popup_scaling/100. # Scaling [percentage] is transformed into factor
# DO NOT EDIT
#####

possible_IAFs=['RIVER','SUGOL','ARTIP']
runways_use_land=['18C-27','18C','27'] # Specifies, for each IAF in possible_IAFs, the active landing runway
unique_runways=['18C','27'] 

Popup_exclusion_list=['DUMMY'] # For a horizon of 200 nm or smaller (E-AMAN), these airports are not considered as pop-up airports
wpt_exclusionlist=['ROBVI'] # Sometimes necessary to remove certain waypoint for the sake of convenience (e.g. ROBVI). If this waypoint is not deleted, last wpt before SUGOL is SOBVI, which is located too close to SUGOL to sufficiently decelerate. For convenience, SOBVI is removed. Only has limited impact, as wpt is only used after MONIL and LUTEX

# For the sake of how BlueSky works, it is necessary to also include the last waypoint of the TMA route of the opposite runway
allrunways=['18L','18C','18R','36L','36C','36R','09','27','06','24','04','22']
allrunways_opposite=['36R','36C','36L','18R','18C','18L','27','09','24','06','22','04']

######################################################################################## 

print('************************************ Generating Scenario ************************************')
print('Planning Horizon [NM]: '+str(AMAN_horizon))
print('Active Advisory Horizon [NM]: '+str(SARA_horizon))
print('Maximum Flight Plan Distance [NM]: '+str(max_flpl_dist))
print('Pop-up Scaling [%]: '+str(popup_scaling*100))

A=open(filename,'r')
lines=A.readlines()
A.close()

FlightIdentifiers=[]
for line in lines:
    item=line.strip().split(" ")
    FlightIdentifiers.append(item[16].strip().upper()) # Extract Flight Identifiers from .so6 traffic file

FlightIdentifiers=list(set((FlightIdentifiers))) # Remove duplicates

AllFlights=Flights() # Construct AllFlights object

for flight in FlightIdentifiers:
    segments,origin,destination,actype,timeb,FLb,CallSign,Dateb,LATb,LONb,Sequence=FlightInfo(flight,lines) 
    AllFlights.create_flight(flight,CallSign[0],actype[0],origin[0],timeb[0],Dateb[0],destination[0]) 
    for k in range(len(segments)):
        segment=segments[k]
        if segment[0].strip() != '*':
            item=segments[k].strip().split("_")
            if item[0] not in wpt_exclusionlist: # Sometimes necessary to remove certain waypoint for the sake of convenience (e.g. ROBVI). If this waypoint is not deleted, last wpt before SUGOL is SOBVI, which is located too close to SUGOL to sufficiently decelerate. For convenience, SOBVI is removed. Only has limited impact, as wpt is only used after MONIL and LUTEX
                AllFlights.Route_outside_TMA[-1].addwpt(item[0],LATb[k],LONb[k],FLb[k]) 
              
A=open('TMAroutes.txt','r') # Extract data from TMA routes file
lines=A.readlines()
A.close()    

B=open('waypoints.dat','r')
lines2=B.readlines()
B.close()
del lines2[0] # Necessary to remove header

C=open(data_path+'/global/airports.dat','r')
lines3=C.readlines()
C.close()
del lines3[0] # Necessary to remove header

tempdatabase_wpt=[]
tempdatabase_wptlat=[]
tempdatabase_wptlon=[]

tempdatabase_apt=[]
tempdatabase_aptlat=[]
tempdatabase_aptlon=[]

for j in range(len(AllFlights.Route_outside_TMA)): # Find IAF used and set route within TMA
    AllFlights.Route_outside_TMA[j].findIAF(possible_IAFs) # Which IAF is used by a particular aircraft?
	
    AllFlights.Route_outside_TMA[j].find_CBAS_waypoint() # Add CBAS as waypoint
    AllFlights.Route_outside_TMA[j].remove_intermediate_waypoints() # Remove unwanted waypoints
	
    AllFlights.Route_outside_TMA[j].calc_dist_and_heading() # Calculate distance and heading between waypoints
    AllFlights.Route_outside_TMA[j].delete_tooshort_legs() # Delete short legs
    AllFlights.Route_outside_TMA[j].calc_dist_and_heading() # Re-calculate distance and heading between waypoints
    AllFlights.Route_outside_TMA[j].delete_tooshort_legs() # Delete short legs
    AllFlights.Route_outside_TMA[j].calc_dist_and_heading() # Re-calculate distance and heading between waypoints
    AllFlights.Route_outside_TMA[j].findFlightPathAngle() # Find flight path angle
    
    idx=AllFlights.Route_outside_TMA[j].waypoints.index(AllFlights.Route_outside_TMA[j].whichIAF)
    AllFlights.Route_outside_TMA[j].delwpts_fromIAFonwards(idx) # Delete waypoints from IAF onwards   
    
    AllFlights.Route_outside_TMA[j].findPhase() # Find flight phase for each segment
      
    AllFlights.Route_outside_TMA[j].findalmostIAF() # Find waypoint before IAF
    
    AllFlights.Route_outside_TMA[j].findLocation() # Segment type
        
    AllFlights.Route_outside_TMA[j].findRWY(AllFlights.Route_outside_TMA[j].whichIAF,possible_IAFs,runways_use_land,j) # Find runway
        
    # Find the necessary TMA route waypoints and add to route object
    TMAroute_waypoints=find_TMAroute(lines,AllFlights.Route_outside_TMA[j].whichIAF,AllFlights.Route_outside_TMA[j].whichRWY)
    
    for k in range(len(TMAroute_waypoints)):   
        if TMAroute_waypoints[k] not in tempdatabase_wpt:
            LAT,LON=obtain_TMAwpt_data(TMAroute_waypoints[k],lines2)
            tempdatabase_wpt.append(TMAroute_waypoints[k])
            tempdatabase_wptlat.append(LAT)
            tempdatabase_wptlon.append(LON)
        elif TMAroute_waypoints[k] in tempdatabase_wpt:
            idx=tempdatabase_wpt.index(TMAroute_waypoints[k])
            LAT=tempdatabase_wptlat[idx]
            LON=tempdatabase_wptlon[idx]
            del idx
        AllFlights.Route_TMA[j].addTMAwpt(TMAroute_waypoints[k],LAT,LON)
        del LAT,LON
        
    AllFlights.Origin_LAT.append(AllFlights.Route_outside_TMA[j].LAT[0])
    AllFlights.Origin_LON.append(AllFlights.Route_outside_TMA[j].LON[0])
    
    if AllFlights.Destination[j] not in tempdatabase_apt:
        LAT,LON=obtain_apt_data(AllFlights.Destination[j],lines3)
        tempdatabase_apt.append(AllFlights.Destination[j])
        tempdatabase_aptlat.append(LAT)
        tempdatabase_aptlon.append(LON)        
    elif AllFlights.Destination[j] in tempdatabase_apt:
        idx=tempdatabase_apt.index(AllFlights.Destination[j])
        LAT=tempdatabase_aptlat[idx]
        LON=tempdatabase_aptlon[idx]
    AllFlights.Destination_LAT.append(LAT)
    AllFlights.Destination_LON.append(LON)
    del LAT,LON
    
    AllFlights.Route_TMA[j].determine_extrawpts(AllFlights.Route_outside_TMA[j].whichRWY,allrunways,allrunways_opposite,lines,lines2) # Find extra waypoints
    
    AllFlights.Route_TMA[j].calc_dist_and_heading() # Calculate distance and heading between waypoints
    
    AllFlights.Route_TMA[j].findFAF() # Find FAF (last waypoint before runway)    
    
    AllFlights.Route_TMA[j].findLocation() # Segment type
    
    AllFlights.calculate_distances(j,AMAN_horizon,Popup_exclusion_list) # Calculate distances for overall flight (direct in-between and total flight plan distance)
	
    AllFlights.Route_TMA[j].calculate_altitudes() # Calculate altitude inside TMA
    
	# Calculate speeds
    AllFlights.Route_outside_TMA[j].calculate_Speeds(nom_climb,nom_cruise_M,nom_cruise_spd,nom_CAS_TOD_almost_IAF,min_climb,min_cruise_M,min_cruise_spd,min_CAS_TOD_almost_IAF) # Outside TMA
    AllFlights.Route_TMA[j].calculate_Speeds(AllFlights.Route_outside_TMA[j],nom_CAS_almostIAF_IAF,nom_CAS_IAF_FAF,nom_CAS_FAF_RWY,min_CAS_almostIAF_IAF,min_CAS_IAF_FAF,min_CAS_FAF_RWY) # Inside TMA
    
    # Estimate flying times
    AllFlights.Route_TMA[j].estimate_flyingtimes() # In TMA
    AllFlights.Route_outside_TMA[j].estimate_flyingtimes(AllFlights.Route_TMA[j]) # Outside TMA
    AllFlights.Route_outside_TMA[j].estimate_flyingtime_CBAS() # To CBAS
    AllFlights.calculate_total_estFT(j) # Total
    
    AllFlights.Route_outside_TMA[j].calc_directdist_wpt_RWY(AllFlights.Route_TMA[j]) # Calculate direct distance
    
    # Determine how much delay can be absorbed by reducing speed from nominal speed to minimum speed in each segment
    AllFlights.Route_TMA[j].calculate_maxpossible_spddelabs() # In TMA
    AllFlights.Route_outside_TMA[j].calculate_maxpossible_spddelabs(AllFlights.Route_TMA[j]) # Outside TMA
    AllFlights.calculate_maxpossible_spddelabs(j) # Total
    
    AllFlights.estimate_CBAS_IAF_runway_arrtimes(j) # Calculate pre-departure estimates for arrival times at CBAS, IAF and RWY
    
    AllFlights.determine_start_heading(j) # Determine start heading
 
######################################################################################## 

# Edit the scenario, such that it is more to my liking
# First provide some information on the 'original' dataset
totflights=len(AllFlights.CallSign)
popupflights=AllFlights.PopupLabel.count('POPUP')
popupratio=float(popupflights)/float(totflights)
print
print('Original Pop-up Flights: '+str(popupflights))
print('Original Total Flights: '+str(totflights))
print('Original Pop-up Ratio [%]: '+str(100*popupratio))

# Secondly, edit the scenario. 
print
print('************************************* Editing Scenario **************************************')
# Remove all flights that are too long
removed_flights_callsign=[]
new_flights_callsign=[]

counter_replaced_longhaul=0

z=0 # Index that will select a new flight

# Find suitable flight (no pop-up, no long-distance)
for j in range(len(AllFlights.Route_outside_TMA)):
    if AllFlights.Total_flightplan_dist[j]>max_flpl_dist:
        repl=False
        while repl==False:
            
            if AllFlights.PopupLabel[z]=='NORMAL' and AllFlights.Origin[z] !='EDDS' and AllFlights.Total_flightplan_dist[z]<=max_flpl_dist and AllFlights.Route_outside_TMA[z].whichIAF==AllFlights.Route_outside_TMA[j].whichIAF and AllFlights.Route_outside_TMA[z].whichRWY==AllFlights.Route_outside_TMA[j].whichRWY: # Check that this flights is 1) no pop-up flight and 2) no long-haul flight
                removed_flights_callsign.append(AllFlights.CallSign[j])                
                
                AllFlights.replace_flight(j,z,'REP'+str(counter_replaced_longhaul)) # j is the long-haul flight, z the NORMAL
                
                repl=True 
                
                counter_replaced_longhaul=counter_replaced_longhaul+1
                
                new_flights_callsign.append(AllFlights.CallSign[j])
                
            z=z+1
            if z>(len(AllFlights.Route_outside_TMA)-1):
                z=0
                
print 'Replaced Flights (Longhaul > Normal): ',counter_replaced_longhaul
      
# Add pop-up flights if necessary (replace normal flights, add pop-up flights)
if popup_scaling>1:
    indexes_tobereplaced_start=[]
    indexes_tobereplaced_final=[]
    IAFS_tobereplaced_final=[]    
    RWYS_tobereplaced_final=[]    
    
    indexes_replacements_start=[]
    indexes_replacements_final=[]
    
    popupflights_tobeadded=int(min(totflights-popupflights,round(popupflights*popup_scaling)-popupflights))
 
    tempor=int(floor(totflights/popupflights_tobeadded))
    
    for k in range(popupflights_tobeadded):
        indexes_tobereplaced_start.append(-1+k*tempor)
        indexes_replacements_start.append(-1+k*tempor)
    
    for element in indexes_tobereplaced_start:
        repl=False
              
        while repl==False:
            element=element+1
            if element>(len(AllFlights.CallSign)-1):
                element=0
                
            if AllFlights.PopupLabel[element]=='NORMAL' and element not in indexes_tobereplaced_final:
                indexes_tobereplaced_final.append(element)
                IAFS_tobereplaced_final.append(AllFlights.Route_outside_TMA[element].whichIAF)
                RWYS_tobereplaced_final.append(AllFlights.Route_outside_TMA[element].whichRWY)
                repl=True
       
    print  indexes_tobereplaced_final
    
    counter=0        
    for element in indexes_replacements_start:
        repl=False
        
        countertemp=0
        
        while repl==False:
            element=element+1
            if element>(len(AllFlights.CallSign)-1):
                element=0    
                
            if countertemp<500:
                if AllFlights.PopupLabel[element]=='POPUP' and AllFlights.Route_outside_TMA[element].whichIAF==IAFS_tobereplaced_final[counter] and AllFlights.Route_outside_TMA[element].whichRWY==RWYS_tobereplaced_final[counter]:
                    indexes_replacements_final.append(element)
                    repl=True
                       
            if countertemp>=500:
                if AllFlights.PopupLabel[element]=='POPUP' and AllFlights.Route_outside_TMA[element].whichRWY==RWYS_tobereplaced_final[counter]:
                    indexes_replacements_final.append(element)
                    repl=True
                    
            if countertemp>=1000: # In certain cases it is necessary to revise the NORMAL flight that had to be replaced, as there is no pop-up flight using the same IAF/RWY
                nextindex=indexes_tobereplaced_final[counter]+1
                while AllFlights.PopupLabel[nextindex]=='POPUP' or (nextindex in indexes_tobereplaced_final):
                    nextindex=nextindex+1
                    if nextindex>(len(AllFlights.PopupLabel)-1):
                        nextindex=0
                
                indexes_tobereplaced_final[counter]=nextindex
                IAFS_tobereplaced_final[counter]=AllFlights.Route_outside_TMA[nextindex].whichIAF
                RWYS_tobereplaced_final[counter]=AllFlights.Route_outside_TMA[nextindex].whichRWY
                countertemp=0               
                
                del nextindex
            
            countertemp=countertemp+1
        
        counter=counter+1
        
    counter_replaced_extrapopup=0
    for z in range(len(indexes_tobereplaced_final)):  
        AllFlights.replace_flight(indexes_tobereplaced_final[z],indexes_replacements_final[z],'POP'+str(counter_replaced_extrapopup))
        counter_replaced_extrapopup=counter_replaced_extrapopup+1
    
    print 'Replaced Flights (Normal > Pop-up): ',counter_replaced_extrapopup

    del element
 
# Remove pop-up flights if necessary
if popup_scaling<1:
    indexes_tobereplaced_start=[]
    indexes_tobereplaced_final=[]
    IAFS_tobereplaced_final=[]
    RWYS_tobereplaced_final=[]    
    
    indexes_replacements_start=[]
    indexes_replacements_final=[]
    
    popupflights_toberemoved=int(min(popupflights,popupflights-round(popupflights*popup_scaling)))
 
    tempor=int(floor(totflights/popupflights_toberemoved))
    
    for k in range(popupflights_toberemoved):
        indexes_tobereplaced_start.append(-1+k*tempor)
        indexes_replacements_start.append(-1+k*tempor)  
          
    for element in indexes_tobereplaced_start:
        repl=False
        
        while repl==False:
            element=element+1
            if element>(len(AllFlights.CallSign)-1):
                element=0    
                
            if AllFlights.PopupLabel[element]=='POPUP' and element not in indexes_tobereplaced_final:
                indexes_tobereplaced_final.append(element)
                IAFS_tobereplaced_final.append(AllFlights.Route_outside_TMA[element].whichIAF)
                RWYS_tobereplaced_final.append(AllFlights.Route_outside_TMA[element].whichRWY)
                repl=True
    
    counter=0
    for element in indexes_replacements_start:
        repl=False
        
        countertemp=0
        
        while repl==False:
            element=element+1
            if element>(len(AllFlights.CallSign)-1):
                element=0
            
            if countertemp<500:
                if AllFlights.PopupLabel[element]=='NORMAL' and AllFlights.Origin[element]!='EDDS' and AllFlights.Route_outside_TMA[element].whichIAF==IAFS_tobereplaced_final[counter] and AllFlights.Route_outside_TMA[element].whichRWY==RWYS_tobereplaced_final[counter]:
                    indexes_replacements_final.append(element)
                    repl=True
            
            if countertemp>=500:
                if AllFlights.PopupLabel[element]=='NORMAL' and AllFlights.Origin[element]!='EDDS' and AllFlights.Route_outside_TMA[element].whichRWY==RWYS_tobereplaced_final[counter]:
                    indexes_replacements_final.append(element)
                    repl=True
            
            countertemp=countertemp+1
        
        counter=counter+1        
        
    counter_replaced_extranormal=0
    for z in range(len(indexes_tobereplaced_final)): 
        AllFlights.replace_flight(indexes_tobereplaced_final[z],indexes_replacements_final[z],'NOR'+str(counter_replaced_extranormal))
        counter_replaced_extranormal=counter_replaced_extranormal+1
    
    print 'Replaced Flights (Pop-up > Normal): ',counter_replaced_extranormal

    del element

# Scenario editing completed
totflights=len(AllFlights.CallSign)
popupflights=AllFlights.PopupLabel.count('POPUP')
popupratio=float(popupflights)/float(totflights)
print('Revised Pop-up Flights: '+str(popupflights))
print('Revised Total Flights: '+str(totflights))
print('Revised Pop-up Ratio [%]: '+str(100*popupratio))

print
print('********************************* Editing Scenario Finished *********************************')

######################################################################################## 

print('*********************************** Preparing Simulation ************************************')
# Prepare variables for scenario file
simulation_start=min(AllFlights.SimTime) # Start point simulation
time_var=np.arange(simulation_start,simulation_start+24.*3600.,1)

# Scenario file for BlueSky
if '--node' in sys.argv:
    outputfile=open('scenario/' + str(var_name) + '.scn','w') # Specifies output file
else:
    outputfile=open('scenario/scenariotest' + '.scn','w') # Specifies output file

outputfile.write('#********************************************************************************************* \n')
outputfile.write('#********************************************************************************************* \n')
outputfile.write('#************************************ ARSIM SCENARIO FILE ************************************ \n')
outputfile.write('#********************************************************************************************* \n')
outputfile.write('#*********************************************************************************************')
outputfile.write('\n')
outputfile.write('\n')
outputfile.write('00:00:0>FF')
outputfile.write('\n')
outputfile.write('\n')
outputfile.write('00:00:0>ASAS OFF')
	
for time in time_var:
    for k in range(len(AllFlights.SimTime)):
        if time==AllFlights.SimTime[k]:
            scenario_creator(AllFlights.FlightIdentifier[k])
outputfile.close()

# Information file on all flights and parameters
if '--node' in sys.argv:
    outputfile2=open('scenario/' + str(var_name) + '_flight_information' + '.txt','w') # Specifies output file
else:
    outputfile2=open('scenario/flight_information' + '.txt','w') # Specifies output file

for k in range(len(AllFlights.CallSign)):
    outputfile2.write(str(AllFlights.CallSign[k]) + \
    ', ' + str(AllFlights.PopupLabel[k]) + \
    ', ORIG:' + str(AllFlights.Origin[k]) + \
    ', DEST:' + str(AllFlights.Destination[k]) +  \
    ', DIRECT DIST:' + str(int(AllFlights.Direct_inbetween_dist[k])) + \
    ', FlPl DIST:' + str(int(AllFlights.Total_flightplan_dist[k])) + \
    ', Est Nom Total FT: ' + str(int(AllFlights.Total_estFT[k])) + \
    ', Est Max Total FT: ' + str(int(AllFlights.Total_estmaxFT[k])) + \
    ', MaxPossSpdDelAbs Total: ' + str(int(AllFlights.Maxposs_spddelabs_total[k])) + \
    ', Outside TMA DIST:'  + str(int(AllFlights.Route_outside_TMA[k].totdist)) + \
    ', Outside TMA NomEstFT: ' + str(int(AllFlights.Route_outside_TMA[k].totestFT)) + \
    ', Outside TMA MaxEstFT: ' + str(int(AllFlights.Route_outside_TMA[k].totestmaxFT)) + \
    ', Outside TMA MaxPossDelAbs:' + str(int(AllFlights.Route_outside_TMA[k].maxposs_spddelabs_total)) + \
    ', IAF:' + str(AllFlights.Route_outside_TMA[k].whichIAF) + \
    ', TMA DIST:' + str(int(AllFlights.Route_TMA[k].totdist)) + \
    ', TMA NomEstFT: ' + str(int(AllFlights.Route_TMA[k].totestFT)) + \
    ', TMA MaxEstFT: ' + str(int(AllFlights.Route_TMA[k].totestmaxFT)) + \
    ', TMA MaxPossSpdDelAbs: ' + str(int(AllFlights.Route_TMA[k].maxposs_spddelabs_total)) + \
    ', RWY:' + str(AllFlights.Route_outside_TMA[k].whichRWY) + '\n')
    outputfile2.write(str(AllFlights.CallSign[k]) + \
    ', SimTime: ' + str(int(AllFlights.SimTime[k])) + \
    ', ST-sim_start: ' + str(int(AllFlights.SimTime[k]-simulation_start)) + \
    ', Est_at_CBAS: ' + str(int(AllFlights.PreDepEstTime_at_CBAS[k])) + \
    ', Est_at_CBAS corrected: ' + str(int(AllFlights.PreDepEstTime_at_CBAS[k]-simulation_start)) + \
    ', Est_at_IAF: ' + str(int(AllFlights.PreDepEstTime_at_IAF[k])) + \
    ', Est_at_IAF corrected: ' + str(int(AllFlights.PreDepEstTime_at_IAF[k]-simulation_start)) + \
    ', Est_at_RWY: ' + str(int(AllFlights.PreDepEstTime_at_RWY[k])) + \
    ', Est_at_RWY corrected: ' + str(int(AllFlights.PreDepEstTime_at_RWY[k]-simulation_start)) + \
    ', Start-RWY: ' + str(int(AllFlights.PreDepEstTime_at_RWY[k]-AllFlights.SimTime[k])) + \
    ', IAF-RWY: ' + str(int(AllFlights.PreDepEstTime_at_RWY[k]-AllFlights.PreDepEstTime_at_IAF[k])) + '\n')
    outputfile2.write('\n') 
   
    for j in range(len(AllFlights.Route_outside_TMA[k].waypoints)):
        outputfile2.write(str(AllFlights.CallSign[k]) + \
        ', ' + str(AllFlights.Route_outside_TMA[k].waypoints[j]) +  \
        ', Dist_IAF:' +  str(int(AllFlights.Route_outside_TMA[k].dist_to_IAF[j])) + \
        ', DistLeg:' + str((AllFlights.Route_outside_TMA[k].dist[j]))  + \
        ', Heading:' + str(AllFlights.Route_outside_TMA[k].heading[j]) + \
        ', EstNomFT:' + str(int(AllFlights.Route_outside_TMA[k].estFT[j]))   + \
        ', EstMaxFT:' + str(int(AllFlights.Route_outside_TMA[k].estmaxFT[j])) + \
        ', MaxPossSpdDelAbs:' + str(int(AllFlights.Route_outside_TMA[k].maxposs_spddelabs_segment[j]))   + \
        ', NomEstFT_IAF:' + str(int(AllFlights.Route_outside_TMA[k].estFT_to_IAF[j]))  + \
        ', MaxEstFT_IAF:' + str(int(AllFlights.Route_outside_TMA[k].estmaxFT_to_IAF[j]))  + \
        ', MaxPossSpdDelAbs_IAF:' + str(int(AllFlights.Route_outside_TMA[k].maxposs_spddelabs_to_IAF[j]))  + \
        ', NomEstFT_RWY:' + str(int(AllFlights.Route_outside_TMA[k].estFT_to_RWY[j]))  + \
        ', MaxEstFT_RWY:' + str(int(AllFlights.Route_outside_TMA[k].estmaxFT_to_RWY[j]))  + \
        ', MaxPossSpdDelAbs_RWY:' + str(int(AllFlights.Route_outside_TMA[k].maxposs_spddelabs_to_RWY[j]))  + \
        ', DirectDist_RWY:' + str(int(AllFlights.Route_outside_TMA[k].directdist_RWY[j]))  + \
        ', NomCAS:'  + str(int(AllFlights.Route_outside_TMA[k].spd[j])) + \
        ', NomTAS:' + str(int(AllFlights.Route_outside_TMA[k].spd_TAS[j])) + \
        ', MinCAS:'  + str(int(AllFlights.Route_outside_TMA[k].minspd[j])) + \
        ', MinTAS:' + str(int(AllFlights.Route_outside_TMA[k].minspd_TAS[j])) + \
        ', ALT:' + str(int(float(AllFlights.Route_outside_TMA[k].FL[j])*100)) + \
        ', FPA:' + str(AllFlights.Route_outside_TMA[k].flpathangle[j]) + \
        ', ' + str(AllFlights.Route_outside_TMA[k].phase[j]) + \
        ', ' + str(AllFlights.Route_outside_TMA[k].loc[j]) + '\n' )
    outputfile2.write('\n')    
    
    for l in range(len(AllFlights.Route_TMA[k].waypoints)):
        outputfile2.write(str(AllFlights.CallSign[k]) + \
        ', ' + str(AllFlights.Route_TMA[k].waypoints[l]) +  \
        ', Dist_RWY:' +  str(int(AllFlights.Route_TMA[k].dist_to_RWY[l])) + \
        ', DistLeg:' + str((AllFlights.Route_TMA[k].dist[l])) + \
        ', Heading:' + str(AllFlights.Route_TMA[k].heading[l]) + \
        ', NomEstFT:' + str(int(AllFlights.Route_TMA[k].estFT[l])) + \
        ', MaxEstFT:' + str(int(AllFlights.Route_TMA[k].estmaxFT[l])) + \
        ', MaxPossSpdDelAbs:' + str(int(AllFlights.Route_TMA[k].maxposs_spddelabs_segment[l]))   + \
        ', NomEstFT_RWY:' + str(int(AllFlights.Route_TMA[k].estFT_to_RWY[l]))  + \
        ', MaxEstFT_RWY:' + str(int(AllFlights.Route_TMA[k].estmaxFT_to_RWY[l]))  + \
        ', MaxPossSpdDelAbs_RWY:' + str(int(AllFlights.Route_TMA[k].maxposs_spddelabs_to_RWY[l]))  + \
        ', NomCAS:' + str(int(AllFlights.Route_TMA[k].spd[l])) + \
        ', NomTAS:' + str(int(AllFlights.Route_TMA[k].spd_TAS[l])) + \
        ', MinCAS:' + str(int(AllFlights.Route_TMA[k].minspd[l])) + \
        ', MinTAS:' + str(int(AllFlights.Route_TMA[k].minspd_TAS[l])) + \
        ', ALT:' + str(int(AllFlights.Route_TMA[k].FL[l]*100)) + \
        ', TMA ' + str(AllFlights.Route_TMA[k].phase[l]) + \
        ', ' + str(AllFlights.Route_TMA[k].loc[l]) + '\n' )
    outputfile2.write('\n \n \n \n \n')    
    
outputfile2.close()

if len(sys.argv)<2:
	var_name = 'scenariotest'
	var_txt = open('variables.txt','w')
	var_txt.write(str(var_name)+'\n') 			# Name
	var_txt.write('Dataset1'+'\n') 				# Dataset
	var_txt.write(str(popup_scaling*100)+'\n') 	# popup_scaling
	var_txt.write('EAMAN'+'\n') 				# AMAN
	var_txt.write('ASAPBASIC'+'\n') 			# Trajectory Predictor
	var_txt.write('0'+'\n') 					# Pre-departure delay
	var_txt.write(str(approach_margin)+'\n') 	# Approach margin
	var_txt.close()
	var_predeparture_delay = float(0.)

# Simulation ready
print('************************************** Simulation Ready *************************************')