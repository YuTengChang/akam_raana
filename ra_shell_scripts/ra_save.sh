#!/bin/bash
# this script check existence of the RA file and move them to temporary folder with timestamp appended to the file name
ra_temp_folder="/home/testgrp/RAAnalysis/ra_data/ra_msg/assignments_agg/"

# file #1
# get the time
ts_ra=$(PrintMessageRegionAssignment /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.1 | head -10 | grep 'start_time' | awk '{print $2}')
dest="$ra_temp_folder$ts_ra"

# check if the folder exists in temporary folder, if not, create one and copy this file into that folder
if [ ! -d "$dest" ]; then
  mkdir $ra_temp_folder$ts_ra;
  ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.1 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
else # if folder exist, check if this file has been added, if not, add it.
  if [ ! -f "$dest/Mapper.1.MAPMON.Assignments.$ts_ra.1" ]; then
    ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.1 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
  fi
fi

# file #2
# get the time
ts_ra=$(PrintMessageRegionAssignment /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.2 | head -10 | grep 'start_time' | awk '{print $2}')
dest="$ra_temp_folder$ts_ra"

# check if the folder exists in temporary folder, if not, create one and copy this file into that folder
if [ ! -d "$dest" ]; then
  mkdir $ra_temp_folder$ts_ra;
  ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.2 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
else # if folder exist, check if this file has been added, if not, add it.
  if [ ! -f "$dest/Mapper.1.MAPMON.Assignments.$ts_ra.2" ]; then
    ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.2 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
  fi
fi


# file #3
# get the time
ts_ra=$(PrintMessageRegionAssignment /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.3 | head -10 | grep 'start_time' | awk '{print $2}')
dest="$ra_temp_folder$ts_ra"

# check if the folder exists in temporary folder, if not, create one and copy this file into that folder
if [ ! -d "$dest" ]; then
  mkdir $ra_temp_folder$ts_ra;
  ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.3 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
else # if folder exist, check if this file has been added, if not, add it.
  if [ ! -f "$dest/Mapper.1.MAPMON.Assignments.$ts_ra.3" ]; then
    ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.3 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
  fi
fi

# file #4
# get the time
ts_ra=$(PrintMessageRegionAssignment /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.4 | head -10 | grep 'start_time' | awk '{print $2}')
dest="$ra_temp_folder$ts_ra"

# check if the folder exists in temporary folder, if not, create one and copy this file into that folder
if [ ! -d "$dest" ]; then
  mkdir $ra_temp_folder$ts_ra;
  ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.4 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
else # if folder exist, check if this file has been added, if not, add it.
  if [ ! -f "$dest/Mapper.1.MAPMON.Assignments.$ts_ra.4" ]; then
    ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.4 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
  fi
fi


# file #5
# get the time
ts_ra=$(PrintMessageRegionAssignment /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.5 | head -10 | grep 'start_time' | awk '{print $2}')
dest="$ra_temp_folder$ts_ra"

# check if the folder exists in temporary folder, if not, create one and copy this file into that folder
if [ ! -d "$dest" ]; then
  mkdir $ra_temp_folder$ts_ra;
  ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.5 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
else # if folder exist, check if this file has been added, if not, add it.
  if [ ! -f "$dest/Mapper.1.MAPMON.Assignments.$ts_ra.5" ]; then
    ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.5 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
  fi
fi


# file #6
# get the time
ts_ra=$(PrintMessageRegionAssignment /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.6 | head -10 | grep 'start_time' | awk '{print $2}')
dest="$ra_temp_folder$ts_ra"

# check if the folder exists in temporary folder, if not, create one and copy this file into that folder
if [ ! -d "$dest" ]; then
  mkdir $ra_temp_folder$ts_ra;
  ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.6 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
else # if folder exist, check if this file has been added, if not, add it.
  if [ ! -f "$dest/Mapper.1.MAPMON.Assignments.$ts_ra.6" ]; then
    ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.6 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
  fi
fi


# file #7
# get the time
ts_ra=$(PrintMessageRegionAssignment /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.7 | head -10 | grep 'start_time' | awk '{print $2}')
dest="$ra_temp_folder$ts_ra"

# check if the folder exists in temporary folder, if not, create one and copy this file into that folder
if [ ! -d "$dest" ]; then
  mkdir $ra_temp_folder$ts_ra;
  ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.7 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
else # if folder exist, check if this file has been added, if not, add it.
  if [ ! -f "$dest/Mapper.1.MAPMON.Assignments.$ts_ra.7" ]; then
    ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.7 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
  fi
fi


# file #8
# get the time
ts_ra=$(PrintMessageRegionAssignment /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.8 | head -10 | grep 'start_time' | awk '{print $2}')
dest="$ra_temp_folder$ts_ra"

# check if the folder exists in temporary folder, if not, create one and copy this file into that folder
if [ ! -d "$dest" ]; then
  mkdir $ra_temp_folder$ts_ra;
  ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.8 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
else # if folder exist, check if this file has been added, if not, add it.
  if [ ! -f "$dest/Mapper.1.MAPMON.Assignments.$ts_ra.8" ]; then
    ls /a/etc/ddr/mdt/Mapper.1.MAPMON.Assignments.8 | tr ' ' '\n' | xargs -I{} /bin/bash -c "fname=\$(echo {} | awk -v var=`echo \$ts_ra` -F\".\" '{print \"Mapper.\"\$2\".\"\$3\".\"\$4\".\"var\".\"\$5}'); echo \$fname; cp {} `echo \$dest/`\$fname";
  fi
fi
