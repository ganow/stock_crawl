#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import date

from peewee import *

from params import *

database_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = database_proxy

class MarketType(BaseModel):
    type_name = CharField(index=True)

class IndustoryType(BaseModel):
    type_name = CharField(index=True)

class Brand(BaseModel):
    code = CharField(index=True)
    name = CharField(unique=True, index=True)
    market = ForeignKeyField(MarketType, related_name='brands')
    industory = ForeignKeyField(IndustoryType, related_name='brands')

class DayChart(BaseModel):

    brand = ForeignKeyField(Brand, related_name='daycharts')

    start_value = DoubleField(null=True)
    max_value = DoubleField(null=True)
    min_value = DoubleField(null=True)
    end_value = DoubleField(null=True)
    turnover = DoubleField(null=True)
    sales_value = DoubleField(null=True)

    date = DateField(index=True)

def _create_table():

    Models = ( MarketType, IndustoryType, Brand, DayChart )

    for M in Models:
        try:
            M.create_table()
        except OperationalError, e:
            print e
            # raise e

def init(MODE='DEBUG', DROP_DB=False, CREATE_DB=False):
    if MODE == 'MYSQL':
        db = MySQLDatabase('stock', user='code')

    else:
        if MODE == 'DEBUG':
            db_dir = DB_TEST_FILE
        elif MODE == 'REAL':
            db_dir = DB_FILE
        else:
            print 'something wrong!!'

        if DROP_DB and os.path.exists(db_dir):
            os.system('rm ' + db_dir)

        db = SqliteDatabase(db_dir)

    database_proxy.initialize(db)

    if CREATE_DB: _create_table()

