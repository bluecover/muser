#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import arrow
from sqlalchemy.orm import Session

from orm.orm_mysql import MidModel


def mid_to_int(mid: MidModel):
    return (mid.base << 24) + (mid.random << 20) + mid.auto


def _mid_to_int(b, r, a):
    return (b << 24) + (r << 20) + a


def create_mid(db: Session, base: int, random_max: int = 0xF):
    now = arrow.now()
    mid = MidModel(
        base=base,
        random=random.randint(1, random_max),
        create_ts=now.timestamp,
        ts=now.datetime
    )
    db.add(mid)
    db.commit()
    return mid_to_int(mid.base, mid.auto, mid.random)
