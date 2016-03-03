#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 15:58:55 2015

@author: ychang

This script do the concatenation of RA files

"""
import sys,os
sys.path.append('/home/testgrp/RAAnalysis/')
import subprocess as sp
import glob
import time
import configurations.config as config
import shutil

def main():
    # parameters
    # RAinput='/home/testgrp/RAAnalysis/ra_data/ra_msg/assignments_agg'

    # current time
    timenow = int(time.time())
    # #### RA PART ####
    # only process folder with "age" one hour or more
    #cmd = 'rm /home/testgrp/RAAnalysis/ra_data/ra_concated/Assign*'
    #sp.check_call(cmd, shell=True)
    #cmd = 'rm /home/testgrp/RAAnalysis/ra_data/mpg_tree/MPG*'
    #sp.check_call(cmd, shell=True)
    print "********************************"
    print "start processing at %s"% str(timenow)
    print "********************************"
    for diritem in os.listdir( config.RAinput ):
        # exclude if not a valid directory
        if not os.path.isdir( os.path.join( config.RAinput, diritem) ):
            print '%s not a valid folder' % diritem
            continue
        # processing the folder
        if (timenow-int(diritem) > config.mapmon_msg_latency):
            print 'processing folder: ' + diritem
            # print header from one file
            header_file = os.path.join( config.RAconcat, config.ra_msg_header)
            one_RAinput_file = os.listdir( os.path.join( config.RAinput, diritem ) )[0] # pick arbitrary file
            print 'sample data for header info: ' + one_RAinput_file
            cmd = '/home/testgrp/bin/PrintMessageRegionAssignment %s | head -6 > %s' % (os.path.join(config.RAinput, diritem, one_RAinput_file), header_file)
            sp.check_call(cmd, shell=True)

            # extract index (UUID and timestamp of the RA file)
            print '    ::::::::: SAMPLE HEADER FILE ::::::::::'
            with open( header_file ) as f:
                for line in f:
                    print '    ::  '+line,
                    if 'mpd_uuid' in line:
                        UUID = line.split(' ')[1][:-1]
                    if 'start_time' in line:
                        STARTTIME = line.split(' ')[1][:-1]
                    if 'end_time' in line:
                        ENDTIME = line.split(' ')[1][:-1]
            print '    :::::::::::::::::::::::::::::::::::::::'

            datestamp = time.strftime( "%Y%m%d", time.gmtime(int(STARTTIME)) ) # get the datestamp of the patch
            dftime = int(ENDTIME) - int(STARTTIME) # get the interval width
            print 'uuid=%s, starttime=%s, endtime=%s, date=%s, dtime=%s' % (UUID, STARTTIME, ENDTIME, datestamp, str(dftime))
            ra_concat_file = os.path.join( config.RAconcat, 'Assignment.%s.%s.%s.%s.txt' % (datestamp, UUID, STARTTIME, ENDTIME) )
            cmd1 = 'var_param2="%s,%s,%s";' % (STARTTIME, dftime, UUID)

            for fileitem in os.listdir( os.path.join( config.RAinput, diritem) ):
                # write to the concatenate file
                ra_input_file = os.path.join( config.RAinput, diritem, fileitem )
                cmd2 = '''/home/testgrp/bin/PrintMessageRegionAssignment %s | tail -n+8 | awk -v var=`echo $var_param2` 'BEGIN{OFS=","}{if($1!~/mpg/){print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,var;}}' >> %s''' % (ra_input_file, ra_concat_file)
                cmd = cmd1 + cmd2
                print "process input " + ra_input_file
                sp.check_call(cmd, shell=True)

            # ####  MPD TREE & NS_INFO with lookups  ####
            list_treefiles = glob.glob( os.path.join(config.MPGtree,'*.tr') ) # glob get the full path
            mpg_output_file = os.path.join( config.MPGtree, 'MPG.%s.%s.tr' % (datestamp,UUID) )
            print 'checking for MPG tree ' + mpg_output_file
            if mpg_output_file not in list_treefiles:
                print "Create non-exist MPG tree files..."
                cmd = '/home/testgrp/bin/RALookup_new %s getATree %s' % (ra_input_file, mpg_output_file)
                sp.check_call(cmd, shell=True)
                print "NS lookups..."
                # lookup the ns info file
                ns_input_file = glob.glob( os.path.join( config.NSdata, '*_%s.txt' % datestamp) )[0] # glob get the full path
                ns_output_file = os.path.join( os.path.join( config.NSdata, 'ns_info_%s_mpg.%s.txt' % (datestamp, UUID) ) )
                cmd = '''cat %s | /home/testgrp/RAAnalysis/bin/TreeToolsUInt lookup -full %s | awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15}' > %s ''' % (ns_input_file, mpg_output_file, ns_output_file)
                print cmd
                sp.check_call(cmd, shell=True)

            # clean up the files when success concatenate
            shutil.rmtree( os.path.join( config.RAinput, diritem ) )


if __name__=='__main__':
    sys.exit(main())
