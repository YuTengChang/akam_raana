#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 15:58:55 2015

@author: ychang
"""
import sys,os
sys.path.append('/home/testgrp/RAAnalysis/')
import subprocess as sp
import time
#import httplib
import YT_Timeout as ytt
import configurations.config as config

def main():
    ''' this function perform the necessary pre-processing steps on RA messages
    and upload the data to the hadoop cluster '''

#==============================================================================
#   # combine RegionAssignment Message
#==============================================================================




#==============================================================================
#   # Print Out the distinct MPD Tree
#==============================================================================




#==============================================================================
# # remove partitions from hive table
#==============================================================================

def mrqos_table_cleanup():
    ''' when called, this function will delete all partitions
        the clnspp table as long as it is older than the threshold '''

    #get the lowest partition
    partition_list = open('/tmp/testgrp/mrqos_table_partitions.txt','w')
    sp.call(['hive','-e','use mrqos; show partitions score;'],stdout=partition_list)
    partition_list.close()
    partition_list = open('/tmp/testgrp/mrqos_table_partitions.txt','r')
    str_parts = partition_list.read()
    partition_list.close()
    os.remove('/tmp/testgrp/mrqos_table_partitions.txt')
    str_parts_list = [i.split('=',1)[1] for i in str_parts.strip().split('\n')]
    str_parts_list_int=map(int,str_parts_list)

    #check if "partitions" is within the threshold
    timenow = int(time.time())
    for partition in str_parts_list_int:
        if partition < timenow - config.mrqos_table_delete:
            try:
                mtype = ['score','distance','in_country','in_continent','ra_load'];
                for item in mtype:
                    # drop partitions
                    sp.check_call(['hive','-e','use mrqos; alter table ' + item + ' drop if exists partition(ts=%s)' % partition])
                    # remove data from HDFS
                    hdfs_d = os.path.join(config.hdfs_table,item,'ts=%s' % partition)
                    sp.check_call(['hadoop','fs','-rm','-r', hdfs_d])
            except sp.CalledProcessError:
                raise GenericHadoopError


#==============================================================================
# # remove partitions from hive table
#==============================================================================

def mrqos_join_cleanup():
    ''' when called, this function will delete all partitions
        the clnspp table as long as it is older than the threshold '''

    #get the lowest partition
    partition_list = open('/tmp/testgrp/mrqos_table_partitions.txt','w')
    sp.call(['hive','-e','use mrqos; show partitions mrqos_join;'],stdout=partition_list)
    partition_list.close()
    partition_list = open('/tmp/testgrp/mrqos_table_partitions.txt','r')
    str_parts = partition_list.read()
    partition_list.close()
    os.remove('/tmp/testgrp/mrqos_table_partitions.txt')
    str_parts_list = [i.split('=',1)[1] for i in str_parts.strip().split('\n')]
    str_parts_list_int=map(int,str_parts_list)

    #check if "partitions" is within the threshold
    timenow = int(time.time())
    for partition in str_parts_list_int:
        if partition < timenow - config.mrqos_join_delete:
            try:
                # drop partitions
                sp.check_call(['hive','-e','use mrqos; alter table mrqos_join drop if exists partition(ts=%s)' % partition])
                # remove data from HDFS
                hdfs_d = os.path.join(config.hdfs_table,'mrqos_join','ts=%s' % partition)
                sp.check_call(['hadoop','fs','-rm','-r', hdfs_d])
            except sp.CalledProcessError:
                raise GenericHadoopError


#==============================================================================
# # upload to hdfs and link to hive table
#==============================================================================

def upload_to_hive(listname, hdfs_d, ts, tablename):
    ''' this function will create a partition directory in hdfs with the requisite timestamp. It will
    then add the partition to the table cl_ns_pp with the appropriate timestamp '''

    #hdfs_d = config.hdfsclnspp % (ts)
    # create the partition
    try:
        sp.check_call(['hadoop','fs','-mkdir',hdfs_d])
    # upload the data
    except sp.CalledProcessError:
        raise HadoopDirectoryCreateError
    try:
        sp.check_call(['hadoop','fs','-put',listname,hdfs_d])
    except sp.CalledProcessError:
        raise HadoopDataUploadError

    # add the partition
    try:
        hiveql_str = 'use mrqos; alter table ' + tablename + ' add partition(ts=%s);' % (ts)
        sp.check_call(['hive','-e',hiveql_str])
    except sp.CalledProcessError:
        raise HiveCreatePartitionError


#==============================================================================
# # hdfs error category
#==============================================================================
class HadoopDirectoryCreateError(Exception):
    def __init__(self):
        self.message = "Unable to create directory."

class HadoopDataUploadError(Exception):
    def __init__(self):
        self.message = "Unable to upload data to hdfs."

class HiveCreatePartitionError(Exception):
    def __init__(self):
        self.message = "Unable to create partition"

class GenericHadoopError(Exception):
    def __init__(self):
        self.message = "Something went wrong in deleting a partition or associated data"


if __name__=='__main__':
    sys.exit(main())
