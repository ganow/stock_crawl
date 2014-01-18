#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest, os

from translate_to_db import (
    set_up,
    parse_raw_text,
    get_market,
    get_industory,
    get_brand,
    store_day_chart,
)

from util_funcs import print_data

from model import (
    BASE_DIR,
    CSV_DIR
)

from model import (
    init,
    Brand,
    MarketType,
    IndustoryType,
    DayChart,
)
from model import database_proxy as db


class TestTranslate(unittest.TestCase):

    def setUp(self):
        init(
            MODE = 'DEBUG',
            DROP_DB = True,
            CREATE_DB = True
        )
        db.connect()
        self.fnames = os.listdir(CSV_DIR)

    def test_main(self):
        fname = self.fnames[0]

        f = open(os.path.join(CSV_DIR, fname), 'r')

        for x,line in enumerate(f):
            if 2 <= x <= 100:
                try:
                    print_data(parse_raw_text(line))
                except Exception, e:
                    print line
                    raise e

if __name__ == '__main__':
    unittest.main()