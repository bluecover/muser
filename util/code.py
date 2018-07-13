#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from typing import List

DIGIT_CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def generate_random_code(length: int, chars: List[str] = DIGIT_CHARS) -> str:
    return "".join(random.sample(chars, length))
