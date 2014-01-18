#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import random

from datetime import date
from model import (
    init,
    Brand,
    MarketType,
    IndustoryType,
    DayChart,
)
from model import database_proxy as db

class TestModel(unittest.TestCase):

    def setUp(self):
        init(
            MODE = 'DEBUG',
            DROP_DB = True,
            CREATE_DB = True
        )
        db.connect()
        db.set_autocommit(False)

        self.Models = (MarketType, IndustoryType, Brand, DayChart)

    def test_main(self):

        for M in self.Models:
            self.assertEqual(0, M.select().count())

        test_market_types = (
            u'東証',
            u'東証夜間'
        )

        mts = []
        for mt_name in test_market_types:
            mts.append( MarketType(type_name=mt_name) )

        for obj in mts:
            obj.save()
        self.assertEqual(len(mts), MarketType.select().count())


        test_industory_types = (
            u'指数',
            u'先物',
            u'その他'
        )

        its = []
        for it_name in test_industory_types:
            its.append( IndustoryType(type_name=it_name) )

        for obj in its:
            obj.save()
        self.assertEqual(len(its), IndustoryType.select().count())

        test_brands = (
            u'大日本印刷',
            u'電通',
            u'Google'
        )

        brands = []
        for i, b_name in enumerate(test_brands):
            brands.append( Brand(
                code = i,
                name = b_name,
                market = random.choice(mts),
                industory = random.choice(its)
            ) )

        for obj in brands:
            obj.save()
        self.assertEqual(len(brands), Brand.select().count())

        day_charts = []
        for i in xrange(1,100):
            day_charts.append( DayChart(
                brand = random.choice(brands),
                start_value = random.random() * 100,
                end_value = random.random() * 100,
                max_value = random.random() * 100,
                date = date.today()
            ) )

        for obj in day_charts:
            obj.save()
        self.assertEqual(len(day_charts), DayChart.select().count())

        db.commit()

        self.assertEqual(1, Brand.select().where(
            Brand.name==test_brands[2]).count())
        self.assertEqual(1, MarketType.select().where(
            MarketType.type_name==test_market_types[0]).count())
        self.assertEqual(0, IndustoryType.select().where(
            IndustoryType.type_name==test_industory_types[0]+'hoge').count())

if __name__ == '__main__':
    unittest.main()

