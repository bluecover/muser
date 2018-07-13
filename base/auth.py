#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from hashlib import sha256

private_key = "Before God we are all equally wise - and equally foolish.人人生而平等。"


def create_token(device_id, user_id) -> str:
    if len(device_id) != 32:
        raise Exception("Wrong device_id length")
    ts = int(time.time())
    tmp = "{0}{1}{2}{3}".format(device_id, user_id, ts, private_key)
    sig = sha256(sha256(tmp.encode("utf8")).digest()).hexdigest()
    return "{0}{1}{2}".format(sig, user_id, ts)


# token dict
# {t , h , i } / { date , hash token string, db_id }
def parse_token(token, device_id) -> str:
    if len(device_id) != 32:
        raise Exception("Wrong device_id length")
    ts = token[-10:]
    user_id = token[64:-10]
    sig = token[:64]
    tmp = "{0}{1}{2}{3}".format(device_id, user_id, ts, private_key)
    vsig = sha256(sha256(tmp.encode("utf8")).digest()).hexdigest()
    if sig == vsig:
        return user_id
    else:
        return None
