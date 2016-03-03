#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 15:58:55 2015

@author: ychang

This script do the insertion of RA-Info files

"""
import sys,os
sys.path.append('/home/testgrp/RAAnalysis/')
import subprocess as sp
import glob
import time
import configurations.config as config
import configurations.hdfsutil as hdfs

def main():
    # parameters
    # RAinput='/home/testgrp/RAAnalysis/ra_data/ra_msg/assignments_agg'

    # current time
    timenow = int(time.time())
    # #### RA PART ####
    for ra_concat_file in glob.glob( os.path.join(config.RAconcat,'*.txt') ):
        infoitem = ra_concat_file.split('.')
        datestamp = infoitem[1]
        UUID = infoitem[2]
        STARTTIME = infoitem[3]
        ENDTIME = infoitem[4]
        print 'uuid=%s, starttime=%s, endtime=%s, datestamp=%s' % (UUID, STARTTIME, ENDTIME, datestamp)

        # upload ra_concat_file to HDFS
        print '*** uploading file to HDFS ' + ra_concat_file
        try:
            sp.check_call(['hadoop', 'fs', '-put', ra_concat_file, config.hdfs_ra_intermediate])
            sp.check_call(['rm', ra_concat_file])
            intermediate_file_name = ra_concat_file.split('/')[-1]
        except:
            print 'HDFS file upload error'
            # still remove the local file (keeps from cumulating the concatenated files)
            sp.check_call(['rm', ra_concat_file])
            continue # check the next ra_concat_file

        # create corresponding HDFS directory
        # PIG will create the HDFS in the designated folder

        # run PIG script to utilize AVRO
        # example: HADOOP_USER_NAME=akamai; pig11 -p datestamp=20151201 -p uuid=0e0bda82-9823-11e5-b44e-300ed5c5f881 -p ts=1448980818 /home/testgrp/RAAnalysis/pig/csv_to_avro.pig
        print '*** pig serializes the data into HDFS for file ' + ra_concat_file
        cmd = '%s; %s -p datestamp=%s -p uuid=%s -p ts=%s %s; %s' % ( config.cmd_hadoop_user_akamai,
                                                                      config.cmd_pig11,
                                                                      datestamp,
                                                                      UUID,
                                                                      STARTTIME,
                                                                      config.csv_to_avro_pig_script,
                                                                      config.cmd_hadoop_user_testgrp )
        #print cmd
        try:
            print 'try the pig script...'
            sp.check_call( cmd, shell=True )
            # pig log cleanup _log directory and _SUCCESS file when successful
            this_ra_temp_hdfs_location = config.hdfs_ra_temp % (datestamp,
                                                                UUID,
                                                                STARTTIME)
            this_ra_map_hdfs_location = config.hdfs_ra_map % (datestamp,
                                                              UUID,
                                                              STARTTIME)

            # copy the file from ramap [PIG OUTPUT] to RA_map folder [HIVE]
            print 'copy the file to RA_map folder'
            print 'HDFS copy RA-avro fail' if hdfs.cp( this_ra_temp_hdfs_location+'/part-r-00000.avro',
                                                       this_ra_map_hdfs_location) else 'HDFS copy RA-avro success'

            # remove the remainder in ramap [PIG output] folder (not fully clear yet)
            print 'remove the remainder in the ramap folder'
            cmd = '%s; hadoop fs -rm -r %s; %s' % (config.cmd_hadoop_user_akamai,
                                                   this_ra_temp_hdfs_location,
                                                   config.cmd_hadoop_user_testgrp)
            sp.check_call( cmd, shell=True )
            #cmd = '%s; hadoop fs -rm %s/_SUCCESS' % (config.cmd_hadoop_user_change,
            #                                         this_ra_map_hdfs_location)
            #sp.check_call( cmd, shell=True )

            # remove the remainder in the RA_pre_Avro folder
            print 'intermediate_file_name = ' + intermediate_file_name
            hdfs.rm( config.hdfs_ra_intermediate+'/'+intermediate_file_name )

            # update the HIVE table
            cmd = "hive -e 'use raana; MSCK REPAIR TABLE ra_map;'"
            sp.check_call( cmd, shell=True )

        except:
            print 'PIG script Error.'

        # Alter HIVE table correspondingly


    # #### NS PART ####
    # list_ns_files = glob.glob( os.path.join(config.NSdata,'*_mpg*.txt') ) # glob get the full path
    # for fileitem in list_ns_files:
    # config.hdfs_ns_info
    # #### RG PART ####

if __name__=='__main__':
    sys.exit(main())
