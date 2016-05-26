#! /usr/bin/env python


import rivet, yoda, sys, os
for root, dirs, files in os.walk('.'):
        filelist=''
        outfile=''
        for name in files:
            #filelist=''
            if '.yoda' not in name:
                continue
            yodafile = os.path.join(root, name)
            filelist += " " + yodafile
        print filelist
        if not filelist:
            continue
        else:
            os.system("yodamerge -o " + root + "/" +root.strip("./")+".yoda " + filelist)

#print 'break'
