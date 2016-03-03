#!/bin/bash
# manage data from mdt to cluster

# aliases and hadoop paths
source /home/testgrp/ksprong/login.conf

# local working dirs
wdir="/home/testgrp/ksprong/hdm/"
md5dir="/home/testgrp/ksprong/tmp/mapmon/md5sums"
tsvdir="/home/testgrp/ksprong/tmp/mapmon/tsv"
csvdir="/home/testgrp/ksprong/tmp/mapmon/csv"

# hadoop target directories
hdfsintermed="/ghostcache/hadoop/devel/mapmon"
hdfsdir="/ghostcache/hadoop/data/mapmon"

# get new raw files
for f in `ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments*`; do 
    # get basename
    fout=`echo "$f" | cut -d'/' -f6 | sed -r 's/\s+//g'`
    # see if checksum of first part of file has changed
    prevck=""
    if [ -s $md5dir/$fout ]; then
        prevck=`cat $md5dir/$fout`
    fi
    newck=`head -c 10000 $f | md5sum | awk '{ print $1 }'`
    if [ "$prevck" != "$newck" ]; then
        # get a tsv of the file
        PrintMessage $f > $tsvdir/$fout;
        ts=`head -n 4 $tsvdir/$fout | tail -n 1 | cut -d':' -f2 | sed -r 's/\s+//g'`
        echo $fout " : " $ts
        mv $tsvdir/$fout $tsvdir/$ts.$fout
        # update checksum for future reads
        echo $newck > $md5dir/$fout
    fi
done

# make full sets into csv
nfiles=`ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments* | sort | tail -n 1 | cut -d'.' -f 5`
availablets=`ls $tsvdir | cut -d'.' -f1`
newestfullset=`printf '%s\n' "${availablets[@]}" | sort -n | uniq -c | egrep "$nfiles\s" | sed -r 's/^\s+//g' | cut -d' ' -f2 | sort -n | tail -n 1`
# might as well also process any ts earlier than the latest full set
tstoprocess=`printf '%s\n' "${availablets[@]}" | awk -v maxts="$newestfullset" '$1 <= maxts {print $1}' | sort -n | uniq`
for ts in $tstoprocess; do
    echo processing $ts into csvs
    python $wdir/tsv_to_csv.py $ts

    echo pushing to hdfs
    ymd=`date -d @$ts +%Y%m%d`
    hadoop fs -copyFromLocal $csvdir/$ts.* $hdfsintermed/csv/

    # only cleanup locally on hdfs success
    if [ $? -eq 0 ]; then
        echo hdfs push succeeeded, removing local files
        rm $tsvdir/$ts.*
        rm $csvdir/$ts.*
    fi

    echo avroizing
    # pig11 alias includes many jars needed to run avro jobs
    pig11 -p ts=$ts $wdir/csv_to_avro.pig
    
    # only cleanup on avro job success
    if [ $? -eq 0 ]; then
        echo avro job succeeded, removing intermediate hdfs files
        hadoop fs -rm -r $hdfsintermed/csv/$ts.*
        # should only be one file matching the glob; pig script mandates 1 reducer
        hadoop fs -mv $hdfsintermed/avro/$ts/part-r-*.avro $hdfsdir/$ymd/$ts.snappy.avro && hadoop fs -rm -r $hdfsintermed/avro/$ts
    fi
done



