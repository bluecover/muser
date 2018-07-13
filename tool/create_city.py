#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from orm.orm_mysql import CityModel
from tool import db

engine, session_maker = db.conn("local")
session = session_maker()

city_file = open("docs/meituan_address.txt", "r")
contents = city_file.read()
city_json = json.loads(contents)
city_nav = city_json["data"]["city_nav"]
city_orms = []

for item in city_nav:
    cities = item["cities"]
    for city in cities:
        orm_city = CityModel(
            id=city["city_id"],
            name=city["city_name"],
            pinyin=city["city_pinyin"]
        )
        city_orms.append(orm_city)

session.add_all(city_orms)
session.commit()
