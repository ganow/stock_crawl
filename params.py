#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'sqlite/stock.db')
DB_TEST_FILE = os.path.join(BASE_DIR, 'sqlite_test/stock.db')
SJIS_CSV_DIR = os.path.join(BASE_DIR, 'data/')
CSV_DIR = os.path.join(BASE_DIR, 'data_utf/')
