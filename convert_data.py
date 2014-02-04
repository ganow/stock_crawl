#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import datetime

from scipy.interpolate import UnivariateSpline

from model import (
    Brand,
    DayChart,
)


def get_data(target, competitors, start_day, end_day, t_step=1, attr='max_value', verbose=False):
    """
    線形回帰のためのデータをモデルから取得する関数
    入力として
        - 回帰で予測したい会社
        - 予測に使用する競合のリスト
        - 取得期間のための開始日，終了日
    を引数に取ることで，
        - ( 取得期間-ステップ数 ) x ( (ターゲット+競合の会社数)xステップ数 ) の行列
        - ( 取得期間-ステップ数 ) のベクトル
    の二つを返す．それぞれ回帰で使用するX,yに当たる．

    オプションとして
        - t_step
        - attr
    を取れる．
    t_stepは何期まえまでを特徴次元数として含めるか
    attrは取得する値を何にするか
    """

    target_data = get_brands_value_list(target, attr, start_day, end_day)
    competitors_data = [] # 会社数 x 取得期間の行列
    used_competitors = []
    for i, c in enumerate(competitors):
        try:
            # 全てが欠損となってしまうようなブランドのデータを突っ込んでしまった時はその特徴量を捨てる
            competitors_data.append(get_brands_value_list(c, attr, start_day, end_day))
            if verbose:
                print u'%d: %s(id:%d)のデータを取得しました。' % (i, c.name, c.id)
            used_competitors.append(c)
        except Exception, e:
            print u'%s(id:%d)のデータは全て欠損だったため破棄しました。' % (c.name, c.id)
            # raise e

    # competitors_data = np.array(competitors_data)

    # print competitors_data.shape

    # days = (end_day - start_day).days + 1

    X = get_value_matrix(target_data, t_step)
    for i, c_data in enumerate(competitors_data):
        X = np.vstack((X, get_value_matrix(c_data, t_step)))

    y = target_data[t_step:]

    return X.T, y, used_competitors


def get_value_matrix(brand_data, t_step):
    """
    一社に対して，考慮する期数 x (期間-考慮する期数)
    """
    size = brand_data.size
    idx_matrix = get_idx_matrix(t_step, size-t_step)
    return brand_data[idx_matrix]


def get_idx_matrix(t, n):
    """
    t x nの行列を得るための関数
    一列目は0~t-1までiteration
    二列目は1~t-1までiteration
    ...
    n列目はn~n+t-1までiteration
    """

    t_iter_matrix = np.repeat( np.arange(t).reshape(t,1), n, axis=1 )
    n_iter_matrix = np.repeat( np.arange(n).reshape(1,n), t, axis=0 )
    return t_iter_matrix + n_iter_matrix


def get_brands_value_list(brand, attr, start_day, end_day):
    """
    指定期間内の特定のブランドの価格リストを取得する関数
    時々データの日付が飛ぶことがある
    -> スプライン補間
    """

    output = get_brands_raw_value_list(brand, attr, start_day, end_day)
    idx_array = np.arange(output.size)
    try:
        # 全てが欠損のデータに関してエラーが出る
        f = UnivariateSpline(idx_array[output!=-1], output[output!=-1])
    except Exception, e:
        raise e
    return f(idx_array)


def get_brands_raw_value_list(brand, attr, start_day, end_day):
    """
    欠損を補完しないデータの取得
    """

    data = DayChart.select().join(Brand).where(
        (Brand.id == brand.id) &
        (DayChart.date.between(start_day, end_day)) )

    output = np.zeros( (end_day-start_day).days + 1 )

    one_day = datetime.timedelta(1)
    d = start_day
    i = 0
    while d != end_day + one_day:
        try:
            tmp = data.where(DayChart.date == d).get().__getattribute__(attr)
            assert tmp is not None, "missing value"
            output[i] = tmp
        except Exception, e:
            output[i] = -1
            # raise e
        d += one_day
        i += 1
    return output
