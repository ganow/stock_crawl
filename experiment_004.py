#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from experiment_base import Experiment

from params import *

"""

TOPIX以外の企業数: 3
考慮する期数: 60

"""


def main():
    e = Experiment()
    e.run(30, 60, save_dir=os.path.join(BASE_DIR, 'img/experiment_004/'))

if __name__ == '__main__':
    main()
