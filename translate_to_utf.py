#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time


def main():

    data_dir = './data/'
    out_dir = './data_utf/'

    target = set(os.listdir(data_dir)) - set(os.listdir(out_dir))

    for i, csv_file in enumerate( target ):
        print str(i+1) + '/' + str(len(target)), 'translate', csv_file, 'input:', data_dir, 'output:', out_dir
        os.system('nkf -u ' + data_dir + csv_file + ' > ' + out_dir + csv_file)
        time.sleep(0.1)

if __name__ == '__main__':
    main()
