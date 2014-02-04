#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import datetime

import urllib2

from params import *

one_day = datetime.timedelta(1)

# ex) http://k-db.com/site/download.aspx?p=all&download=csv&date=2013-12-27

base_url = 'http://k-db.com/site/download.aspx?p=all&download=csv&date='

data_dir = './data/'


def main(start_day, end_day):
    d = start_day
    while d != end_day+one_day:

        if os.path.exists(os.path.join(SJIS_CSV_DIR, d.strftime('%Y-%m-%d')+'.csv')):
            # すでにファイル持ってたら取りに行かない
            d += one_day
            continue

        url = base_url + '%s-%s-%s' % (d.year, d.month, d.day)
        print 'get', d, 'url:', url
        page = urllib2.urlopen(url)

        f = open(data_dir + d.strftime('%Y-%m-%d') + '.csv', 'w')
        f.writelines(page.readlines())
        f.close()

        d += one_day
        time.sleep(1)


if __name__ == '__main__':

    ###########################################
    ### finished @ 2014/01/04               ###
    ### from datetime.date(2013, 1, 1)      ###
    ### to datetime.date(2014, 1, 2)        ###
    ###########################################

    start_day = datetime.date(2013, 1, 1)
    end_day = datetime.date(2013, 11, 1)

    main(start_day, end_day)
