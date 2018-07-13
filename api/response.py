#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from util import DictObject


class OKResponse(DictObject):
    def __init__(self, data):
        super(OKResponse).__init__()
        self.status = dict(code=0, msg='')
        self.data = data


class ErrorResponse(DictObject):
    def __init__(self, error, data=dict()):
        self.status = dict(code=error.code, msg=error.wording)
        self.data = data

    @staticmethod
    def from_error(error):
        return ErrorResponse(error.code, error.wording)
