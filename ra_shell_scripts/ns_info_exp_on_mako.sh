#!/usr/bin/env bash

# get time
epochtime=`date +%s`
regulartime=`date`
temp_file="/home/ychang/tmp/ns_exp.txt"
output_file="/home/ychang/tmp/ns_exp_all.ext"

# get the checksum of the particular mako result
/home/ychang/bin/mako --csv -s "select sum(demand) from ns_info where COUNTRY='JP' " | tail -1 > $temp_file
md5str=`cat $temp_file`

# write to the experiment result
echo $epochtime $regulartime $md5str >> $output_file