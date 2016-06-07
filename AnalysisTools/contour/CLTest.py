import rivet, yoda, sys, os
from contour import TestingFunctions as ctr
from contour import Utils as util


def getHistos(filelist):
    """Loop over all input files. Only use the first occurrence of any REF-histogram
    and the first occurrence in each MC file for every MC-histogram."""
    ##Stolen from rivet-cmphistos
    refhistos = {}
    mchistos = {}
    #for infile in filelist:
    mchistos.setdefault(filelist, {})
    analysisobjects = yoda.read(filelist)
    for path, ao in analysisobjects.iteritems():
            ## Conventionally don't plot data objects whose names start with an underscore
        if os.path.basename(path).startswith("_"):
            continue
        if path.startswith('/REF/'):
            if not refhistos.has_key(path):
                refhistos[path] = ao
        else:
            if not mchistos[filelist].has_key(path):
                mchistos[filelist][path] = ao
    return refhistos, mchistos

def getRivetRefData(refhistos, anas=None):
    "Find all Rivet reference data files"
    rivet_data_dirs = rivet.getAnalysisRefPaths()
    dirlist = []
    for d in rivet_data_dirs:
        if anas is None:
            import glob
            dirlist.append(glob.glob(os.path.join(d, '*.yoda')))
        else:
            dirlist.append([os.path.join(d, a+'.yoda') for a in anas])
    for filelist in dirlist:
        # TODO: delegate to getHistos?
        for infile in filelist:
            analysisobjects = yoda.read(infile)
            for path, ao in analysisobjects.iteritems():
                if path.startswith('/REF/'):
                    if not refhistos.has_key(path):
                        refhistos[path] = ao



if __name__ == '__main__':
    #need an empty dict to store our results
    scatterpoints ={}
    masterDict={}
    heatMap={}
    for anatype in ctr.anapool:
        masterDict[anatype] =[]
    #CN.anapool()
    for root, dirs, files in os.walk('.'):
        for name in files:
            fileliststatic = []
            if '.yoda' in name and 'LHC' not in name:
                #if "1000_mX_800" not in name:
                #    continue
                #else:
                yodafile = os.path.join(root, name)
                fileliststatic = str(yodafile)
            else:
                continue
            refhistos, mchistos = getHistos(fileliststatic)
            hpaths = []
            for aos in mchistos.values():
                for p in aos.keys():
                    if p and p not in hpaths:
                        hpaths.append(p)

            getRivetRefData(refhistos)

            mapPoints={}

            for h in hpaths:
                if refhistos.has_key('/REF' + h):
                    refdata = refhistos['/REF' + h]
				#Manually store additional plot in a function called LumiFinder, if a Lumi isn't stored vs an
				#analysis name then use that info to veto testing
                if ctr.LumiFinder(h)[0] == -1:
                    continue
                #Use this switch to view individual analyses
                if '/ATLAS_2014_I1268975' not in h:
                    continue
                print 'testing: ' + h
                lumi = ctr.LumiFinder(h)[0]
                if lumi > 0:
					#make some empty arrays, not all of these are used, can definitely be optimised and cleaned up but used for de
					#bugging for now
                    sighisto=yoda.core.mkScatter(mchistos[fileliststatic][h])
                    CLs=[]
                    sigCount = []
                    bgCount = []
                    bgError = []
                    sigError = []
                    #fill test results for each bin
                    #out=np.zeros([refdata.numPoints,1])
                    for i in range(0,refdata.numPoints):
                        global mu_test
                        mu_test=1
                        mu_hat=0
                        varmat=0
                        sigCount.append(sighisto.points[i].y*lumi)
                        bgCount.append(refdata.points[i].y*lumi)
                        bgError.append(refdata.points[i].yErrs[1]*lumi)
                        sigError.append(sighisto.points[i].yErrs[1]*lumi)
                        ##cater for the case where the refdata bin is empty, occurs notably in ATLAS_2014_I1307243
                        if refdata.points[i].y > 0:
                            CLs.append(ctr.confLevel([sigCount[i]],[bgCount[i]],[bgError[i]],[sigError[i]]))
                        else:
                            CLs.append(0)
                            # Var_mu(mu_test,ML_b_hat_model(refdata.points[i].y*lumi,mu_test,refdata.points[i].y*lumi,sighisto.points[i].y*lumi,refdata.points[i].yErrs[1]*lumi),sighisto.points[i].y*lumi,refdata.points[i].yErrs[1]*lumi)[0,0]
                            # mu_hat=ML_mu_hat(refdata.points[i].y*lumi,refdata.points[i].y*lumi,sighisto.points[i].y*lumi)


##All these extra count checks are to stop any plots with no count in most likely bin from being entered
##into liklihood calc, should be fixed upstream
                if ctr.LumiFinder(h)[2]:
                    tempKey = ''
                    tempKey= h.split('/')[1] +'_'+ctr.LumiFinder(h)[2]
                    if tempKey not in mapPoints and bgCount[CLs.index(max(CLs))]>0.0:
                        mapPoints[tempKey] = [float(name.strip('.yoda').split('_')[1]),float(name.strip('.yoda').split('_')[3]), float(max(CLs)) , [sigCount[CLs.index(max(CLs))]], [bgCount[CLs.index(max(CLs))]] , [bgError[CLs.index(max(CLs))]], [sigError[CLs.index(max(CLs))]]]
                    elif bgCount[CLs.index(max(CLs))] > 0.0:
                        mapPoints[tempKey][3].append(sigCount[CLs.index(max(CLs))])
                        mapPoints[tempKey][4].append(bgCount[CLs.index(max(CLs))])
                        mapPoints[tempKey][5].append(bgError[CLs.index(max(CLs))])
                        mapPoints[tempKey][6].append(sigError[CLs.index(max(CLs))])
                else:
                    if h not in mapPoints and bgCount[CLs.index(max(CLs))]>0.0:
                        mapPoints[h] = [float(name.strip('.yoda').split('_')[1]),float(name.strip('.yoda').split('_')[3]), float(max(CLs)) , [sigCount[CLs.index(max(CLs))]], [bgCount[CLs.index(max(CLs))]] , [bgError[CLs.index(max(CLs))]],[sigError[CLs.index(max(CLs))]]]
            for key in mapPoints:
                tempName = ctr.LumiFinder(key)[1]
                mapPoints[key][2] = ctr.confLevel(mapPoints[key][3],mapPoints[key][4],mapPoints[key][5], mapPoints[key][6])
                if not masterDict[tempName]:
                    masterDict[tempName].append(mapPoints[key][:])
                else:
                    _overWriteFlag = False
                    _pointExistsFlag = False
                    for listelement in masterDict[tempName]:
                        if mapPoints[key][0] == listelement[0] and mapPoints[key][1] == listelement[1]:
                            _pointExistsFlag = True
                            if mapPoints[key][2] > listelement[2]:
                                masterDict[tempName][masterDict[tempName].index(listelement)] = mapPoints[key][:]
                                #listelement = mapPoints[key][:]
                                _overWriteFlag=True
                    if _overWriteFlag == False and _pointExistsFlag == False:
                        masterDict[tempName].append(mapPoints[key][:])


                # else if mapPoints[key][]
                # else if mapPoints[key][2] > masterDict[tempName]
                #
                # masterDict[]
    import pickle
    for key in masterDict:
        if masterDict[key]:
            masterDict[key].sort(key=lambda x: x[0])
            util.writeOutput(masterDict[key],key + ".dat")
            with open("./ANALYSIS/"+key+'.map', 'w') as f:
                pickle.dump(masterDict[key], f)


print 'end'
