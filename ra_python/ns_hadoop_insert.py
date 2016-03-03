#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 15:58:55 2015

@author: ychang

This script do the insertion of NS-Info files

"""
import sys,os
sys.path.append('/home/testgrp/RAAnalysis/')
import subprocess as sp
import glob
import time
import configurations.config as config
import configurations.hdfsutil as hdfs

def main():
    # #### RG PART ####
    datestamp = time.strftime( "%Y%m%d", time.gmtime() )
    list_ns_files = glob.glob( os.path.join(config.NSdata,
                                            'ns_info_*mpg.*.txt') ) # glob get the full path
    for ns_file in list_ns_files:
        infoitem = ns_file.rsplit('_',2)
        datestamp = infoitem[1]
        UUID = infoitem[2].split('.')[1]
        print 'file = ' + ns_file
        print '    datestamp = %s; UUID = %s' % ( datestamp,
                                                  UUID )

        # put the file to HDFS folder and remove from Local
        try:
            print '    upload to HDFS'
            hdfs_ns_destination = config.hdfs_ns_info % ( datestamp, UUID )
            hdfs.mkdir( hdfs_ns_destination )
            hdfs.put( ns_file, hdfs_ns_destination )

            print '    adding partition'
            hiveql_str = config.add_ns_partition % ( datestamp, UUID )
            print '    '+hiveql_str
            sp.check_call(['hive','-e',hiveql_str])
            print '    remove local file: ' + ns_file
            sp.check_call(['rm',ns_file])
        except:
            print 'resolver(NS) information update failed for date=%s, uuid=%s' % ( datestamp, UUID )


if __name__=='__main__':
    sys.exit(main())
