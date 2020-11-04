# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:39:42 2020

@author: Ryan Kari
@email: ryan.j.kari@gmail.com

"""

import tkinter as tk
from tkinter import Tk, Listbox,ttk,Button
import numpy as np



        
class TorqueStressGUI:
    """
    This is a self contained GUI that converted shaft outer diameter (OD) in mm,
    inner diameter (ID) in mm, and an applied torque T, into stress. 
    
    A table is also created that displays the torque required to apply: 
        100MPa, 200MPa, 300MPa, 400MPa, and 500MPa
    
    The entry boxes are in a callback, such that the values are updated 
    immediately
    """
    global default_trq_value,default_id_value,default_od_value
    default_trq_value = 1000
    default_id_value = 12
    default_od_value = 22
    def __init__(self, master):
        self.master = master
        master.title("Torque to Stress V1")

#Define frames and grid locations
#          
###        |---frame1---|---frame5---|-6-!----------frame7-----------|
###        |---frame1---|------------|---!---------------------------|      
###        |---frame1---|------------|---!---------------------------|
###        |---frame4---|------------|---!---------------------------|
###        |------------|------------|---!---------------------------|
###        |------------|------------|---!---------------------------|

        
        frame1width = 110
        frame5width = 100
        frame6width = 40
        frame7width = 500
        frame1height = 150
        frame2height = 100

        frame1 = tk.Frame(master,width=frame1width,height=frame1height)
        frame5 = tk.Frame(master,width=frame5width,height=frame1height)
        frame6 = tk.Frame(master,width=frame6width)
        frame7 = tk.Frame(master,width = frame7width)

        frame1.grid(row=0, column=0,padx = 5,sticky=tk.N)
        
        frame5.grid(row=0,column=1,rowspan=1,stick=tk.N)
        frame6.grid(row=0,column=2,rowspan=1,stick=tk.N)
        frame7.grid(row=0,column=3,rowspan=1,stick=tk.E)    
        
        self.ShaftOD = tk.DoubleVar(master,value=default_od_value)
        labelText6=tk.StringVar()
        labelText6.set("Shaft OD (mm)")
        tk.Label(frame1, textvariable=labelText6,font=12).grid(row=0, 
                                                               column=0,sticky=tk.W,padx=5)
        
        ttk.Entry(frame1,  textvariable=self.ShaftOD,width=12, font = 12).grid(row=1,column=0,sticky=tk.W)
        
        self.ShaftOD.trace_add("write", self.compute_function)
        
        self.ShaftID = tk.DoubleVar(master,value=default_id_value)
        labelText6=tk.StringVar()
        labelText6.set("Shaft ID (mm)")     
        tk.Label(frame1, textvariable=labelText6,font=12).grid(row=2, column=0,sticky=tk.W)
        ttk.Entry(frame1,  textvariable=self.ShaftID,width=12, font = 12).grid(row=3,column=0,sticky=tk.W)
        self.ShaftID.trace_add("write", self.compute_function)   
        
        self.Torque = tk.DoubleVar(master,value=default_trq_value)
        labelText6=tk.StringVar()
        self.Torque.trace_add("write", self.compute_function)
        
        labelText6.set("Torque (Nm)")     
        tk.Label(frame1, textvariable=labelText6,font=12).grid(row=4, column=0,sticky=tk.W,padx=1)
        ttk.Entry(frame1,  textvariable=self.Torque,width=12, font = 12).grid(row=5,column=0,sticky=tk.W)       

        self.Stress = tk.DoubleVar(master,value=default_trq_value)
        labelText6=tk.StringVar()
        labelText6.set("Stress (MPa)")     
        tk.Label(frame5, textvariable=labelText6,font=12).grid(row=2, column=1,sticky=tk.W)
        ttk.Entry(frame5,  textvariable=self.Stress,width=12, font = 12).grid(row=3,column=1,sticky=tk.W)      
        
        self.ExecuteButton =    Button(frame1, text="Compute", height = 3,
                                       width=12,padx = 5,command=self.compute_function,
                                       compound=tk.LEFT)
        
        self.ExecuteButton.grid(row=6, column=0, sticky=tk.W+tk.S,pady=20)
        
        TableLabel = tk.StringVar()
        TableLabel.set('Table')
        tk.Label(frame7, textvariable=TableLabel,font=12).grid(row=0, column=0,sticky=tk.E)
        
        self.List1 = Listbox(frame7,width=20,height=15,font=('times',12),selectmode='single')
        self.List1.grid(row=1,column=0,rowspan=1,columnspan = 2,sticky=tk.E)
    
        self.compute_function()

    """  This function does the computation and updates the table. This is called 
    via the Compute button and callbacks associated with the entry boxes   """
    def compute_function(self,*args):
        try:
            Torque = self.Torque.get()
            ID = self.ShaftID.get()/1000
            OD = self.ShaftOD.get()/1000
        except:
            Torque = 0
            OD = default_od_value
            ID = default_id_value
        
        stress = np.round( Torque * 16/np.pi*OD / (OD**4-ID**4)/10**6  ,1)   
        
        self.Stress.set( stress )
        self.List1.delete(0,'end')
        
        # Create linear spaced data from 1Nm to 150,0000Nm
        torque_array = np.linspace(1,150000,100)
        
        # Compute the stress at each torque
        stress_array = torque_array*16/np.pi*OD/(OD**4-ID**4)/10**6
        
        #Define lookup points to find stress
        lookup_pts = [50,100,200,300,400,500] 
        
        #Interpolate to find torque and stresses of interest
        lookup_output  = np.round(np.interp(lookup_pts,stress_array,torque_array))
        
        #Update the table
        for index,item in enumerate(lookup_output):
            stress_stress = f"{str(item)} Nm     {str(lookup_pts[index])} MPa"
            self.List1.insert(tk.END,stress_stress)
        root.update()

""" Execute the following to create and run the class when the file is executed  """
root = Tk()
w, h = root.winfo_screenwidth()*.25, root.winfo_screenheight()*.35
root.geometry("%dx%d+0+0" % (w, h))

my_gui = TorqueStressGUI(root)

root.mainloop()
