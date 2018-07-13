#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time


def current_timestamp() -> int:
    return int(time.mktime(time.localtime()))


class DictObject(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
