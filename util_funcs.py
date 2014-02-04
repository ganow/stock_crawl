#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime


def print_data(data):
    print '{'
    for k,v in data.iteritems():
        print '\t%s: %s\t(%s),' % (k, v, v.__class__)
    print '}'


def get_fname(offset, date):
    return os.path.join(offset, date.strftime('%Y-%m-%d') + '.csv')


def get_days_list(s_date, e_date):
    one_day = datetime.timedelta(1)
    d = s_date
    output = []
    while d != e_date + one_day:
        output.append(d)
        d += one_day
    return output
