#!/bin/bash
echo "***************************************"
echo " startime(UTC): " `date -u`
echo "***************************************"

echo "SSH_AUTH_SOCK" $SSH_AUTH_SOCK
echo "SSH_AGENT_PID" $SSH_AGENT_PID
echo "USER" $USER

filename=`ls -ltr /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ra_data/ns_info/ | tail -1 | awk '{print $NF}'`
echo $filename
ddc_datanode="23.3.136.55"
scp -Sgwsh /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ra_data/ns_info/$filename testgrp@$ddc_datanode:/home/testgrp/RAAnalysis/ra_data/ns_info/

rsync -r -v --exclude="*.tmp" --exclude="bin" --exclude="ra_data/ra_msg" -e gwsh /home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis/ $ddc_datanode:/home/testgrp/RAAnalysis/
