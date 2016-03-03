# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:57:38 2015

@author: ychang
"""

### configuration files

#==============================================================================
# # HDFS Locations
#==============================================================================
#hdfs_score = '/ghostcache/hadoop/data/MRQOS/score/ts=%s'
#hdfs_distance = '/ghostcache/hadoop/data/MRQOS/distance/ts=%s'
#hdfs_in_country = '/ghostcache/hadoop/data/MRQOS/in_country/ts=%s'
#hdfs_in_continent = '/ghostcache/hadoop/data/MRQOS/in_continent/ts=%s'
#hdfs_ra_load = '/ghostcache/hadoop/data/MRQOS/ra_load/ts=%s'
hdfs_table = '/ghostcache/hadoop/data/MRQOS'
hdfs_ra_intermediate = '/ghostcache/hadoop/data/RAANA/RA_pre_Avro'
hdfs_ra_map = '/ghostcache/hadoop/data/RAANA/RA_map/datestamp=%s/uuid=%s/ts=%s'
hdfs_ns_info = '/ghostcache/hadoop/data/RAANA/ns_info/datestamp=%s/uuid=%s'
hdfs_ra_temp = '/ghostcache/hadoop/data/RAANA/ramap/datestamp=%s/uuid=%s/ts=%s'
hdfs_rg_info = '/ghostcache/hadoop/data/RAANA/rg_info/datestamp=%s'

#==============================================================================
# # Local File Locations
#==============================================================================
# DIRECTORY
RAinput='/home/testgrp/RAAnalysis/ra_data/ra_msg/assignments_agg'
RAconcat='/home/testgrp/RAAnalysis/ra_data/ra_concated'
MPGtree='/home/testgrp/RAAnalysis/ra_data/mpg_tree'
NSdata='/home/testgrp/RAAnalysis/ra_data/ns_info'
RGdata='/home/testgrp/RAAnalysis/ra_data/rg_info'

ra_data = '/home/testgrp/RAAnalysis/ra_data/ra_msg'
rg_data = '/home/testgrp/RAAnalysis/ra_data/rg_info'
ra_query = '/home/testgrp/RAAnalysis/ra_query'

# FILE
ra_msg_header = 'RA_Header_File_single_one_eighth.tmp'
csv_to_avro_pig_script = '/home/testgrp/RAAnalysis/pig/csv_to_avro.pig'

#==============================================================================
# # Constant Configurations
#==============================================================================
query_retrial = 20 # 20 times
query_timeout = 20 # 20 sec

mrqos_table_delete = 60 * 30 # 1800 sec = 30 minutes
mrqos_join_delete = 60 * 60 * 24 * 32 # 32 days

mapmon_msg_latency = 60 * 60 * 1.5 # 5400 sec = 1.5 hours


#==============================================================================
# # HIVE Scripts, table managements
#==============================================================================
add_rg_partition = 'use RAANA; alter table rg_info add partition(datestamp=%s);'
add_ns_partition = 'use RAANA; alter table ns_info add partition(datestamp=%s,uuid="%s");'

#==============================================================================
# # PIG Settings
#==============================================================================
cmd_hadoop_user_akamai = 'HADOOP_USER_NAME=akamai'
cmd_hadoop_user_testgrp = 'HADOOP_USER_NAME=testgrp'
cmd_pig = '/home/testgrp/pig/pig-0.11.0-cdh4.6.0/bin/pig'
cmd_pig11 = '%s -Dpig.additional.jars=/home/testgrp/pig/pig-0.11.0-cdh4.6.0/lib/piggybank.jar:/home/testgrp/pig/pig-0.11.0-cdh4.6.0/lib/avro-1.7.6.jar:/home/testgrp/pig/pig-0.11.0-cdh4.6.0/lib/avro-mapred-1.7.6-hadoop2.jar:/home/testgrp/pig/pig-0.11.0-cdh4.6.0/lib/json-simple-1.1.jar:/home/testgrp/pig/pig-0.11.0-cdh4.6.0/lib/snappy-java-1.0.4.1.jar:/home/testgrp/pig/pig-0.11.0-cdh4.6.0/lib/jackson-core-asl-1.9.13.jar:/home/testgrp/pig/pig-0.11.0-cdh4.6.0/lib/jackson-mapper-asl-1.9.13.jar -Dudf.import.list=org.apache.pig.piggybank.storage.avro' % cmd_pig
