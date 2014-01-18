#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import datetime

from scipy.interpolate import UnivariateSpline

from model import (
    init,
    Brand,
    MarketType,
    IndustoryType,
    DayChart,
)
from model import database_proxy as db

def main():
    init(
        MODE = 'MYSQL',
        DROP_DB = False,
        CREATE_DB = False
    )
    db.connect()
    db.set_autocommit(False)

    dq = DayChart.delete().where(
        ( DayChart.start_value >> None ) &
        ( DayChart.end_value >> None ) &
        ( DayChart.max_value >> None ) &
        ( DayChart.min_value >> None ) )
    dq.execute()

    db.commit()

if __name__ == '__main__':
    main()