#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pylab as pl
import matplotlib.dates as dates
from scipy import stats

import datetime
from datetime import date

from sklearn.linear_model import BayesianRidge, LinearRegression

from convert_data import get_data, get_brands_value_list
from util_funcs import get_days_list

font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 16}
pl.rc('font', **font)

one_day = datetime.timedelta(1)

def plot_value(brand, attr, start_day=date(2013,1,1), end_day=date(2014,1,1)):
    data = get_brands_value_list(brand, attr, start_day, end_day)

    days = get_days_list(start_day, end_day)

    pl.figure(figsize=(6, 5))
    pl.title("Value Fluctuation Value: %s" % attr)

    pl.plot(days, data, 'b-', lw=2)

    pl.ylabel(attr)
    pl.show()

def compute_sqerr(lhs, rhs):
    sqerr = ( lhs - rhs ) ** 2
    sqerrsum = sqerr.sum()
    return sqerr, sqerrsum

def save_or_show(fname, pl, save_dir):
    if save_dir:
        pl.savefig(os.path.join(save_dir, fname))
    else:
        pl.show()

class Regressor(object):
    def __init__(self, target, competitors, start_day, end_day, t_step, attr='max_value'):
        super(Regressor, self).__init__()

        self.target = target
        self.competitors = competitors
        self.start_day = start_day
        self.end_day = end_day
        self.t_step = t_step
        self.attr = attr

        self.clf = BayesianRidge(compute_score=True)
        self.ols = LinearRegression()

    def get_data(self, start_day=None, end_day=None, update_self=False):
        if not start_day: start_day = self.start_day
        if not end_day: end_day = self.end_day

        X, y, competitors = get_data(
            self.target,
            self.competitors,
            start_day,
            end_day,
            self.t_step,
            self.attr )
        if update_self:
            self.X = X
            self.y = y
            self.competitors = competitors
            return
        else:
            return X, y

    def train(self):
        print u"ベイズ線形回帰の計算開始..."
        self.clf.fit(self.X, self.y)
        print u"線形回帰の計算開始..."
        self.ols.fit(self.X, self.y)

    def test(self, test_start_day, test_end_day):

        self.test_start_day = test_start_day
        self.test_end_day = test_end_day
        test_X, test_y = self.get_data(test_start_day - datetime.timedelta(self.t_step), test_end_day)

        self.test_y = test_y

        self.predicted_by_bayes = self.clf.decision_function(test_X)
        self.predicted_by_linear = self.ols.decision_function(test_X)

        self.bayes_sqerr, self.bayes_sqerrsum = compute_sqerr(self.predicted_by_bayes, test_y)
        self.linear_sqerr, self.linear_sqerrsum = compute_sqerr(self.predicted_by_linear, test_y)

    def plot_weight(self, save_dir=None):
        pl.figure(figsize=(6, 5))
        pl.title("Weights of the model")
        pl.plot(self.clf.coef_, 'b-', label="Bayesian Ridge estimate", lw=3)

        span = pl.ylim()[1] - pl.ylim()[0]
        pl.ylim( pl.ylim()[0] - span*0.1, pl.ylim()[1] + span*0.1 )

        pl.plot(self.ols.coef_, 'r--', label="OLS estimate")

        pl.xlabel("Features")
        pl.ylabel("Values of the weights")
        pl.legend(loc="best", prop=dict(size=12))

        save_or_show('weight.pdf', pl, save_dir)

    def plot_log_likelihood(self, save_dir=None):
        pl.figure(figsize=(6, 5))
        pl.title("Marginal log-likelihood")
        pl.plot(self.clf.scores_)
        pl.ylabel("Score")
        pl.xlabel("Iterations")

        save_or_show('log_likelihood.pdf', pl, save_dir)

    def plot_forecast(self, save_dir=None):

        predicted_by_bayes = self.predicted_by_bayes
        predicted_by_linear = self.predicted_by_linear

        test_start_day = self.test_start_day
        test_end_day = self.test_end_day

        test_y = self.test_y

        train_days = get_days_list(self.start_day+datetime.timedelta(self.t_step), self.end_day)
        test_days = get_days_list(test_start_day, test_end_day)

        pl.figure(figsize=(10, 5))
        pl.title("Value forecasting")

        pl.plot(train_days, self.y, 'g-', lw=2, label="Trained Data")
        pl.plot(test_days, test_y, 'g-', lw=2, label="Actual Data")

        pl.plot(test_days, predicted_by_bayes, 'b-', lw=3, label="Predicted by Bayes")

        span = pl.ylim()[1] - pl.ylim()[0]
        pl.ylim( pl.ylim()[0] - span*0.1, pl.ylim()[1] + span*0.1 )

        pl.plot(test_days, predicted_by_linear, 'r--', lw=2, label="Predicted by Linear")

        ax = pl.gca()
        ax.xaxis.set_major_locator(dates.DayLocator(interval=60)) #主目盛を日単位で60日間隔で表示
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=30)) #補助目盛を日単位で30日間隔で表示
        ax.xaxis.set_major_formatter(dates.DateFormatter('%d%b\n%Y')) #主目盛のラベルの表示形式を指定

        pl.ylabel(self.attr)
        pl.legend(loc='best', prop=dict(size=12))

        save_or_show('forecast.pdf', pl, save_dir)

    def plot_sqerr(self, save_dir=None):

        test_days = get_days_list(self.test_start_day, self.test_end_day)

        pl.figure(figsize=(10, 5))
        pl.title("Squared Error")

        pl.plot(test_days, self.bayes_sqerr, 'b-', lw=2, label="Bayes(Sum:%0.2f)" % self.bayes_sqerrsum)
        pl.plot(test_days, self.linear_sqerr, 'r-', lw=2, label="Linear(Sum:%0.2f)" % self.linear_sqerrsum)

        ax = pl.gca()
        ax.xaxis.set_major_locator(dates.DayLocator(interval=60)) #主目盛を日単位で60日間隔で表示
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=30)) #補助目盛を日単位で30日間隔で表示
        ax.xaxis.set_major_formatter(dates.DateFormatter('%d%b\n%Y')) #主目盛のラベルの表示形式を指定

        pl.ylabel("Squared Error")
        pl.legend(loc='best', prop=dict(size=12))

        save_or_show('sqerr.pdf', pl, save_dir)

