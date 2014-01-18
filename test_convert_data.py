#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import random
import numpy as np

from datetime import date
from model import (
    init,
    Brand,
    MarketType,
    IndustoryType,
    DayChart,
)
from model import database_proxy as db
from convert_data import get_data, get_brands_value_list, get_idx_matrix, get_value_matrix

class TestModel(unittest.TestCase):

    def setUp(self):
        init(MODE = 'MYSQL', DROP_DB = False, CREATE_DB = False)
        db.connect()
        self.s_date = date(2013, 1, 1)
        self.e_date = date(2013, 2, 1)

    def test_get_brands_value_list(self):
        s_date = self.s_date
        e_date = self.e_date

        topix = Brand.get(Brand.name == "TOPIX")
        data = get_brands_value_list(topix, 'max_value', s_date, e_date)
        self.assertEqual((e_date-s_date).days+1, len(data))
        # print data

    def test_get_value_matrix(self):
        idx_matrix = get_idx_matrix(3,5)

        test_matrix = np.array([
            [0, 1, 2, 3, 4],
            [1, 2, 3, 4, 5],
            [2, 3, 4, 5, 6]])

        # print test_matrix == idx_matrix

        data = np.arange(1,10)
        # print get_value_matrix(data, 3)

    # def test_get_data(self):
    #     s_date = self.s_date
    #     e_date = self.e_date

    #     rand_brands = [Brand.get(Brand.id == random.randint(1000+20*i, 1010+20*i)) for i in range(10)]
    #     self.assertEqual(10, len(rand_brands))

    #     # for b in rand_brands:
    #         # print b.name

    #     get_data(rand_brands[0], rand_brands[1:], s_date, e_date)

    def test_time(self):
        s_date = date(2013,1,1)
        e_date = date(2014,1,1)

        brands = Brand.select().join(IndustoryType).where(IndustoryType.id == 12)
        for i, b in enumerate(brands[1:15]):
            print i, 'th brand:', b.name
        get_data(brands[0], brands[1:100], s_date, e_date)

if __name__ == '__main__':
    unittest.main()