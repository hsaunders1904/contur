#Log onto plus1 UCL > then to a PC
source /unix/cedar/software/sl6/setupEnv.sh
#checkout code and source setup file in top level of svn
source setupContour.sh

-----------------------------------------

#Copy the grid setup to a test folder
cp -r $CONTURMODULEDIR/AnalysisTools/GridSetup/* .

-----------------------------------------

#2 ways of running, specific to the simple DM model but can be modified




#HerwigCommandHad - runs inclusive generation of BSM particles

#For test case we only have 1 new mediator so force generator to produce this and inclusively all LO 2->2 scatters involving the mediator
insert HPConstructor:Outgoing 0 /Herwig/FRModel/Particles/Y1
set HPConstructor:Processes SingleParticleInclusive

#Also add resonant S channel 2->2 scatter involving mediator via
insert ResConstructor:Intermediates 0 /Herwig/FRModel/Particles/Y1
#with some other bits to specify the desired interactions in the resonant mode



#HerwigCommandWeak - forces associated production modes of weak bosons

#Forces decay modes of SM bosons via
do /Herwig/Particles/Z0:SelectDecayModes Z0->e-,e+;
set /Herwig/Particles/Z0/Z0->mu-,mu+;:OnOff On

#Generate Y1 inclusive 2->2 scatters as before but now veto outgoing coloured SM particles
insert HPConstructor:ExcludedExternal 0 /Herwig/Particles/c
insert HPConstructor:ExcludedExternal 0 /Herwig/Particles/cbar


#At End of these files theres a line like:
set LHCGenerator:EventHandler:LuminosityFunction:Energy 7000.0
read 7_WEAK.ana
#Which sets the CoM energy and loads the relevant rivet analyses in the .ana files
#.ana files are in the GridPack folder copied over

-----------------------------------------


#Do a single test run
cd GridPack
cp ../HerwigCommandHad TestRun.in
#Herwig utility to read the UFO model folder and build it

ufo2herwig VDM_simplified_model_UFO && make

-----------------------------------------

#HerwigCommand snippets are for batch runs so add the three lines to the begining of your TestRun.in
read FRModel.model
set /Herwig/FRModel/Particles/Y1:NominalMass 1000.*GeV
set /Herwig/FRModel/Particles/Xm:NominalMass 600.*GeV

#Build the Herwig runcard
Herwig read TestRun.in

#Generate the events and pipe straight through rivet
Herwig run LHC.run -N 2000

-----------------------------------------


#Run the single test script on the output yoda
CLTestSingle LHC.yoda

#prints
Combined CL: 0.743664
Based on 11 found counting tests

More details output to ANALYSIS folder

#Also makes a plots directory containing all the .dat files for the analyses scanned


----------------------------------------

#Todo a batch run to make a grid,
cd ..
#Back to the base directory copied over

emacs BatchSubmitHad.py

#make sure the two sourced files are in the right location, and change the grid size, granularity in the for loop

#outputs a folder structure like
cd /unix/atlas4/yallup/ConturGrids/gq05/gq05had_7/

#To build the heatmaps, in this directory run
YodaMerger

#To merge all the output yodas and
CLTest

#To do the analysis and output a folder ANALYSIS
cd ANALYSIS

PlotMaker

#to make the heatmaps