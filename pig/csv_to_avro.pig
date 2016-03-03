/*
Simple csv -> avro conversion for mapmon data, flat schema
*/
-- this has been commented out
--REGISTER piggybank.jar
--REGISTER avro-1.7.6.jar
--REGISTER avro-mapred-1.7.6-hadoop2.jar
--REGISTER json-simple-1.1.jar
--REGISTER snappy-java-1.0.4.1.jar
--REGISTER jackson-core-asl-1.9.13.jar
--REGISTER jackson-mapper-asl-1.9.13.jar

SET mapred.compress.map.output true;
SET mapred.output.compress true;
SET mapred.output.compression.codec org.apache.hadoop.io.compress.SnappyCodec
SET avro.output.codec snappy;
SET mapred.task.timeout 600000;

SET default_parallel 1;

%declare LOCAL_DIR '/home/testgrp/RAAnalysis/pig'
%declare HDFS_BASE_DIR '/ghostcache/hadoop/data/RAANA'

%declare SCHEMA `cat $LOCAL_DIR/ra_concat.avsc`
%default ts 'avrotest'

SET job.name 'Mapmon ingest: CSV to Avro'

-- load N csv files, order, and write out one avro file
data = LOAD '$HDFS_BASE_DIR/RA_pre_Avro/*$ts*' USING PigStorage(',') AS
(mpgid:int,
 mrid:int,
 mpg_type:int,
 region:int,
 link:int,
 cnt:int,
 min_s:int,
 max_s:int,
 min_r:int,
 max_r:int,
 t_st:int,
 dftime:int,
 mpd_uuid:chararray);

data = ORDER data BY mpgid, mrid, cnt;

STORE data INTO '$HDFS_BASE_DIR/ramap/datestamp=$datestamp/uuid=$uuid/ts=$ts'
USING AvroStorage('{
"index" : 1,
"schema": $SCHEMA}');
