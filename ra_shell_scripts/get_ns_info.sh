#!/bin/bash
# cron task to query mako and obtain ns information, saved in /home/ychang/Documents/Projects/09-SystemInfo/NS_info/ 

# get time
epochtime=`date +%s`
Year=`date -d @$epochtime -u +%Y`
Month=`date -d @$epochtime -u +%m`
Day=`date -d @$epochtime -u +%d`
Hour=`date -d @$epochtime -u +%H`

# file name
ns_info_file=$(echo "ns_info_"$Year$Month$Day".txt")
#echo $ns_info_file

# file location
ns_info_dir="/home/ychang/Documents/Projects/22-RAAnalysis/RAAnalysis_Data/ns_info/"
#ns_info_dir="/home/ychang/Documents/Projects/09-SystemInfo/NS_info/"
#echo $ns_info_dir

# backup location
bk_dir="/home/ychang/Documents/Projects/09-SystemInfo/NS_info/"
#echo $bk_dir

# grab the file by talking to MAKO from MC2
#/home/ychang/bin/mako -s "select IP, ASNUM, COUNTRY, CONTINENT,LATITUDE, LONGITUDE, PINGPOINT, DEMAND from ns_info where demand>0.1 order by DEMAND DESC" | tail -n+4  > $ns_info_dir$ns_info_file

/home/ychang/bin/mako --csv -s "select nsip, demand, geoid, continent, country, city, ns_lat, ns_lon, ns_asnum, ppip, pp_lat, pp_lon, pp_asnum, ns_pp_dist from (select nsip, demand, geoid, continent, country, city, ns_lat, ns_lon, ns_asnum, nvl(ppip, 'nil') ppip, nvl(pp_lat, 0) pp_lat, nvl(pp_lon, 0) pp_lon, nvl(pp_asnum, 0) pp_asnum, nvl( round(3963.17*atan2(sqrt(alpha),sqrt(1-alpha)),2) , 0) ns_pp_dist from (select a.ip nsip, a.demand demand, power(sin(abs(mod(a.latitude-b.latitude,360))*3.1416/180/2),2) + cos(b.latitude*3.1416/180)*cos(a.latitude*3.1416/180)*power(sin(abs(mod(a.longitude-b.longitude,360))*3.1416/180/2),2) alpha, a.geoid geoid, a.continent continent, a.country country, a.state state, a.city city, a.latitude ns_lat, a.longitude ns_lon, a.asnum ns_asnum, b.ip ppip, b.asnum pp_asnum, b.latitude pp_lat, b.longitude pp_lon from ((select * from ns_info) a left outer join (select * from pp_info) b on a.pingpoint=b.ip) order by demand desc) where demand>0.1)" | tail -n+4 | sed 's/,/ /g' > $ns_info_dir$ns_info_file

# copy file to other location 
cp $ns_info_dir$ns_info_file $bk_dir$ns_info_filg
