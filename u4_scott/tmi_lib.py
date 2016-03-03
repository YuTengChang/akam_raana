#!/a/bin/python2.7

import sys,os
import subprocess as sp
sys.path.append('/home/testgrp/perfTMI/perftmi')
import etc.config as config
import time,datetime
import threading


#### call to get the partitions for a table in the perftmi database


def get_existing_partitions(tablename):

    ex_parts=hive_output('show partitions %s'%tablename)
    if ex_parts == '':
        ex_parts_list = [] 
    else:
        ex_parts_list=[i.split('=')[1] for i in ex_parts.strip().split('\n')] 
        
    return map(int,ex_parts_list)


#### save a list of exising partition somewhere

def save_existing_partitions(tablename,filename):

    with open(filename,'w') as f:
        sp.check_call([config.hive,'-e','use perftmi; show partitions %s;'%tablename],stdout=f)


####


#### remove a partition from a table

def remove_partition(tablename,partition_name,partition_value):
    hql_str = 'alter table %s drop partition(%s=%s);'%(tablename,partition_name,partition_value)
    hive_call(hql_str)

    return


def add_partition(tablename,partition_name,partition_value):

    hql_str = 'alter table %s add partition(%s=%s);'%(tablename,partition_name,partition_value)
    hive_call(hql_str)
    return 

#### call to mail program


def send_mail(dest_address,subject,message):

    p1 = sp.Popen(['echo',message],stdout=sp.PIPE)
    p2 = sp.Popen(['mail','-s',subject,dest_address],stdin=p1.stdout)

    p2.communicate()

    return


#### convert between partition startdate format for pipeline and
#### python datetime object


def startdate_to_datetime(startdate_string):

    dte_tme = datetime.datetime.strptime(startdate_string,'%Y%m%d%H')
    return dte_tme

def datetime_to_startdate(datetime_object):

    return '%s%s%s%s'%(
        str(datetime_object.year),
        str(datetime_object.month).zfill(2),
        str(datetime_object.day).zfill(2),
        str(datetime_object.hour).zfill(2))

def convert_to_timestamp(startdate):

    dt = datetime.datetime.strptime(repr(startdate),'%Y%m%d%H')
    ts = (dt - datetime.datetime(1970,1,1)).total_seconds()
    return int(ts) 


#### make a call to hive #####


def hive_call(hql_str):
    
    hql_full_str = 'use perftmi; add jar %s; '%config.ddrjar + hql_str
    print hql_full_str
    try:
        sp.check_call([config.hive,'-e',hql_full_str])

    except sp.CalledProcessError:

        raise HiveError

    return


def hive_call2(hql_str):
    ''' same as above but w/o use perftmi;''' 
    hql_full_str = 'add jar %s;'%config.ddrjar + hql_str 
    try:
        sp.check_call([config.hive,'-e',hql_full_str])
    except sp.CalledProcessError:
        raise HiveError
    return 


def hive_call2compress(hql_str,file2save):

    hql_full_str = 'add jar%s;'%config.ddrjar + hql_str

    try:
        sp.check_call('hive -e %s | gzip > %s'%(
            hql_full_str,file2save))

    except sp.CalledProcessError:
        raise HiveError
    
    return 


def hive_output(hql_str):
 
    hql_full_str = 'use perftmi; add jar %s; '%config.ddrjar + hql_str
    print hql_full_str

    if not os.path.isfile(config.hive):
        print "%s does not exist"%config.hive

    
    try:
        str_out  = sp.check_output([config.hive,'-e',hql_full_str])
        return str_out

    except sp.CalledProcessError:

        raise HiveError

    return


##### some helpers function

def fence_ppreply(startdate):

    pp_parts = get_existing_partitions('ppreply')
    #executive decision -- include all ppl messages within the last hour
    ts = convert_to_timestamp(startdate)
    pp_parts_inc = [i for i in pp_parts if i > ts - 3601]

    return (min(pp_parts_inc),max(pp_parts_inc))


##### subprocess timeout for Spark timeouts

class Command(object):
    def __init__(self,cmd):
        self.cmd = cmd
        self.process = None
    def run(self,timeout):
        def target():
            self.process = sp.Popen(self.cmd,shell=True)
            self.process.communicate()
        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
        return self.process.returncode

     
##### some Exceptions #####


class HiveError(Exception):
    def __init__(self):
        self.message = 'Unable to complete query, check Syntax'

 
    
