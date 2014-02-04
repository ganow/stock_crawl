#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from experiment_base import Experiment

from params import *

"""

TOPIX以外の企業数: 2
考慮する期数: 30

※ TOPIXを対象から外す

"""


def main():
    e = Experiment()
    e.run(2, 30, save_dir=os.path.join(BASE_DIR, 'img/experiment_006/'), exclude_TOPIX=True)

if __name__ == '__main__':
    main()
