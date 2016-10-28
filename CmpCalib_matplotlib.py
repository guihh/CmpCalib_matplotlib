#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import numpy as np
import re
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
from scipy.interpolate import griddata
from collections import OrderedDict 


class Calibration:
	
 def __init__(self):
 		
      self.path = ''
      self.e_radiaux=[]
      self.e_plani=[]
      self.e_plani_max=0
      self.random_color = np.asarray( np.random.rand(3) )
      return
 
 def load(self):	
     file=open(self.path,'r')		
     for row in file :
         if re.match('\s\d', row) :
            self.e_radiaux.append(map(float,row.split()))
         elif re.match('\d', row):
             self.e_plani.append(map(float,row.split()))	
     return
           
 def set_path(self,path):
     self.path=path
     return
 
 def set_e_plani_max(self):
       self.e_plani_max = np.max(np.asarray(self.e_plani)[:,4])
       return
			

class Comparaison:
	
      def __init__(self):
      		
           self.path_calibs = []
           self.calibrations = OrderedDict()
           
           self.max_all_e_plani=[]
           self.max_scale= 1.0
           self.is_max_scale_defined=False
           self.linewidth = 1.75
           self.fontsize = 17
           self.nbclass=50
           self.scale_output=1.0
           self.plot = plt.figure(1)
           self.plot.set_size_inches(20,15)
           self.ratio = 0.2 
           self.dir_output='' 
           self.interpolation = 'linear'
           self.width_arrows = 0.003
      
           return
      
	  #Instances all Calibs
      def load(self):
      	for path_calib in self.path_calibs:
      		self.calibrations[path_calib] = Calibration() #Instance
      		self.calibrations[path_calib].set_path(path_calib) # set path 
      		self.calibrations[path_calib].load() # parse txt file
      		self.calibrations[path_calib].set_e_plani_max() # store the max euclidian dist  
      		self.max_all_e_plani.append(self.calibrations[path_calib].e_plani_max) # store in Comparaison object the maximum objet between all file to plot to share same scale
      		
      	return
      	
      def get_args(self):
          
           try:
               parser = argparse.ArgumentParser()
           except:
               parser.print_help()
               sys.exit(0)

           parser.add_argument( 'Calibrations' , help = 'Absolute path of calibration file(s).' , type = str , nargs = '+' )
           parser.add_argument( '-o' , '--output' , help = 'Absolute path to save' , type = str , action = "store", dest = 'output')
           parser.add_argument( '-m' , '--max_scale' , help = 'Maximum deviation value to plot. Default is maximum deviation from input file(s).' , type = float , action = "store", dest = 'max_scale')
           parser.add_argument( '-c' , '--nbclass' , help = 'Number of classes for the LUT. Default is 50.' , type = int , action = "store", dest = 'nbclass')
           parser.add_argument( '-f' , '--fontsize' , help = 'Fontsize. Default is 17.' , type = int , action = "store", dest = 'fontsize')
           parser.add_argument( '-l' , '--linewidth' , help = 'Width of the line to plot. Default is 1.75.' , type = float , action = "store", dest = 'linewidth')
           parser.add_argument( '-r' , '--ratio' , help = 'Padding  in each "Ecarts Planimetriques" frame (%% of maximum value X & Y). Useful to displayed whole plotted arrows. Default is 0.2.' , type = float , action = "store", dest = 'ratio')
           parser.add_argument( '-sc' , '--scale_output' , help = 'coefficient to choose scale of image output.' , type = float , action = "store", dest = 'scale_output')
           parser.add_argument( '-i' , '--interpolation_mode' , help = 'Choose between: {‘linear’, ‘nearest’, ‘cubic’}. Default is ''linear'' ', type = str , action = "store", dest = 'interpolation_mode')
           parser.add_argument( '-w' , '--width_arrows' , help = 'Width of the arrows. Default is 0.03', type = float , action = "store", dest = 'width_arrows')
           args = parser.parse_args()
           
           self.path_calibs = args.Calibrations
           self.dir_output = os.path.join(os.path.dirname(self.path_calibs[0]),'CmpCalib_plot.png')
           
           if args.ratio is not None:
              self.ratio = args.ratio 
           if args.output is not None:
              self.dir_output = args.output
           if args.max_scale is not None:
              self.is_max_scale_defined=True
              self.max_scale = args.max_scale 
           if args.nbclass is not None:
              self.nbclass = args.nbclass
           if args.fontsize is not None:
              self.fontsize = args.fontsize
           if args.linewidth is not None:
              self.linewidth = args.linewidth
           if args.scale_output is not None:
              self.scale_output = args.scale_output
           if args.interpolation_mode is not None:
              self.interpolation = args.interpolation_mode 
           if args.width_arrows is not None:
              self.width_arrows = args.width_arrows         
           
           return
      
      def initialize_plot(self):
		  
           plt.clf() # clear
           plt.ion()
           #~ plt.show() #keep open
           
           return

      			 
      def plot_e_radiaux_plani(self):
		
        gs = gridspec.GridSpec(7, 7)
		 
        for i,calibration in enumerate(self.calibrations.keys()): 
              #### plot ecart radiaux #### 				    
				#~ ax = plt.subplot2grid((4, 4), (0,0),colspan=4,rowspan=1)              
              ax = plt.subplot(gs[0:2, 0:7])
              ax.plot(np.asarray(self.calibrations[calibration].e_radiaux)[:,0],np.asarray(self.calibrations[calibration].e_radiaux)[:,1],c=self.calibrations[calibration].random_color,label=os.path.basename(calibration),linewidth = self.linewidth) # plot ecart radiaux data
              ax.tick_params( axis = 'both' , labelsize = self.fontsize-3)	
              ax.set_xlabel('Rayon (px)', horizontalalignment = 'center').set_fontsize(self.fontsize)
              ax.set_ylabel( 'Ecarts radiaux (px)' ).set_fontsize(self.fontsize)
              ax.legend(loc = 'upper left', prop = {'size': self.fontsize} )
              
              ax.spines['top'].set_visible(False)
              
              #~ ax.yaxis.set_ticks_position('left','right')
              ax.xaxis.set_ticks_position('bottom')
              
			  #### plot ecart plani ####
              	
              if len(self.calibrations)==1:
                ax1 = plt.subplot(gs[3:7, 1:6])
                ax1.set_title(os.path.basename(calibration),fontsize=self.fontsize+4,fontweight='bold',color=self.calibrations[calibration].random_color,position=(0.5, 1-(self.ratio/5))) #if 1 file
                
                            
              elif len(self.calibrations)==2:
                ax1 = self.plot.add_subplot(2,2,(i+1+2))
                ax1.set_title(os.path.basename(calibration),fontsize=self.fontsize,fontweight='bold',color=self.calibrations[calibration].random_color,position=(0.5, 0.95-(self.ratio/2.8))) #if 2 files
              else:	
                ax1 = self.plot.add_subplot(3,3,(i+len(self.calibrations)))
                ax1.set_title(os.path.basename(calibration),fontsize=self.fontsize,color=self.calibrations[calibration].random_color,position=(0.5, 0.95-(self.ratio/3))) #if n files
				
                            

              
              ax1.spines['top'].set_visible(False)
              ax1.spines['right'].set_visible(False)
              ax1.spines['left'].set_visible(False)
              ax1.spines['bottom'].set_visible(False)
              
              ax1.set_xticks([min(np.asarray(self.calibrations[calibration].e_plani)[:,0]),max(np.asarray(self.calibrations[calibration].e_plani)[:,0])/2,max(np.asarray(self.calibrations[calibration].e_plani)[:,0])])
              ax1.set_yticks([min(np.asarray(self.calibrations[calibration].e_plani)[:,1]),max(np.asarray(self.calibrations[calibration].e_plani)[:,1])/2,max(np.asarray(self.calibrations[calibration].e_plani)[:,1])])

              if i==0:
                  ax1.set_ylabel('Ecarts Planimetriques (px)').set_fontsize(self.fontsize)
                  ax1.tick_params( axis = 'both' , labelsize = self.fontsize-3)	
                  ax1.set_xlabel('Rayon (px)', horizontalalignment = 'center').set_fontsize(self.fontsize)
              
              xi = np.linspace(np.min(np.asarray(self.calibrations[calibration].e_plani)[:,0])-np.max(np.asarray(self.calibrations[calibration].e_plani)[:,0])*(self.ratio), np.max(np.asarray(self.calibrations[calibration].e_plani)[:,0])*(1+self.ratio),400)
              yi = np.linspace(np.min(np.asarray(self.calibrations[calibration].e_plani)[:,1])-np.max(np.asarray(self.calibrations[calibration].e_plani)[:,1])*(self.ratio), np.max(np.asarray(self.calibrations[calibration].e_plani)[:,1])*(1+self.ratio),400)
             
              
              points = np.vstack((np.asarray(self.calibrations[calibration].e_plani)[:,0],np.asarray(self.calibrations[calibration].e_plani)[:,1])).T
              values = np.asarray(self.calibrations[calibration].e_plani)[:,4]
                   		   
              zi = griddata(points,values,(xi[None,:], yi[:,None]), method=self.interpolation)
              m = cm.ScalarMappable(cmap=cm.viridis_r)
              
              
              
              
              if not self.is_max_scale_defined:
                  v = np.linspace(0, np.max(self.max_all_e_plani),self.nbclass,endpoint=True)
              else:
                  v = np.linspace(0, self.max_scale,self.nbclass,endpoint=True)
              m.set_array(v)
              
              CS = plt.contourf(xi,yi,zi,v,cmap=m.get_cmap())
              

              ax1.quiver(np.asarray(self.calibrations[calibration].e_plani)[:,0],np.asarray(self.calibrations[calibration].e_plani)[:,1],np.asarray(self.calibrations[calibration].e_plani)[:,2],np.asarray(self.calibrations[calibration].e_plani)[:,3],width=self.width_arrows)
                  
              plt.axis('equal')
              plt.draw()

              if i == (len(self.calibrations)-1):
                  cbar_ax = self.plot.add_axes([0.95, 0.15, 0.01, 0.7])
                  self.plot.colorbar(m,cax=cbar_ax)
                  plt.subplots_adjust(wspace=0.1, hspace=0)
                  #~ self.plot.set_size_inches( int(round(20*self.scale_output)) , int(round(15*self.scale_output)) )
                  self.plot.savefig(self.dir_output,dpi=90)
        
if __name__ == '__main__':
    comparaison=Comparaison()
    comparaison.get_args()
    print('--- parsing file(s) ---')
    comparaison.load()
    comparaison.initialize_plot()
    print('--- plotting ---')
    comparaison.plot_e_radiaux_plani()
    print('--- Saved to : '+comparaison.dir_output )
    
    
    
    
