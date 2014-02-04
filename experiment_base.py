#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from bayes_regression import Regressor
from datetime import date

from model import (
    init,
    Brand,
    IndustoryType,
)
from model import database_proxy as db


"""

日本オラクルの株価変動をそれ以外の情報通信業+TOPIXから予測する

除外銘柄は EXCEPTION_ID_LIST にて示す
除外理由: 欠損値ばっかりだから(というか途中で消えてるっぽい？)

使用する企業数を多い・少ない
考慮する期数を多い・少ない

でそれぞれ実験してフィットがどう出るか検証

それぞれの線形回帰についても同様に評価

"""

EXCEPTION_ID_LIST = [
    3902,
    3904,
    3906,
    3907,
    3908,
    3910,
    3912,
    3913,
    3922,
    3981,
    3982,
    4011,
    4013,
    4014 ]


class Experiment(object):
    def __init__(self, evaluate_value='max_value'):
        super(Experiment, self).__init__()
        self.evaluate_value = evaluate_value
        self.setup()

    def setup(self):
        print u"実験のセットアップを開始します。"
        init(
            MODE='MYSQL',
            DROP_DB=False,
            CREATE_DB=False
        )
        db.connect()

        # 情報通信の方々+TOPIXのみ取得(除外リストを除く)
        expression = (IndustoryType.id == 12)
        expression = (expression) & ( Brand.name != u"日本オラクル" )
        for exception_id in EXCEPTION_ID_LIST:
            expression = expression & ( Brand.id != exception_id )
        self.master_brands = Brand.select().join(IndustoryType).where(expression)

    def run(self, company_num, t_step, save_dir=None, exclude_TOPIX=False):
        self.brand_list = np.hstack((
            [Brand.get(Brand.name == 'TOPIX')],
            np.random.choice(self.master_brands[0:], company_num) ))
        if exclude_TOPIX:
            self.brand_list = self.brand_list[1:]

        start_day = date(2013, 1, 1)
        end_day = date(2013, 8, 31)
        test_start_day = date(2013, 9, 1)
        test_end_day = date(2013, 12, 31)

        target = Brand.get(Brand.name == u"日本オラクル")

        r = Regressor(target, self.brand_list, start_day, end_day, t_step, self.evaluate_value)
        r.get_data(update_self=True)

        print u"回帰式の計算を開始します。"
        r.train()

        print u"テストデータを使った評価を開始します。"
        r.test(test_start_day, test_end_day)

        r.plot_forecast(save_dir)
        r.plot_weight(save_dir)
        r.plot_log_likelihood(save_dir)
        r.plot_sqerr(save_dir)
