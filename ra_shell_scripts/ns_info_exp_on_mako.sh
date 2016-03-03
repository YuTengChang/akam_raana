#!/usr/bin/env bash

# get time
epochtime=`date +%s`
regulartime=`date`
temp_file="/home/ychang/tmp/ns_exp.txt"
output_file="/home/ychang/tmp/ns_exp_all.ext"

# get the checksum of the particular mako result
/home/ychang/bin/mako --csv -s "select * from (select * from ns_info where COUNTRY='JP' order by demand desc) where rownum<=20" > $temp_file
md5str=`/usr/bin/md5sum $temp_file | awk '{print $1}'`

# write to the experiment result
echo $epochtime $regulartime $md5str >> $output_file