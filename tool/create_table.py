#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import toml
from sqlalchemy import create_engine
from orm.orm_mysql import Base

# dbconfig = toml.load('config/local.toml')['mysql']
dbconfig = toml.load('config/mysql.toml')['local']

mysql_dsn = 'mysql://{user}:{password}@{host}/{database}?{params}'.format(
    host=dbconfig['host'],
    user=dbconfig['user'],
    password=dbconfig['password'],
    database=dbconfig['database'],
    params=dbconfig['params']
)

engine = create_engine(mysql_dsn, echo=True)
Base.metadata.create_all(engine)
