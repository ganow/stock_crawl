#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
import datetime

one_day = datetime.timedelta(1)

import crawl
import translate_to_utf
import translate_to_db


def main(start_day, end_day):
    print u"%s から %s までのデータのクロールを開始します。" % ( start_day.strftime('%Y-%m-%d'), end_day.strftime('%Y-%m-%d') )
    crawl.main(date(2010, 3, 27), date(2010, 3, 27))
    print u"取得したデータの文字コードの変換を開始します。"
    translate_to_utf.main()
    print u"%s から %s までのデータのデータベースへの保存を開始します。" % ( start_day.strftime('%Y-%m-%d'), end_day.strftime('%Y-%m-%d') )
    translate_to_db.set_up()
    translate_to_db.main(date(2010, 3, 27), end_day)

if __name__ == '__main__':

    # 2014/01/18の時点で
    # 2012-01-01 から 2014-01-02 まで終了

    start_day = date(2010, 1, 1)
    end_day = date(2012, 1, 1) - one_day

    main(start_day, end_day)
