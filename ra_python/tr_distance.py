#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 15:58:55 2015

@author: ychang

This script do the distance calculation

"""
import sys,os
sys.path.append('/home/testgrp/RAAnalysis/')
import math

#R = 3963.1676
R = 6371
pi = 3.141592653
lat1 = 40.0
lon1 = -70.0

for line in sys.stdin:
    # anything passed into the streaming is a tab-separate string
    line_str = line.strip().split('\t')
    (region, ecor, service, rg_name, nghost, prp, latitude, longitude, datestamp) = line_str


    lat2 = float(latitude)
    lon2 = float(longitude)

    lat1r = math.radians(lat1)
    lat2r = math.radians(lat2)
    lon1r = math.radians(lon1)
    lon2r = math.radians(lon2)

    #print 'lat2=%s, lat2r=%s' % (str(lat2), str(lat2r))

    dlat = abs(lat2r - lat1r)/2
    dlon = abs(lon2r - lon1r)/2

    a = math.pow(math.sin(dlat),2) + math.cos(lat2r) * math.cos(lat1r) * math.pow(math.sin(dlon),2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    print '\t'.join([str(region),
                     str(ecor),
                     service,
                     rg_name,
                     str(nghost),
                     str(prp),
                     str(latitude),
                     str(longitude),
                     str( round(R*c,3) )])
