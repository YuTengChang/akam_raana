import os,sys
import subprocess as sp
#sys.path.append('/home/testgrp/perfTMI/perftmi')


def ls_full(dir_name):
    # return list of 2-tuple with (name, timestamp) fromat in HDFS
    ls_list = sp.check_output('hadoop fs -ls %s'%dir_name,
                                shell=True).strip().split('\n')
    ls_list = [(i.rsplit(' ',1)[1],
                i.rsplit(' ',3)[1]+' '+i.rsplit(' ',3)[2])
                for i in ls_list[1:] ]
    return ls_list


def ls(dir_name):
    # return list of names in HDFS
    ls_list = sp.check_output('hadoop fs -ls %s'%dir_name,
                                shell=True).strip().split('\n')
    ls_list = [i.rsplit(' ',1)[1] for i in ls_list[1:]]
    return ls_list


def mkdir(dir_name):
    # make directory in HDFS, abort when folder exists
    if sp.call('hadoop fs -test -d %s'%dir_name, shell=True):
        return sp.check_call('hadoop fs -mkdir -p %s'%dir_name,shell=True)
    else:
        return 'HDFS destination folder exists and abort'

def put(here,there):
    # upload file to HDFS
    return sp.check_call('hadoop fs -put %s %s'%(here,there),shell=True)

def cp(source, target):
    # copy source HDFS FILE to target HDFS DIRECTORY, make directory if needed
    if sp.call('hadoop fs -test -d %s'%target, shell=True):
        mkdir(target)
    return sp.check_call('hadoop fs -cp %s %s'%(source,target), shell=True)


def rm(pth_to_rm,r=False):
    #
    if r:
        return sp.check_call('hadoop fs -rm -r %s'%pth_to_rm,shell=True)
    else:
        return sp.check_call('hadoop fs -rm %s'%pth_to_rm,shell=True)


def getmerge(input_dir,out_path):

    return sp.check_call('hadoop fs -getmerge %s %s'%(input_dir,out_path),
                        shell=True)
