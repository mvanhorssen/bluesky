#Scenario_Post_Analyser.py
import numpy as np
import pickle
import sys

show_graphs_sw=False

#First read pickled data (Make sure the order is identical as in the PreAnalyser)
if len(sys.argv)>1:
    fnametempor=str(sys.argv[1])
else:
    fnametempor='214scenario2c12' #Specify file (without .pkl extension) to be read  

#fnametempor='scenariotest' 
    
with open(fnametempor+'.pkl','rb') as input:
    #IMPORTANT! SAME ORDER AS IN PRE-ANALYSER
    SimulationParameters=pickle.load(input)    
    
    CallSigns=list(pickle.load(input))
    PreDepEstTimes_at_RWY=list(pickle.load(input))
    PopupLabels=list(pickle.load(input))
    Direct_inbetween_dists=list(pickle.load(input))
    SimTimes=list(pickle.load(input))
    Origins=list(pickle.load(input))      
	
    IAFs=list(pickle.load(input))
    RWYs=list(pickle.load(input))
	
    Total_flightplan_dists=list(pickle.load(input))
    PreDepEstTimes_at_IAF=list(pickle.load(input))      
    
    LOG_times_at_IAF=list(pickle.load(input))
    LOG_times_at_RWY=list(pickle.load(input))
    LOG_accuracies_predepests_at_IAF=list(pickle.load(input))
    LOG_accuracies_predepests_at_RWY=list(pickle.load(input))
    LOG_IAFs_passed=list(pickle.load(input))
    LOG_RWYs_passed=list(pickle.load(input))
    LOG_delivery_accuracies_IAF=list(pickle.load(input))
	
    LOG_schtimehist_schtimes=list(pickle.load(input))
    LOG_schtimehist_disttorwys=list(pickle.load(input))
    LOG_schtimehist_flightphases=list(pickle.load(input))
    LOG_schtimehist_STAstatuses=list(pickle.load(input))
    LOG_schtimehist_simtimes=list(pickle.load(input)) #not yet
    
    LOG_energycosts=list(pickle.load(input))
    
    LOG_lowlevel_delabs_times=list(pickle.load(input))
    LOG_lowlevel_delabs_dists=list(pickle.load(input))
    LOG_lowlevel_delabs_types=list(pickle.load(input))
    LOG_lowlevel_delabs_IAFs=list(pickle.load(input))
    LOG_lowlevel_delabs_simtimes=list(pickle.load(input)) #not yet        

    LOG_seqhist_numbers=list(pickle.load(input))
    LOG_seqhist_disttorwys=list(pickle.load(input))
    LOG_seqhist_flightphases=list(pickle.load(input))
    LOG_seqhist_STAstatuses=list(pickle.load(input))
	
    PreDepEstTimes_at_CBAS=list(pickle.load(input))
    LOG_CBAS_passed=list(pickle.load(input))
    LOG_times_at_CBAS=list(pickle.load(input))
    LOG_accuracies_predepests_at_CBAS=list(pickle.load(input))
	
    LOG_speed_changes_before_TOD_per_1_kts=list(pickle.load(input))
    LOG_speed_changes_after_TOD_per_1_kts=list(pickle.load(input))
    LOG_speed_changes_before_TOD_per_5_kts=list(pickle.load(input))
    LOG_speed_changes_after_TOD_per_5_kts=list(pickle.load(input))
	
    LOG_trafficbunchhist_esttime=list(pickle.load(input))
    LOG_trafficbunchhist_disttorwy=list(pickle.load(input))
    LOG_trafficbunchhist_STAstatus=list(pickle.load(input))
    LOG_trafficbunchhist_currdelay=list(pickle.load(input))
    LOG_trafficbunchhist_simtime=list(pickle.load(input))
#


#First print some numbers
print 
print 
print
print str(fnametempor)
print '---'
print
print 'RWY27/RWY18C count: ',RWYs.count('27'),RWYs.count('18C')
print 'ARTIP/RIVER/SUGOL count: ',IAFs.count('ARTIP'),IAFs.count('RIVER'),IAFs.count('SUGOL')

dogleg_delays=[]
twosem_delays=[]
holding_delays=[]

for k in range(len(LOG_lowlevel_delabs_times)):
    if LOG_lowlevel_delabs_types[k]=='DogLeg':
        dogleg_delays.append(LOG_lowlevel_delabs_times[k])
    elif LOG_lowlevel_delabs_types[k]=='TwoSemicircles':
        twosem_delays.append(LOG_lowlevel_delabs_times[k])
    elif LOG_lowlevel_delabs_types[k]=='HoldingStack':
        holding_delays.append(LOG_lowlevel_delabs_times[k])

average_dogleg=np.mean(dogleg_delays)
average_twosem=np.mean(twosem_delays)
average_holding=np.mean(holding_delays)

print
print 'Average amount of speed changes before TOD per 1 kts: ',np.mean(LOG_speed_changes_before_TOD_per_1_kts), np.max(LOG_speed_changes_before_TOD_per_1_kts)
print 'Average amount of speed changes after TOD per 1 kts: ',np.mean(LOG_speed_changes_after_TOD_per_1_kts), np.max(LOG_speed_changes_after_TOD_per_1_kts)
print 'Average amount of speed changes before TOD per 5 kts: ',np.mean(LOG_speed_changes_before_TOD_per_5_kts), np.max(LOG_speed_changes_before_TOD_per_5_kts)
print 'Average amount of speed changes after TOD per 5 kts: ',np.mean(LOG_speed_changes_after_TOD_per_5_kts), np.max(LOG_speed_changes_after_TOD_per_5_kts)

print 
print 'Average low-level del. abs. [s]: ',np.mean(LOG_lowlevel_delabs_times)
print 'None [ac]: ',LOG_lowlevel_delabs_types.count('None')
print 'Dog [ac/s]: ',LOG_lowlevel_delabs_types.count('DogLeg'),' ',average_dogleg
print 'TwoSem [ac/s]: ',LOG_lowlevel_delabs_types.count('TwoSemicircles'),' ',average_twosem
print 'Stack [ac/s]: ',LOG_lowlevel_delabs_types.count('HoldingStack'),' ',average_holding

#Additional check: last STA for both runways
runway1_lastSTAs=[]
runway2_lastSTAs=[]

for k in range(len(CallSigns)):
    individualac_lastSTA=LOG_schtimehist_schtimes[k][-1]

    if RWYs[k]=='27':
        runway1_lastSTAs.append(individualac_lastSTA)
    elif RWYs[k]=='18C':    
        runway2_lastSTAs.append(individualac_lastSTA)

print 
print 'RWY 27/RWY18C last STA: ',max(runway1_lastSTAs),max(runway2_lastSTAs)

sorted_runway1_lastSTAs=runway1_lastSTAs
sorted_runway2_lastSTAs=runway2_lastSTAs

sorted_runway1_lastSTAs.sort()
sorted_runway2_lastSTAs.sort()

diff_rwy1_lastSTAs=[]
diff_rwy2_lastSTAs=[]
 
for k in range(len(sorted_runway1_lastSTAs)-1):
    diff_rwy1_lastSTAs.append(sorted_runway1_lastSTAs[k+1]-sorted_runway1_lastSTAs[k])
    
for k in range(len(sorted_runway2_lastSTAs)-1):
    diff_rwy2_lastSTAs.append(sorted_runway2_lastSTAs[k+1]-sorted_runway2_lastSTAs[k])

sorted_diff_rwy1_lastSTAs=diff_rwy1_lastSTAs
sorted_diff_rwy2_lastSTAs=diff_rwy2_lastSTAs
sorted_diff_rwy1_lastSTAs.sort()
sorted_diff_rwy2_lastSTAs.sort()

print 
print 'Should be 100 (or larger): ',min(sorted_diff_rwy1_lastSTAs),min(sorted_diff_rwy2_lastSTAs)
print 'Average int.arr.time RWY27: ',np.mean(sorted_diff_rwy1_lastSTAs),np.mean(diff_rwy1_lastSTAs[:int(len(diff_rwy1_lastSTAs)*0.90)])
print 'Average int.arr.time RWY18C: ',np.mean(sorted_diff_rwy2_lastSTAs),np.mean(diff_rwy2_lastSTAs[:int(len(diff_rwy2_lastSTAs)*0.90)])

#Clear up schedule time history by only considering ONLY semi-fixed changes
cleared_schtimehist_schtimes=[]
cleared_schtimehist_disttorwys=[]
cleared_schtimehist_flightphases=[]
cleared_schtimehist_STAstatuses=[]
absolute_STA_difference_individualac=[]
required_revisions_individualac=[]
STA_difference_allaircraft=[]
absolute_STA_difference_individualac_beforeTOD=[]
absolute_STA_difference_individualac_afterTOD=[]
STAdiff_allairc_beforeTOD=[]
STAdiff_allairc_afterTOD=[]
counter_STA_rev_beforeTOD=0
counter_STA_rev_afterTOD=0

for k in range(len(CallSigns)):
    cleared_schtimehist_schtimes.append([])
    cleared_schtimehist_disttorwys.append([])
    cleared_schtimehist_flightphases.append([])
    cleared_schtimehist_STAstatuses.append([])
    
    absolute_STA_difference_individualac.append([])
    absolute_STA_difference_individualac_beforeTOD.append([])           
    absolute_STA_difference_individualac_afterTOD.append([])           
           
    for l in range(len(LOG_schtimehist_schtimes[k])):
            if LOG_schtimehist_STAstatuses[k][l]=='Semi-Fixed':
                
#                if l==0:
#                    absolute_STA_difference_individualac[k].append(0.)
#                elif l>0 and LOG_schtimehist_STAstatuses[k][l-1]=='OFF':
#                    absolute_STA_difference_individualac[k].append(0.)
#                
                if l>0 and LOG_schtimehist_STAstatuses[k][l-1]!='OFF':
                    if (LOG_schtimehist_schtimes[k][l]-LOG_schtimehist_schtimes[k][l-1])>5.: #Only record if STA deviates by more than +5seconds 
                        cleared_schtimehist_schtimes[k].append(LOG_schtimehist_schtimes[k][l])
                        cleared_schtimehist_disttorwys[k].append(LOG_schtimehist_disttorwys[k][l])
                        cleared_schtimehist_flightphases[k].append(LOG_schtimehist_flightphases[k][l])
                        cleared_schtimehist_STAstatuses[k].append(LOG_schtimehist_STAstatuses[k][l])
                                    
                        absolute_STA_difference_individualac[k].append(LOG_schtimehist_schtimes[k][l]-LOG_schtimehist_schtimes[k][l-1])
                        STA_difference_allaircraft.append(LOG_schtimehist_schtimes[k][l]-LOG_schtimehist_schtimes[k][l-1])        
            
                        if LOG_schtimehist_flightphases[k][l]=='Before':
                            absolute_STA_difference_individualac_beforeTOD[k].append(STA_difference_allaircraft[-1])
                            counter_STA_rev_beforeTOD=counter_STA_rev_beforeTOD+1
                            STAdiff_allairc_beforeTOD.append(absolute_STA_difference_individualac_beforeTOD[k][-1])
                        elif LOG_schtimehist_flightphases[k][l]=='After':
                            absolute_STA_difference_individualac_afterTOD[k].append(STA_difference_allaircraft[-1])
                            counter_STA_rev_afterTOD=counter_STA_rev_afterTOD+1
                            STAdiff_allairc_afterTOD.append(absolute_STA_difference_individualac_afterTOD[k][-1])
                            
sorted_STA_difference_allaircraft=STA_difference_allaircraft
sorted_STA_difference_allaircraft.sort()

print 
print 'Total STA Rev. when SF: ',len(STA_difference_allaircraft)
print 'Average STA Rev. [per ac]: ',float(len(STA_difference_allaircraft))/float(len(CallSigns))
print 'Average STA Diff. [s]: ',np.mean(np.abs(STA_difference_allaircraft))

if counter_STA_rev_beforeTOD!=0:
    print 'STA Rev. before TOD: ',counter_STA_rev_beforeTOD,np.mean(np.abs(STAdiff_allairc_beforeTOD))
if counter_STA_rev_beforeTOD==0:
    print 'STA Rev. before TOD: ',counter_STA_rev_beforeTOD


if counter_STA_rev_afterTOD!=0:
    print 'STA Rev. after TOD: ',counter_STA_rev_afterTOD,np.mean(np.abs(STAdiff_allairc_afterTOD))
elif counter_STA_rev_afterTOD==0:
    print 'STA Rev. after TOD: ',counter_STA_rev_afterTOD

absolute_pos_changes_individualac=[]
counter_pos_changes=0
#How many sequence position switches per aircraft?
for k in range(len(LOG_seqhist_numbers)):
    temp_abs_pos_change_ac=0
    
    for l in range(len(LOG_seqhist_numbers[k])):
        if l>0:
            if LOG_seqhist_STAstatuses[k][l]=='Semi-Fixed':
                temp_abs_pos_change_ac=temp_abs_pos_change_ac+np.abs(LOG_seqhist_numbers[k][l]-LOG_seqhist_numbers[k][l-1])
                counter_pos_changes=counter_pos_changes+1
                
    absolute_pos_changes_individualac.append(temp_abs_pos_change_ac)
    
print
print 'Total Sequence Change/Magnitude: ',counter_pos_changes,np.sum(np.abs(absolute_pos_changes_individualac))
print 'Average Seq. Ch. [per ac]: ',np.sum(absolute_pos_changes_individualac)/float(len(absolute_pos_changes_individualac))

#Now check how many aircraft have a disturbed descent
disturbed_descent_individualac=[]

for k in range(len(CallSigns)):
    if LOG_schtimehist_flightphases[k][-1]=='After':
        disturbed_descent_individualac.append(True)
    else:
        disturbed_descent_individualac.append(False)

total_disturbed_descents=disturbed_descent_individualac.count(True)
        
print 
print 'Disturbed Descents: ',total_disturbed_descents
print 'Ratio: ',float(total_disturbed_descents)/float(len(CallSigns))



#Energy cost per flight plan nm
energycost_perflplnm_individualac=[]

for k in range(len(CallSigns)):
    if LOG_energycosts[k]>0:
        energycost_perflplnm_individualac.append(LOG_energycosts[k]/Total_flightplan_dists[k])

print 'Average Energy per FlPl nm: ',np.mean(energycost_perflplnm_individualac)*1E-6


print
print 'IAF Deliv. Accuracy Abs. Value [s]: ',np.mean(np.abs(LOG_delivery_accuracies_IAF))
#plt.figure()
#plt.hist(LOG_delivery_accuracies_IAF)
#plt.show()

print
print 'CBAS Deliv. Accuracy Abs. Value [s]: ',np.mean(np.abs(LOG_accuracies_predepests_at_CBAS))


#print(LOG_CBAS_passed)
#print(LOG_times_at_CBAS)
#print(LOG_accuracies_predepests_at_CBAS)

sorted_LOG_time_CBAS_passed = LOG_CBAS_passed

def show_graphs(CallSigns,PreDepEstTimes_at_RWY,PopupLabels,Direct_inbetween_dists,simulation_start,sorted_runway1_lastSTAs,sorted_runway2_lastSTAs,LOG_times_at_RWY,LOG_lowlevel_delabs_times,LOG_lowlevel_delabs_simtimes):
        #Determine, for each time interval (d) during the whole day the number of landing aircraft, whether they are pop-up and the pop-up ratio
        
        #First remove un-landed last aircraft
        #LOG_times_at_RWY.remove(-999.)
        
        #initialisation
        counterpopup=[]
        counterother=[]
        countertotal=[]
        intervalvalue=[]
        
        ratiopopup=[]
        
        counter_planned_rwy1=[]
        counter_planned_rwy2=[]        
        
        counter_actual_landed=[]
        counter_actual_runway1=[]
        counter_actual_runway2=[]        
		
        counter_planned_CBAS_all=[]
        counter_planned_CBAS_ARTIP=[]
        counter_planned_CBAS_RIVER=[]
        counter_planned_CBAS_SUGOL=[]
        counter_planned_CBAS_18C=[]
        counter_planned_CBAS_27=[]
        counter_actual_CBAS_all=[]
        counter_actual_CBAS_ARTIP=[]
        counter_actual_CBAS_RIVER=[]
        counter_actual_CBAS_SUGOL=[]
        counter_actual_CBAS_18C=[]
        counter_actual_CBAS_27=[]
        
        average_lowlev_delay_interval=[]        
        
        #
        
        d=30*60 #width interval used throughout simulations
        
        for j in range(0+d,int(max(PreDepEstTimes_at_RWY)-simulation_start+1000),10*60): 
            #initialisation
            temppopup=0
            tempother=0
            temptotal=0
            
            temp_planned_rwy1=0
            temp_planned_rwy2=0            
            
            temp_actual_landed=0
            temp_actual_landed_runway1=0
            temp_actual_landed_runway2=0
			
            temp_planned_CBAS_all=0
            temp_planned_CBAS_ARTIP=0
            temp_planned_CBAS_RIVER=0
            temp_planned_CBAS_SUGOL=0
            temp_planned_CBAS_18C=0
            temp_planned_CBAS_27=0
            temp_actual_CBAS_all=0
            temp_actual_CBAS_ARTIP=0
            temp_actual_CBAS_RIVER=0
            temp_actual_CBAS_SUGOL=0
            temp_actual_CBAS_18C=0
            temp_actual_CBAS_27=0
            
            temp_interval_lowlev_delay=[]
            #
        
            intervalvalue.append(float(j))
        
            acceptedrange_low=j-d #Specify lower boundary for interval
            acceptedrange_high=j #Specify upper boundary for interval
        
            for idx in range(len(CallSigns)): #for each flight
        
                if (PreDepEstTimes_at_RWY[idx]-simulation_start) >=acceptedrange_low and (PreDepEstTimes_at_RWY[idx]-simulation_start) <=acceptedrange_high: #Check if flight within time range
                    temptotal=temptotal+1
        
                    if PopupLabels[idx]=='POPUP': #Check if flight pop-up flight
                        temppopup=temppopup+1 #Add +1 to number of pop-up flights in range
                        
        
                    elif PopupLabels[idx]=='NORMAL': #If no pop-up flight
                        tempother=tempother+1 #Add +1 to number of other flights in range
                        
                    if RWYs[idx]=='27':
                        temp_planned_rwy1=temp_planned_rwy1+1
                        #temp_planned_CBAS_27=temp_planned_CBAS_27+1
                    elif RWYs[idx]=='18C':
                        temp_planned_rwy2=temp_planned_rwy2+1
                        #temp_planned_CBAS_18C=temp_planned_CBAS_18C+1
					
                    #if IAFs[idx]=='ARTIP':
                    #    temp_planned_CBAS_ARTIP=temp_planned_CBAS_ARTIP+1
                    #elif IAFs[idx]=='RIVER':
                    #    temp_planned_CBAS_RIVER=temp_planned_CBAS_RIVER+1
                    #elif IAFs[idx]=='SUGOL':
					#	temp_planned_CBAS_SUGOL=temp_planned_CBAS_SUGOL+1
                              
                if LOG_times_at_RWY[idx] >=acceptedrange_low and LOG_times_at_RWY[idx] <=acceptedrange_high:
                        temp_actual_landed=temp_actual_landed+1
                        
                if LOG_lowlevel_delabs_simtimes[idx] >=acceptedrange_low and LOG_lowlevel_delabs_simtimes[idx] <=acceptedrange_high:
                    temp_interval_lowlev_delay.append(LOG_lowlevel_delabs_times[idx])
				
                if (PreDepEstTimes_at_CBAS[idx]-simulation_start) >=acceptedrange_low and (PreDepEstTimes_at_CBAS[idx]-simulation_start) <=acceptedrange_high:
                    if RWYs[idx]=='27':
                        temp_planned_CBAS_27=temp_planned_CBAS_27+1
                    elif RWYs[idx]=='18C':
                        temp_planned_CBAS_18C=temp_planned_CBAS_18C+1
					
                    if IAFs[idx]=='ARTIP':
                        temp_planned_CBAS_ARTIP=temp_planned_CBAS_ARTIP+1
                    elif IAFs[idx]=='RIVER':
                        temp_planned_CBAS_RIVER=temp_planned_CBAS_RIVER+1
                    elif IAFs[idx]=='SUGOL':
						temp_planned_CBAS_SUGOL=temp_planned_CBAS_SUGOL+1
					
                    temp_planned_CBAS_all = temp_planned_CBAS_all+1
				
                if LOG_CBAS_passed[idx] >=acceptedrange_low and LOG_CBAS_passed[idx] <=acceptedrange_high:
                    if RWYs[idx]=='27':
                        temp_actual_CBAS_27=temp_actual_CBAS_27+1
                    elif RWYs[idx]=='18C':
                        temp_actual_CBAS_18C=temp_actual_CBAS_18C+1
					
                    if IAFs[idx]=='ARTIP':
                        temp_actual_CBAS_ARTIP=temp_actual_CBAS_ARTIP+1
                    elif IAFs[idx]=='RIVER':
                        temp_actual_CBAS_RIVER=temp_actual_CBAS_RIVER+1
                    elif IAFs[idx]=='SUGOL':
						temp_actual_CBAS_SUGOL=temp_actual_CBAS_SUGOL+1
					
                    temp_actual_CBAS_all = temp_actual_CBAS_all+1
             
            for idx in range(len(sorted_runway1_lastSTAs)): 
                if sorted_runway1_lastSTAs[idx] >=acceptedrange_low and sorted_runway1_lastSTAs[idx] <=acceptedrange_high:
                        temp_actual_landed_runway1=temp_actual_landed_runway1+1
                        
            for idx in range(len(sorted_runway2_lastSTAs)): 
                if sorted_runway2_lastSTAs[idx] >=acceptedrange_low and sorted_runway2_lastSTAs[idx] <=acceptedrange_high:
                        temp_actual_landed_runway2=temp_actual_landed_runway2+1
                        
            #Now store these values in array
            counterpopup.append(temppopup)
            counterother.append(tempother)
            countertotal.append(temptotal)
            
            counter_planned_rwy1.append(temp_planned_rwy1)
            counter_planned_rwy2.append(temp_planned_rwy2)            
            
            counter_actual_landed.append(temp_actual_landed)
            counter_actual_runway1.append(temp_actual_landed_runway1)
            counter_actual_runway2.append(temp_actual_landed_runway2)
			
            counter_actual_CBAS_all.append(temp_actual_CBAS_all)
            counter_actual_CBAS_18C.append(temp_actual_CBAS_18C)
            counter_actual_CBAS_27.append(temp_actual_CBAS_27)
            counter_actual_CBAS_ARTIP.append(temp_actual_CBAS_ARTIP)
            counter_actual_CBAS_RIVER.append(temp_actual_CBAS_RIVER)
            counter_actual_CBAS_SUGOL.append(temp_actual_CBAS_SUGOL)
			
            counter_planned_CBAS_all.append(temp_planned_CBAS_all)
            counter_planned_CBAS_18C.append(temp_planned_CBAS_18C)
            counter_planned_CBAS_27.append(temp_planned_CBAS_27)
            counter_planned_CBAS_ARTIP.append(temp_planned_CBAS_ARTIP)
            counter_planned_CBAS_RIVER.append(temp_planned_CBAS_RIVER)
            counter_planned_CBAS_SUGOL.append(temp_planned_CBAS_SUGOL)
            
            if len(temp_interval_lowlev_delay)>0:
                average_lowlev_delay_interval.append(np.mean(temp_interval_lowlev_delay))
            else:
                average_lowlev_delay_interval.append(0)
             
            if temptotal>0:
                ratiopopup.append(float(temppopup)/float(temptotal)*100)
            elif temptotal==0:
                ratiopopup.append(0.)
            
            del temppopup,tempother,temptotal
        
        #print counterpopup,counterother,countertotal
        
        plt.figure()
        #plt.plot(intervalvalue,counterpopup,"r*--",markeredgecolor='r',label="Pop-up")
        #
        plt.plot(intervalvalue,counter_planned_CBAS_all,"x--",label="Pre-Departure CBAS All")
        plt.plot(intervalvalue,counter_actual_CBAS_all,"r*-",markeredgecolor='r',label="Actual CBAS All")
        plt.grid(True)
        plt.legend(loc="upper right")
        plt.xlabel("Simulation Time [s]",fontsize=16)
        plt.ylabel("Number of Flights [-]",fontsize=16)
        plt.tick_params(axis='x',labelsize=16)
        plt.tick_params(axis='y',labelsize=16)
        plt.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/CBAS_All.png')
		
        plt.figure()
        #plt.plot(intervalvalue,counterpopup,"r*--",markeredgecolor='r',label="Pop-up")
        #
        plt.plot(intervalvalue,counter_planned_CBAS_18C,"x--",label="Pre-Departure CBAS 18C")
        plt.plot(intervalvalue,counter_actual_CBAS_18C,"r*-",markeredgecolor='r',label="Actual CBAS 18C")
        plt.grid(True)
        plt.legend(loc="upper right")
        plt.xlabel("Simulation Time [s]",fontsize=16)
        plt.ylabel("Number of Flights [-]",fontsize=16)
        plt.tick_params(axis='x',labelsize=16)
        plt.tick_params(axis='y',labelsize=16)
        plt.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/CBAS_18C.png')
		
        plt.figure()
        #plt.plot(intervalvalue,counterpopup,"r*--",markeredgecolor='r',label="Pop-up")
        #
        plt.plot(intervalvalue,counter_planned_CBAS_27,"x--",label="Pre-Departure CBAS 27")
        plt.plot(intervalvalue,counter_actual_CBAS_27,"r*-",markeredgecolor='r',label="Actual CBAS 27")
        plt.grid(True)
        plt.legend(loc="upper right")
        plt.xlabel("Simulation Time [s]",fontsize=16)
        plt.ylabel("Number of Flights [-]",fontsize=16)
        plt.tick_params(axis='x',labelsize=16)
        plt.tick_params(axis='y',labelsize=16)
        plt.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/CBAS_27.png')
		
        plt.figure()
        #plt.plot(intervalvalue,counterpopup,"r*--",markeredgecolor='r',label="Pop-up")
        #
        plt.plot(intervalvalue,counter_planned_CBAS_ARTIP,"x--",label="Pre-Departure CBAS ARTIP")
        plt.plot(intervalvalue,counter_actual_CBAS_ARTIP,"r*-",markeredgecolor='r',label="Actual CBAS ARTIP")
        plt.grid(True)
        plt.legend(loc="upper right")
        plt.xlabel("Simulation Time [s]",fontsize=16)
        plt.ylabel("Number of Flights [-]",fontsize=16)
        plt.tick_params(axis='x',labelsize=16)
        plt.tick_params(axis='y',labelsize=16)
        plt.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/CBAS_ARTIP.png')
		
        plt.figure()
        #plt.plot(intervalvalue,counterpopup,"r*--",markeredgecolor='r',label="Pop-up")
        #
        plt.plot(intervalvalue,counter_planned_CBAS_RIVER,"x--",label="Pre-Departure CBAS RIVER")
        plt.plot(intervalvalue,counter_actual_CBAS_RIVER,"r*-",markeredgecolor='r',label="Actual CBAS RIVER")
        plt.grid(True)
        plt.legend(loc="upper right")
        plt.xlabel("Simulation Time [s]",fontsize=16)
        plt.ylabel("Number of Flights [-]",fontsize=16)
        plt.tick_params(axis='x',labelsize=16)
        plt.tick_params(axis='y',labelsize=16)
        plt.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/CBAS_RIVER.png')
		
        plt.figure()
        #plt.plot(intervalvalue,counterpopup,"r*--",markeredgecolor='r',label="Pop-up")
        #
        plt.plot(intervalvalue,counter_planned_CBAS_SUGOL,"x--",label="Pre-Departure CBAS SUGOL")
        plt.plot(intervalvalue,counter_actual_CBAS_SUGOL,"r*-",markeredgecolor='r',label="Actual CBAS SUGOL")
        plt.grid(True)
        plt.legend(loc="upper right")
        plt.xlabel("Simulation Time [s]",fontsize=16)
        plt.ylabel("Number of Flights [-]",fontsize=16)
        plt.tick_params(axis='x',labelsize=16)
        plt.tick_params(axis='y',labelsize=16)
        plt.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/CBAS_SUGOL.png')
		
        plt.figure()
        plt.plot(intervalvalue,counterpopup,"r*--",markeredgecolor='r',label="Pop-up")
        plt.plot(intervalvalue,counterother,"g*--",markeredgecolor='g',label="Normal")
        plt.plot(intervalvalue,countertotal,"x-",label="Total")
        plt.grid(True)
        plt.legend(loc="upper right")
        plt.xlabel("Simulation Time [s]",fontsize=16)
        plt.ylabel("Number of Flights [-]",fontsize=16)
        plt.tick_params(axis='x',labelsize=16)
        plt.tick_params(axis='y',labelsize=16)
        plt.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/Total_Flights_Labels.png')




        plt.figure()
        #plt.plot(intervalvalue,counterpopup,"r*--",markeredgecolor='r',label="Pop-up")
        #
        plt.plot(intervalvalue,counter_planned_rwy1,"x--",label="Pre-Departure - 27")
        plt.plot(intervalvalue,counter_actual_runway1,"r*-",markeredgecolor='r',label="Actual - 27")
        plt.grid(True)
        plt.legend(loc="upper right")
        plt.xlabel("Simulation Time [s]",fontsize=16)
        plt.ylabel("Number of Flights [-]",fontsize=16)
        plt.tick_params(axis='x',labelsize=16)
        plt.tick_params(axis='y',labelsize=16)
        plt.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/Flights_27')
        

        plt.figure()
        #plt.plot(intervalvalue,counterpopup,"r*--",markeredgecolor='r',label="Pop-up")
        #
        plt.plot(intervalvalue,counter_planned_rwy2,"x--",label="Pre-Departure - 18C")
        plt.plot(intervalvalue,counter_actual_runway2,"r*-",markeredgecolor='r',label="Actual - 18C")
        plt.grid(True)
        plt.legend(loc="upper right")
        plt.xlabel("Simulation Time [s]",fontsize=16)
        plt.ylabel("Number of Flights [-]",fontsize=16)
        plt.tick_params(axis='x',labelsize=16)
        plt.tick_params(axis='y',labelsize=16)
        plt.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/Flights_18C.png')

        plt.figure()
        #plt.plot(intervalvalue,counterpopup,"r*--",markeredgecolor='r',label="Pop-up")
        #
        plt.plot(intervalvalue,countertotal,"x-",label="Pre-Departure")
        plt.plot(intervalvalue,counter_actual_landed,"k*--",markeredgecolor='k',label="Actual - Total")
        plt.plot(intervalvalue,counter_actual_runway1,"g*--",markeredgecolor='g',label="Actual - 27")
        plt.plot(intervalvalue,counter_actual_runway2,"r*--",markeredgecolor='r',label="Actual - 18C")
        plt.grid(True)
        plt.legend(loc="upper right")
        plt.xlabel("Simulation Time [s]",fontsize=16)
        plt.ylabel("Number of Flights [-]",fontsize=16)
        plt.tick_params(axis='x',labelsize=16)
        plt.tick_params(axis='y',labelsize=16)
        plt.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/Total_Flights_Runways.png')




        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.plot(intervalvalue,average_lowlev_delay_interval,"rx--",markeredgecolor='r',label="Delay")
        
        ax2=ax.twinx()
        ax2.plot(intervalvalue,counter_actual_landed,"b*--",markeredgecolor='b',label="Actual - Total")
        ax2.plot(intervalvalue,countertotal,"gh--",markeredgecolor='g',label="Pre-Departure - Total")
        ax2.legend()
        
        ax.set_xlabel("Simulation Time [s]",fontsize=16)
        ax2.set_ylabel("Number of Flights [-]",fontsize=16)
        
        ax.set_ylabel("Average Low-Level Delay [s]",fontsize=16)
       
        #plt.plot(intervalvalue,counter_actual_landed,"k*--",markeredgecolor='k',label="Actual - Total")
        #plt.plot(intervalvalue,counter_actual_runway1,"g*--",markeredgecolor='g',label="Actual - 27")
        #plt.plot(intervalvalue,counter_actual_runway2,"r*--",markeredgecolor='r',label="Actual - 18C")
        ax2.yaxis.label.set_color('k')
        ax2.tick_params(axis='y',colors='k')
        ax.yaxis.label.set_color('r')
        ax.tick_params(axis='y',colors='r')
        
        ax.tick_params(axis='x',labelsize=16)
        ax2.tick_params(axis='y',labelsize=16)
        ax.tick_params(axis='y',labelsize=16)
        
        ax.axis(fontsize=16)
        ax2.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/Total_Delay.png')




        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.plot(intervalvalue,ratiopopup,"rh-.",markeredgecolor='r',label="Pop-up")
        
        ax2=ax.twinx()
        ax2.plot(intervalvalue,countertotal,"x-",label="Total")
        ax2.plot(intervalvalue,counterpopup,"*b--",markeredgecolor='b',label="Pop-up")
        ax2.legend()
                
        ax.set_xlabel("Simulation Time [s]",fontsize=16)
        ax2.set_ylabel("Number of Flights [-]",fontsize=16)
        
        ax.set_ylabel("Ratio of Pop-Up Flights [%]",fontsize=16)
        
        ax2.yaxis.label.set_color('b')
        ax2.tick_params(axis='y',colors='b')
        ax.yaxis.label.set_color('r')
        ax.tick_params(axis='y',colors='r')
        
        ax.tick_params(axis='x',labelsize=16)
        ax2.tick_params(axis='y',labelsize=16)
        ax.tick_params(axis='y',labelsize=16)
        
        ax.axis(fontsize=16)
        ax2.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/Popup_Flights.png')
        
        
        horizon_values=range(0,501,1)
        ratios=[]
        
        for horizon_value in horizon_values:
            temp=sum(distance<horizon_value for distance in Direct_inbetween_dists)
            ratios.append(float(temp)/float(len(CallSigns))*100.)
            del temp
        
        plt.figure()
        plt.plot(horizon_values,ratios,"r*--",markeredgecolor='r')
        plt.grid(True)
        plt.xlabel("AMAN Horizon [nm]",fontsize=16)
        plt.ylabel("Pop-Up Ratio [%]",fontsize=16)
        plt.tick_params(axis='x',labelsize=16)
        plt.tick_params(axis='y',labelsize=16)
        plt.axis(fontsize=16)
        plt.show()
        #plt.savefig('figures/Popup_Ratio.png')
        


####
simulation_start=min(SimTimes)
if show_graphs_sw:
    import matplotlib.pyplot as plt 
    show_graphs(CallSigns,PreDepEstTimes_at_RWY,PopupLabels,Direct_inbetween_dists,simulation_start,sorted_runway1_lastSTAs,sorted_runway2_lastSTAs,LOG_times_at_RWY,LOG_lowlevel_delabs_times,LOG_lowlevel_delabs_simtimes)