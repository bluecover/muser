#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from .aliyun_sdk.demo_sms_send import send_sms


def send(business_id, phone_numbers, sign_name, template_code, template_param=None):
    if isinstance(phone_numbers, list):
        phone_numbers = ','.join(phone_numbers)
    response = send_sms(business_id, phone_numbers, sign_name, template_code, template_param)
    result = json.loads(response)
    return result
