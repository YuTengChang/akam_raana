#!/usr/bin/python

''' add header fields to raw tsv rows and make it a csv '''

from __future__ import print_function, division
import sys, os
from glob import glob

IN_DIR = '/home/testgrp/ksprong/tmp/mapmon/tsv/'
OUT_DIR = '/home/testgrp/ksprong/tmp/mapmon/csv/'

def transform_tsv(fn):
    with open(IN_DIR + fn) as filein, open(OUT_DIR + fn, 'w') as fileout:
        # get header fields
        filein.readline()
        mpd_uuid = filein.readline().strip().split(':')[1].strip()
        filein.readline()
        t_st = filein.readline().strip().split(':')[1].strip()
        t_end = filein.readline().strip().split(':')[1].strip()
        filein.readline()

        static_header = ','.join(['', 't_st', 't_end', 'mpd_uuid'])
        static_vals = ','.join(['', t_st, t_end, mpd_uuid])
        # write header
        print(','.join(filein.readline().strip().split('\t')) + static_header)

        # loop over the rest
        for line in filein:
            if line[0:3] == 'mpg':
                continue
            fileout.write(','.join(line.strip().split('\t')) + static_vals + '\n')


def main():
    ts = sys.argv[1]
    for fn in glob(IN_DIR + ts + '*'):
        transform_tsv(fn.split('/')[-1])


if __name__ == '__main__':
    main()



