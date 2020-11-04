# torque_to_stress

##### Summary
GUI that converts shaft OD and ID with applied torque into stress on the shaft. There is an additional table provided to view torque to apply various increments of stress. 

This GUI was created using Python with TKInter. Callbacks are used to re-run the computation based on applying new data into any of the Entry boxes provided. The output is shown in Stress. This function is intended to be used by executing a desktop shortcut,  in which the target is this file. 

For reference, the conversion from torque to stress is:

Stress [MPa] = 16*pi*OD/(OD^4-ID^4)/10^6, 
where OD is the outer diameter and ID is the inner diameter in meters. 

###### Sample image of GUI
![Sample image of GUI](https://github.com/ryankari/torque_to_stress/blob/main/Image_Of_torque_to_stress_GUI.PNG)

