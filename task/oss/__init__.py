#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


STASH_SERVICE_ADDR = 'http://localhost:8088'


class StashAPI:
    AddObjectReference = '{}{}'.format(STASH_SERVICE_ADDR, '/object/addref')


def add_object_reference(user_id, ref_tag, object_info):
    data = {
        'userID': user_id,
        'tag': ref_tag,
        'object': object_info
    }
    r = requests.post(StashAPI.AddObjectReference, json=data)
    return r.json()
