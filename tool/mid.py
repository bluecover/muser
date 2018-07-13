#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from orm.orm_mysql import MidModel
from tool import db
from orm import mid as mid_orm

engine, session_maker = db.conn("local")
session = session_maker()


NID_BASE_01 = 0x01
NID_BASE_02 = 0x02

print("MIN: 01", mid_orm.mid_to_int(0x01, 0x00000, 0x0))
print("MAX: 01", mid_orm.mid_to_int(0x01, 0xFFFFF, 0xF))
print("MIN: 02", mid_orm.mid_to_int(0x02, 0x00000, 0x0))
print("MAX: 02", mid_orm.mid_to_int(0x02, 0xFFFFF, 0xF))

session.query(MidModel).delete()
session.commit()

for i in range(0, 20):
    id_ = mid_orm.create_mid(session, NID_BASE_01)
    print(id_)
