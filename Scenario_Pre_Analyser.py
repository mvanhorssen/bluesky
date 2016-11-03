#Scenario_Pre_Analyser.py

import pickle
import sys

def scenario_print():
    for k in range(1000):
        print 1
    
def save_to_file(sim):
    
    if len(sys.argv)>1:
        fnametempor=str(sys.argv[1])
    else:
        fnametempor='test_sample'    
           
    with open(fnametempor+'.pkl','wb') as output:
        pickle.dump(sys.argv,output,-1)
        pickle.dump(sim.traf.AMAN.AllFlights.CallSign,output,-1)
        pickle.dump(sim.traf.AMAN.AllFlights.PreDepEstTime_at_RWY,output,-1)
        pickle.dump(sim.traf.AMAN.AllFlights.PopupLabel,output,-1)
        pickle.dump(sim.traf.AMAN.AllFlights.Direct_inbetween_dist,output,-1)
        pickle.dump(sim.traf.AMAN.AllFlights.SimTime,output,-1)
        pickle.dump(sim.traf.AMAN.AllFlights.Origin,output,-1)

        pickle.dump(sim.traf.AMAN.whichIAFs,output,-1)
        pickle.dump(sim.traf.AMAN.whichRWYs,output,-1)

        pickle.dump(sim.traf.AMAN.AllFlights.Total_flightplan_dist,output,-1)
        pickle.dump(sim.traf.AMAN.AllFlights.PreDepEstTime_at_IAF,output,-1)
    
        pickle.dump(sim.traf.AMAN.LOG_time_at_IAF,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_time_at_RWY,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_accuracy_predepest_at_IAF,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_accuracy_predepest_at_RWY,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_IAF_passed,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_RWY_passed,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_delivery_accuracy_at_IAF,output,-1)
        
        pickle.dump(sim.traf.AMAN.LOG_schtimehist_schtime,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_schtimehist_disttorwy,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_schtimehist_flightphase,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_schtimehist_STAstatus,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_schtimehist_simtime,output,-1)        
        
        pickle.dump(sim.traf.AMAN.LOG_energycost,output,-1)
        
        pickle.dump(sim.traf.AMAN.LOG_lowlevel_delabs_time,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_lowlevel_delabs_dist,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_lowlevel_delabs_type,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_lowlevel_delabs_simtime,output,-1)
        
        pickle.dump(sim.traf.AMAN.LOG_seqhist_number,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_seqhist_disttorwy,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_seqhist_flightphase,output,-1)
        pickle.dump(sim.traf.AMAN.LOG_seqhist_STAstatus,output,-1)
 
    del fnametempor
    
#import matplotlib.pyplot as plt 
#
#def show_graphs(self,simulation_start):
#        #Determine, for each time interval (d) during the whole day the number of landing aircraft, whether they are pop-up and the pop-up ratio
#        
#        #initialisation
#        counterpopup=[]
#        counterother=[]
#        countertotal=[]
#        intervalvalue=[]
#        
#        ratiopopup=[]
#        #
#        
#        d=30*60 #width interval used throughout simulations
#        
#        for j in range(0+d,int(max(self.AllFlights.PreDepEstTime_at_RWY)-simulation_start+1),15*60): 
#            #initialisation
#            temppopup=0
#            tempother=0
#            temptotal=0
#            #
#        
#            intervalvalue.append(float(j))
#        
#            acceptedrange_low=j-d #Specify lower boundary for interval
#            acceptedrange_high=j #Specify upper boundary for interval
#        
#            for idx in range(len(self.AllFlights.CallSign)): #for each flight
#        
#                if (self.AllFlights.PreDepEstTime_at_RWY[idx]-simulation_start) >=acceptedrange_low and (self.AllFlights.PreDepEstTime_at_RWY[idx]-simulation_start) <=acceptedrange_high: #Check if flight within time range
#                    temptotal=temptotal+1
#        
#                    if self.AllFlights.PopupLabel[idx]=='POPUP': #Check if flight pop-up flight
#                        temppopup=temppopup+1 #Add +1 to number of pop-up flights in range
#                        
#        
#                    elif self.AllFlights.PopupLabel[idx]=='NORMAL': #If no pop-up flight
#                        tempother=tempother+1 #Add +1 to number of other flights in range
#        
#        
#            #Now store these values in array
#            counterpopup.append(temppopup)
#            counterother.append(tempother)
#            countertotal.append(temptotal)
#            if temptotal>0:
#                ratiopopup.append(float(temppopup)/float(temptotal)*100)
#            elif temptotal==0:
#                ratiopopup.append(0.)
#            
#            del temppopup,tempother,temptotal
#        
#        #print counterpopup,counterother,countertotal
#        
#        plt.figure()
#        plt.plot(intervalvalue,counterpopup,"r*--",markeredgecolor='r',label="Pop-up")
#        plt.plot(intervalvalue,counterother,"g*--",markeredgecolor='g',label="Normal")
#        plt.plot(intervalvalue,countertotal,"x-",label="Total")
#        plt.grid(True)
#        plt.legend(loc="upper right")
#        plt.xlabel("Simulation Time [s]",fontsize=16)
#        plt.ylabel("Number of Flights [-]",fontsize=16)
#        plt.tick_params(axis='x',labelsize=16)
#        plt.tick_params(axis='y',labelsize=16)
#        plt.axis(fontsize=16)
#        plt.show()
#
#
#        fig=plt.figure()
#        ax=fig.add_subplot(111)
#        ax.plot(intervalvalue,ratiopopup,"rh-.",markeredgecolor='r',label="Pop-up")
#        
#        ax2=ax.twinx()
#        ax2.plot(intervalvalue,countertotal,"x-",label="Total")
#        ax2.plot(intervalvalue,counterpopup,"*b--",markeredgecolor='b',label="Pop-up")
#        ax2.legend()
#                
#        ax.set_xlabel("Simulation Time [s]",fontsize=16)
#        ax2.set_ylabel("Number of Flights [-]",fontsize=16)
#        
#        ax.set_ylabel("Ratio of Pop-Up Flights [%]",fontsize=16)
#        
#        ax2.yaxis.label.set_color('b')
#        ax2.tick_params(axis='y',colors='b')
#        ax.yaxis.label.set_color('r')
#        ax.tick_params(axis='y',colors='r')
#        
#        ax.tick_params(axis='x',labelsize=16)
#        ax2.tick_params(axis='y',labelsize=16)
#        ax.tick_params(axis='y',labelsize=16)
#        
#        ax.axis(fontsize=16)
#        ax2.axis(fontsize=16)
#        plt.show()
#        
#        
#        horizon_values=range(0,501,1)
#        ratios=[]
#        
#        for horizon_value in horizon_values:
#            temp=sum(distance<horizon_value for distance in self.AllFlights.Direct_inbetween_dist)
#            ratios.append(float(temp)/float(len(self.AllFlights.CallSign))*100.)
#            del temp
#        
#        plt.figure()
#        plt.plot(horizon_values,ratios,"r*--",markeredgecolor='r')
#        plt.grid(True)
#        plt.xlabel("AMAN Horizon [nm]",fontsize=16)
#        plt.ylabel("Pop-Up Ratio [%]",fontsize=16)
#        plt.tick_params(axis='x',labelsize=16)
#        plt.tick_params(axis='y',labelsize=16)
#        plt.axis(fontsize=16)
#        plt.show()
#
#####
#simulation_start=min(sim.traf.AMAN.AllFlights.SimTime)
#show_graphs(sim.traf.AMAN,simulation_start)