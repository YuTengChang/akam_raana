#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 15:58:55 2015

@author: ychang

This script do the insertion of RG-Info files

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
    list_rg_files = glob.glob( os.path.join(config.RGdata,
                                            'region_info_*.txt') ) # glob get the full path
    for rg_file in list_rg_files:
        infoitem = rg_file.split('_')
        datestamp = infoitem[-1].split('.')[0]
        print 'file = ' + rg_file
        print '    datestamp = %s' % ( datestamp )

        # put the file to HDFS folder and remove from Local
        try:
            print '    upload to HDFS'
            hdfs_rg_destination = config.hdfs_rg_info % datestamp
            hdfs.mkdir( hdfs_rg_destination )
            hdfs.put( rg_file, hdfs_rg_destination )

            print '    adding partition'
            hiveql_str = config.add_rg_partition % ( datestamp )
            sp.check_call(['hive','-e',hiveql_str])
            sp.check_call(['rm',rg_file])
        except:
            print 'region information update failed for date=%s.' % datestamp


if __name__=='__main__':
    sys.exit(main())
