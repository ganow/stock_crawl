#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from experiment_base import Experiment

from params import *

"""

TOPIX以外の企業数: 29
考慮する期数: 1

"""


def main():
    e = Experiment()
    e.run(29, 1, save_dir=os.path.join(BASE_DIR, 'img/experiment_001/'))

if __name__ == '__main__':
    main()
