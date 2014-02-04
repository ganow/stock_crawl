#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import time

dirs = ['./data/', './data_utf/']
# dirs = ['./tmp/']

for dr in dirs:
    fnames = os.listdir(dr)
    for i, fname in enumerate(fnames):

        tmp_date = datetime.date( *[int(x) for x in fname.split('.')[0].split('-')] )
        new_fname = tmp_date.strftime('%Y-%m-%d') + '.csv'

        if new_fname == fname:
            continue

        print str(i+1) + '/' + str(len(fnames)), 'rename:', fname, 'to:', new_fname, 'dir:', dr

        os.system('mv ' + dr + fname + ' ' + dr + new_fname)
        time.sleep(0.1)
