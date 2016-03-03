#!/bin/bash
# test call:
# > /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ra_shell_scripts/ra_concat.sh /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ra_data/ra_msg/assignments_agg/ /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ra_data/ra_concated/ /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ra_data/mpg_tree/ /home/ychang/Documents/Projects/09-SystemInfo/NS_info/ /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ra_data/ns_info/

# NEW VERSION:
# > /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ra_shell_scripts/ra_concat.sh /home/ychang/Documents/Projects/09-SystemInfo/RA_mapmon/assignments_agg/ /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ra_data/ra_concated/ /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ra_data/mpg_tree/ /home/ychang/Documents/Projects/09-SystemInfo/NS_info/ /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ra_data/ns_info/

# CLUSTER VERSION:     (on ddc cluster)
# > /home/testgrp/RAAnalysis/ra_shell_scripts/ra_concat.sh /home/testgrp/RAAnalysis/ra_data/ra_msg/assignments_agg/ /home/testgrp/RAAnalysis/ra_data/ra_concated/ /home/testgrp/RAAnalysis/ra_data/mpg_tree/ /home/testgrp/RAAnalysis/ra_data/ns_info/ /home/testgrp/RAAnalysis/ra_data/ns_info/

# moving the file from mdt channel to temp location
#ts_ra=$(PrintMessageRegionAssignment /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.1 | head -10 | grep 'start_time' | awk '{print $2}')
#ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.* | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} /home/testgrp/RAAnalysis/ra_data/ra_msg/assignments_agg/\$fname"

# for testing # comment out when pushed out
rm /home/testgrp/RAAnalysis/ra_data/ra_concated/Assignment.*
rm /home/testgrp/RAAnalysis/ra_data/mpg_tree/RA_UUID_List.tmp
touch /home/testgrp/RAAnalysis/ra_data/mpg_tree/RA_UUID_List.tmp

# get time and date
epochtime=`date +%s`
Year=`date -d @$epochtime -u +%Y`
Month=`date -d @$epochtime -u +%m`
Day=`date -d @$epochtime -u +%d`
Hour=`date -d @$epochtime -u +%H`

# arguments processing
file_source="$1"
file_dest="$2"
mpg_file_dest="$3"
ns_file_source="$4"
ns_file_dest="$5"

# temporary file name
TS_FileSource="RA_sourceTS.tmp"
TS_FileDest="RA_destTS.tmp"
UUID_List="RA_UUID_List.tmp"
Header_File="RA_Header_File_single_one_eighth.tmp"

# get the source file list with id=timestamp
ls -ltr $file_source | awk -F"." 'NF>2{print $5}' | sort | uniq > $file_dest$TS_FileSource

# get the dest file list with id=timestamp
ls -ltr $file_dest | awk -F"." 'NF>2{print $5}' | sort | uniq > $file_dest$TS_FileDest

# get the difference and concatenate all lines within same TIMESTAMP, attaching last column as the temporal window size
diff $file_dest$TS_FileSource $file_dest$TS_FileDest | grep '<' | sed 's/^< //g' | while read ts; do 

files=$(ls $file_source*$ts*); 
head_file=$(echo $files | tr ' ' '\n' | head -1);
PrintMessageRegionAssignment $head_file | head -6 > $file_dest$Header_File
ts2=$(grep end_time $file_dest$Header_File | cut -d" " -f2);
uuid=$(grep mpd_uuid $file_dest$Header_File | cut -d" " -f 2);
resultingFile=$(echo $file_dest'Assignment.'$ts'.'$ts2'.'$uuid'.'$Year'-'$Month'-'$Day'.txt');
var_param=`echo $(($ts2-$ts))","$uuid","$Year"-"$Month"-"$Day`;
var_param2=`echo $(($ts2-$ts))`
echo $var_param
#last one is the interval. UUID will be partition and not part of the table
#echo $files | tr ' ' '\n' | xargs -I{} /bin/bash -c "PrintMessageRegionAssignment {} | tail -n+8 | awk -v var=`echo \$var_param` 'BEGIN{OFS=\",\"}{print \$1,\$2,\$3,\$4,\$5,\$6,\$7,\$8,\$9,\$10,var}' >> $resultingFile"; 
echo $files | tr ' ' '\n' | xargs -I{} /bin/bash -c "PrintMessageRegionAssignment {} | tail -n+8 | awk -v var=`echo \$var_param2` 'BEGIN{OFS=\",\"}{print \$1,\$2,\$3,\$4,\$5,\$6,\$7,\$8,\$9,\$10,var}' >> $resultingFile"; 

# check mpg tree exist or not by uuid, when does not exist create a new one.
echo "now processing mpg tree!"; 
mpg_flag=$(grep $uuid $mpg_file_dest$UUID_List | wc -l) 
if [[ mpg_flag -eq 0  ]]; then
    echo "create mpg tree"
    new_mpg_name=$(echo "MPG."$uuid"."$ts".tr")
    RALookup_new $head_file getATree $mpg_file_dest$new_mpg_name
    
    # a new MPG tree means a new looked up NS-MPG list (update ns_list content)
    echo "tree lookup to update ns list content"
    last_ns_file=$(ls -ltr $ns_file_source | grep "ns_info" | awk '{print $NF}' | sort -k1g | tail -1 )
    new_ns_filename=$(echo "ns_mpg."$uuid"."$ts".csv")
    cat $ns_file_source$last_ns_file | /home/testgrp/RAAnalysis/bin/TreeToolsUInt lookup -full $mpg_file_dest$new_mpg_name | awk 'BEGIN{OFS=","} {print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > $ns_file_dest$new_ns_filename
    
    # update processed uuid lists
    echo "update uuid list"
    echo $new_mpg_name >> $mpg_file_dest$UUID_List
fi;
done;

rm /home/testgrp/RAAnalysis/ra_data/ra_msg/assignments_agg/Mapper.1.MAPMON.*

