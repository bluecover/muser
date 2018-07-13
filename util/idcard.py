#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import arrow
from collections import namedtuple

from base.validator import v_id_number
from config.const import Gender


IDCardInfo = namedtuple("IDCardInfo", ["date_birth", "city_id", "gender"])


def parse_id_card(card_number: str, validate: bool =False) ->IDCardInfo:
    if validate and not v_id_number(card_number):
        return None

    return IDCardInfo(
        arrow.get(card_number[6:14], "YYYYMMDD").date(),
        card_number[:6],
        Gender.Male.value if int(card_number[16]) % 2 == 1 else Gender.Female.value
    )
