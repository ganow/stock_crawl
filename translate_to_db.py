#!/usr/bin/env python
# -*- coding: utf-8 -*-

from params import *

from datetime import date, timedelta, datetime

from model import (
    init,
    Brand,
    MarketType,
    IndustoryType,
    DayChart,
)
from model import database_proxy as db

from util_funcs import print_data, get_fname

# データのアライン
# コード,銘柄名,市場,業種,始値,高値,安値,終値,出来高,売買代金
# 0     1     2   3   4   5   6   7   8     9


def parse_raw_text(raw_text):
    tmp = raw_text.rstrip().split(',')
    return {
        'code': tmp[0],
        'brand_name': tmp[1],
        'market_name': tmp[2],
        'industory_name': tmp[3],
        'start_value': None if tmp[4] == '-' else float(tmp[4]),
        'max_value': None if tmp[5] == '-' else float(tmp[5]),
        'min_value': None if tmp[6] == '-' else float(tmp[6]),
        'end_value': None if tmp[7] == '-' else float(tmp[7]),
        'turnover': None if tmp[8] == '-' else float(tmp[8]),
        'sales_value': None if tmp[9] == '-' else float(tmp[9])
    }


def get_market(data):
    try:
        market = MarketType.get(MarketType.type_name == data['market_name'])
    except Exception, e:
        market = MarketType(
            type_name=data['market_name']
        )
        market.save()
    finally:
        return market


def get_industory(data):
    try:
        industory = IndustoryType.get(IndustoryType.type_name == data['industory_name'])
    except Exception, e:
        industory = IndustoryType(
            type_name=data['industory_name']
        )
        industory.save()
    finally:
        return industory


def get_brand(data):
    try:
        brand = Brand.get(Brand.name == data['brand_name'])
    except Exception, e:
        brand = Brand(
            code=data['code'],
            name=data['brand_name'],
            market=get_market(data),
            industory=get_industory(data)
        )
        brand.save()
    finally:
        return brand


def store_day_chart(date, data):
    dc = DayChart(
        brand=get_brand(data),
        start_value=data['start_value'],
        max_value=data['max_value'],
        min_value=data['min_value'],
        end_value=data['end_value'],
        turnover=data['turnover'],
        sales_value=data['sales_value'],
        date=date,
    )
    dc.save()
    return dc


def file_to_db(fname, date):
    with open(fname, 'r') as f:
        for i,line in enumerate(f):
            if i >= 2:
                data = parse_raw_text(line)
                store_day_chart(date, data)

    db.commit()


def set_up():
    init(
        MODE='MYSQL',
        DROP_DB=False,
        CREATE_DB=False
    )
    db.connect()
    db.set_autocommit(False)


# @profile
def main(start_day, end_day):

    one_day = timedelta(1)

    d = start_day
    while d != end_day + one_day:
        print 'file_to_db date:', d.strftime('%Y-%m-%d'), 'start:', datetime.now()
        fname = get_fname(CSV_DIR, d)

        file_to_db(fname, d)

        d += one_day

if __name__ == '__main__':

    ### finished data(sqlite, real)
    ### from 2013-01-01 to 3014-1-2

    ### finished data(mysql, stock)
    ### from 2013-01-01 to 3014-1-2

    start_day = date(2013,1,1)
    end_day = date(2014,1,2)

    set_up()
    main()
