#!/bin/bash

hive -f /home/testgrp/RAAnalysis/hive_inits/RAANA_RA_table_init.hive
export HADOOP_USER_NAME=akamai
hadoop fs -chown testgrp /ghostcache/hadoop/data/RAANA
hadoop fs -chown testgrp /ghostcache/hadoop/data/RAANA/RA_map
export HADOOP_USER_NAME=testgrp

hadoop fs -mkdir /ghostcache/hadoop/data/RAANA/RA_map/uuid=501ee1fc-8703-11e5-bcea-008cfa145db8/datestamp=2015-11-09/ts=1447100427
hadoop fs -put /home/testgrp/RAAnalysis/ra_data/ra_concated/Assignment.1447100427.1447101617.501ee1fc-8703-11e5-bcea-008cfa145db8.2015-11-09.txt /ghostcache/hadoop/data/RAANA/RA_map/uuid=501ee1fc-8703-11e5-bcea-008cfa145db8/datestamp=2015-11-09/ts=1447100427

hive -e "use RAANA; alter table ra_map add partition(uuid='501ee1fc-8703-11e5-bcea-008cfa145db8', datestamp='2015-11-09', ts='1447100427');"

hive -f /home/testgrp/RAAnalysis/hive_inits/RAANA_NS_table_init.hive
export HADOOP_USER_NAME=akamai
hadoop fs -chown testgrp /ghostcache/hadoop/data/RAANA/ns_info
export HADOOP_USER_NAME=testgrp

hadoop fs -mkdir /ghostcache/hadoop/data/RAANA/ns_info/uuid=501ee1fc-8703-11e5-bcea-008cfa145db8
hadoop fs -put /home/testgrp/RAAnalysis/ra_data/ns_info/ns_mpg.501ee1fc-8703-11e5-bcea-008cfa145db8.1447100427.csv /ghostcache/hadoop/data/RAANA/ns_info/uuid=501ee1fc-8703-11e5-bcea-008cfa145db8

hive -e "use RAANA; alter table ns_info add partition(uuid='501ee1fc-8703-11e5-bcea-008cfa145db8');"

hive -e "use RAANA; set hive.cli.print.header=true; select a.*, nsip, asnum from ra_map a join ns_info b on (a.uuid=b.uuid and a.mpgid=b.mpgid);" > /home/testgrp/RAAnalysis/ra_data/ra_intermediate/ra_ns_tmp.txt

