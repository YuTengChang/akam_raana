import os,sys
import subprocess as sp
#sys.path.append('/home/testgrp/perfTMI/perftmi')


def ls(dir_name):

    return sp.check_output('hadoop fs -ls %s'%dir_name,shell=True)


def ls_list(dir_name):

    ls_list = sp.check_output('hadoop fs -ls %s'%dir_name,
                                shell=True).strip().split('\n')
    ls_list = [i.rsplit(' ',1)[1] for i in ls_list[1:]]
    return ls_list


def mkdir(dir_name):

    return sp.check_call('hadoop fs -mkdir %s'%dir_name,shell=True)

def put(here,there):

    return sp.check_call('hadoop fs -put %s %s'%(here,there),shell=True)

def rm(pth_to_rm,r=False):

    if r:
        return sp.check_call('hadoop fs -rm -r %s'%pth_to_rm,shell=True)
    else:
        return sp.check_call('hadoop fs -rm %s'%pth_to_rm,shell=True)


def getmerge(input_dir,out_path):

    return sp.check_call('hadoop fs -getmerge %s %s'%(input_dir,out_path),
                        shell=True)
