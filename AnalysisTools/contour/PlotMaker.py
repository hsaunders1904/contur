#!usr/bin/env python

import os, sys
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib as mpl
import colormaps as cmaps
import pickle
import scipy.stats as sp
from os.path import join
import errno

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from PlotStyle import *
from contour import TestingFunctions as ctr
#from TesterFunctions import *

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def writeOutput(output, h):
    f = open(h, 'w')
    for item in output:
        f.write(str(item) + "\n")
    f.close()

##quick function to return the pertubative unitarity bound
#the 1.0 is gdm, currently hardcoded, grab from model file/ directory info eventually

def pertUnit(mz):
    return np.sqrt(np.pi/2) * (mz/1.0)

mkdir_p('plots')

for root, dirs, files in os.walk('.',topdown=False):
    maps = {}
    #for dirs
    for filename in files:
		#walk and look for .map files
        if '.map' in filename and 'svn' not in filename:
            filename = join(root,filename)
            with open(filename,'r+b') as f:
                maps[filename.strip(".map")] = pickle.load(f)

    if not maps:
        continue
    ##use longest member of map to make base map, just in case
    data = maps[max(maps, key=lambda x: len(maps[x]))][:]
    for i in range(0,len(data)):
        data[i]=list(data[i])
        data[i][2] = 1.0
        data[i][3] = []
        data[i][4] = []
        data[i][5] = []
        data[i][6] = []
    i=0
    for key in maps:
        i+=1
        for i in range(0,len(maps[key])):
            for j in range(0,len(data)):
                if maps[key][i][0] == data[j][0] and maps[key][i][1] == data[j][1]:
                    data[j][3].extend(maps[key][i][3])
                    data[j][4].extend(maps[key][i][4])
                    data[j][5].extend(maps[key][i][5])
                    data[j][6].extend(maps[key][i][6])

    for listelement in data:
        data[data.index(listelement)][2]= ctr.confLevel(listelement[3],listelement[4],listelement[5],listelement[6])


    temp = []
    temp =  zip(zip(*data)[0],zip(*data)[1],zip(*data)[2])
    temp.sort(key=lambda x: x[0])
    writeOutput(temp,"combinedCL_" + root.strip('./') + ".dat")


#find the grid spacings:

    dx= ( min(filter(lambda x: x> min(zip(*data)[1]), (zip(*data)[1]))) - min(zip(*data)[1]))/2.0
    dy= ( min(filter(lambda x: x> min(zip(*data)[0]), (zip(*data)[0]))) - min(zip(*data)[0]))/2.0

##build the contour grid, NOTE: different to the map grid
    contourXaxis=[]
    contourYaxis=[]
    x=min(zip(*data)[1])
    y=min(zip(*data)[0])
#lets make a second grid for contouring
#for x in range(0, min(zip(*data)[1]), dx*2):
    while x <= max(zip(*data)[1]):
        contourXaxis.append(x)
        x= x+ dx*2
    while y <= max(zip(*data)[0]):
        contourYaxis.append(y)
        y= y+ dy*2

#Build the map grid
#this could be redone intelligently I think...
    x_grid_min= min(zip(*data)[1])-dx
    y_grid_min= min(zip(*data)[0])-dy
    x_grid_max= max(zip(*data)[1])+dx
    y_grid_max= max(zip(*data)[0])+dy

    yy,xx =np.mgrid[y_grid_min:y_grid_max+dy:2*dy,x_grid_min:x_grid_max+dx:2*dx]
    c=np.zeros([len(xx[0,:])-1,len(yy[:,0])-1])


    for i in range(0,len(zip(*data)[1])):
        xcounter=0
        ycounter=0
        for xarg2 in xx[1]:
            if zip(*data)[1][i] > xarg2:
                xcounter+=1
        for yarg2 in yy[:,xcounter]:
            if zip(*data)[0][i] > yarg2:
                ycounter+=1
        c[xcounter-1][ycounter-1]=zip(*data)[2][i]


###Plotting functions
    fig=plt.figure(figsize=fig_dims)
    ax = fig.add_subplot(1,1,1)


##try and pick ticks intelligently

    my_locator_x = MaxNLocator((max(contourXaxis) / 500.0 ) + 1)
    my_locator_y = MaxNLocator((max(contourYaxis) / 500.0) + 1)
    minorLocator_x = MaxNLocator(len(contourXaxis) + 1)
    minorLocator_y = MaxNLocator(len(contourYaxis) + 1)
    ax.yaxis.set_major_locator(my_locator_y)
    ax.xaxis.set_major_locator(my_locator_x)
    ax.xaxis.set_minor_locator(minorLocator_x)
    ax.yaxis.set_minor_locator(minorLocator_y)
    del my_locator_x
    del my_locator_y
    del minorLocator_x
    del minorLocator_y

    plt.pcolormesh(xx,yy,c.T,cmap=cmaps.magma, vmin=0, vmax=1)
    plt.axis([x_grid_min, x_grid_max, y_grid_min, y_grid_max])

##axis labels
    plt.xlabel(r"$M_{DM}$ [GeV]")
    plt.ylabel(r"$M_{Z'}$ [GeV]")

##suppress title
#plt.title("ATLAS + CMS Combined all channels",y=1.01)

##supress colorbar, make in a separate plot
#plt.colorbar().set_label("CL of exclusion")


##save the fig and pad it for better layout
    fig.tight_layout(pad=0.1)
    plt.savefig("./plots/combinedCL_" + root.strip('./') + ".pdf")
    plt.savefig("./plots/combinedCL_" + root.strip('./') + ".png")


############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

###brand new plot for contours, dont need to fully reset?

    fig=plt.figure(figsize=fig_dims)

    ax = fig.add_subplot(1,1,1)

##try and pick ticks intelligently

    my_locator_x = MaxNLocator((max(contourXaxis) / 500.0)+1)
    my_locator_y = MaxNLocator((max(contourYaxis) / 500.0)+1)
    minorLocator_x = MaxNLocator(len(contourXaxis) +1)
    minorLocator_y = MaxNLocator(len(contourYaxis) +1)
    ax.yaxis.set_major_locator(my_locator_y)
    ax.xaxis.set_major_locator(my_locator_x)
    ax.xaxis.set_minor_locator(minorLocator_x)
    ax.yaxis.set_minor_locator(minorLocator_y)


##set axis size, again contour axis different to heatmap axis
    plt.axis([min(zip(*data)[1]), max(zip(*data)[1]), min(zip(*data)[0]), max(zip(*data)[0])])


##draw a filled contour region for the CL excl
    CS=plt.contourf(contourXaxis,contourYaxis,c.T,levels=[0.95,1.0],label="CL",cmap=cmaps.magma)
##and a black outline
    CS2=plt.contour(CS, colors = 'black')

#CS2=plab.contour(contourXaxis,contourYaxis,c.T,levels=[0.95,1.0], colors = 'black')


###plot the pert unitarity bound
    y=np.array(contourYaxis)
    x=pertUnit(y)
    plt.plot(x,y,color='black')
    ax.fill_between(x,y,1.,facecolor='navy',alpha=0.8)

###contour labeler
    fmt={}
    strs=['95\% CL','CL']
    for l , s in zip(CS2.levels, strs):
        fmt[l]=s

###Messing with manually placed labels for contours
#manual_loc=[(800,1300),(400,300)]
#plab.clabel(CS2, CS2.levels[::2], inline=1, fmt=fmt, fontsize=10, manual=manual_loc)
#txt = plab.text(700,1100,'95\% CL',backgroundcolor='white')
#plab.clabel(CS2, inline=1, fontsize=10, manual=manual_loc)


    plt.xlabel(r"$M_{DM}$ [GeV]")
    plt.ylabel(r"$M_{Z'}$ [GeV]")
    artists, labels = CS.legend_elements()

##potential legend info, edit here:
#plt.legend(artists, labels, handleheight=2,loc=2)


#plt.legend(handles=[CS])
#plt.rc('text', usetex=False)
#plt.rc('font', family='sans')
#, fontsize=12
#plab.title("CL Contour",y=1.01)
#legend = ax.legend(loc='upper center', shadow=True)
#plab.colorbar(ticks=[0,0.5,1.0]).set_label("CL of exclusion")

##save the fig and pad it for better layout
    fig.tight_layout(pad=0.1)
#fig.savefig('figure.pdf')

    plt.savefig("./plots/contour_" + root.strip('./') + ".pdf")
    plt.savefig("./plots/contour_" + root.strip('./') + ".png")

    print "Plotting maps: " + root.strip('./')


############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

##print the colorbar on a separate plot

fig=plt.figure(figsize=[fig_dims[0]*2,0.5])
ax = fig.add_subplot(1,1,1)
import matplotlib as mpl
norm = mpl.colors.Normalize(vmin=0, vmax=1)
cb = mpl.colorbar.ColorbarBase(ax, cmap=cmaps.magma, orientation='horizontal', norm=norm)
cb.set_label("CL of exclusion")
fig.tight_layout(pad=0.1)
plt.savefig('./plots/colorbarkey.pdf')