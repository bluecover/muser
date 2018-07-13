#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import arrow
import json
import redis


class ShortMessage(object):

    def __init__(self, template_code: int, params: dict):
        self.template_code = template_code  # 短信模版代号
        self.params = params


class SMSTaskProxy(object):

    def __init__(self, sending_task_queue):
        self.SMS_sending_task_queue = sending_task_queue

    def send_message(self, mobile, mobile_msg):
        param = json.dumps(mobile_msg.params)
        self.SMS_sending_task_queue.delay(mobile, mobile_msg.template_code, param)


class LoginCodeCodeStash(object):

    _REDIS_DB = 0

    _KEY_VALUE = "code:login:{}"
    _KEY_FREQUENCY = "code:login:freq:{}"
    _KEY_LAST_TIME = "code:login:last:{}"
    _KEY_RATE_LIMIT_COUNTER = "code:login:rate:count:{}"

    _LIFE_SECOND = 600  # 10 minutes

    def __init__(self, redis_config):
        self.redis_cli = redis.Redis(
            host=redis_config["host"],
            port=redis_config["port"],
            password=redis_config["password"],
            db=LoginCodeCodeStash._REDIS_DB,
            decode_responses=True
        )

    def get_last_time(self, key) -> int:
        s = self.redis_cli.get(self._KEY_LAST_TIME.format(key))
        return int(s) if s is not None else None

    def update_last_time(self, key, ttl):
        self.redis_cli.set(
            self._KEY_LAST_TIME.format(key),
            arrow.now().timestamp,
            ttl
        )

    def get_rate_limit_counter(self, key) -> int:
        s = self.redis_cli.get(self._KEY_RATE_LIMIT_COUNTER.format(key))
        return int(s) if s is not None else None

    def incr_rate_limit_counter(self, key, ttl) -> int:
        key = self._KEY_RATE_LIMIT_COUNTER.format(key)
        s = self.redis_cli.incr(key)
        value = int(s)
        if value == 1:
            self.redis_cli.expire(key, ttl)
        return value

    def get_value(self, key) -> str:
        return self.redis_cli.get(self._KEY_VALUE.format(key))

    def store_value(self, key, value):
        self.redis_cli.set(self._KEY_VALUE.format(key), value, self._LIFE_SECOND)
