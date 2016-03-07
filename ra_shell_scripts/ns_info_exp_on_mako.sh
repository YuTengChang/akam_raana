#!/usr/bin/env bash

# get time
epochtime=`date +%s`
regulartime=`date`
temp_file="/home/ychang/tmp/ns_exp.txt"
output_file="/home/ychang/tmp/ns_exp_all.ext"

# get the checksum of the particular mako result
/home/ychang/bin/mako --csv -s "select * from (select ip, demand, pingpoint, country, city, asnum, rank() over (partition by country order by demand desc) rankings from ns_info where country='JP') where rankings=2258 " | tail -1 > $temp_file
md5str=`cat $temp_file`

# write to the experiment result
echo $epochtime $regulartime $md5str >> $output_file