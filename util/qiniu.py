#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from qiniu import Auth
from entity import Facade


URL_DURATION = 7200


def url(bucket: str, key: str) -> str:
    return "{}/{}".format(Facade.config["qiniu"]["bucket"][bucket]["url"], key)


def private_url(base_url: str, duration_sec: int = URL_DURATION):
    q = Auth(Facade.config["qiniu"]["access_key"], Facade.config["qiniu"]["secret_key"])
    return q.private_download_url(base_url, expires=duration_sec)


def url_from_path(oss_path: str) -> str:
    splits = oss_path.split(":")
    bucket = splits[1]
    key = splits[2]
    return "{}/{}".format(Facade.config["qiniu"]["bucket"][bucket]["url"], key)
