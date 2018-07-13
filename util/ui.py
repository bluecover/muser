#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Tuple

import arrow


def obscure_string(s: str, range_pairs: List[Tuple[int, int]], r: str) -> str:
    for p in range_pairs:
        s = s.replace(s[p[0]:p[1]], r * len(s[p[0]:p[1]]), 1)
    return s


def obscure_id_card_no(id_card_no: str) -> str:
    return obscure_string(id_card_no, [(3, -4)], "*")


def obscure_mobile_no(mobile_number) -> str:
    return obscure_string(mobile_number, [(3, -4)], "*")


def calculate_age(birth: int) -> int:
    date_birth = arrow.get(birth).date()
    days_from_birth = (datetime.now().date() - date_birth).days
    age = days_from_birth // 365
    return age


def build_family_nickname(child_relation: str, child_name: List[str]):
    if not child_name:
        child_name = ['孩子']
    return "{}的{}".format("+".join(child_name), child_relation)


def distance_display(meter: int) -> str:
    if meter is None:
        return "未知"
    elif meter < 1000:
        return "{}m".format(meter)
    else:
        return "{:.1f}km".format(meter / 1000)
