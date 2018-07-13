#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import arrow
from sqlalchemy.orm import Session

from api.schema import AuthMobileLoginRequest_ChildInfo as FirstLaunchInfo
from config.const import LOGIN_CODE_LENGTH, MessageTemplate
from entity import Facade as EntityFacade
from entity.sms import ShortMessage
from orm.user import (
    find_user_by_mobile,
    find_user_info_by_id,
    create_user_transaction,
    upsert_user_info,
    create_child_transaction
)
from util.code import generate_random_code
from util.hash import double_sha256
from wrong import exception


CODE_FREQUENCY = 60  # 发送频率限制: 60 秒
CODE_RATE_LIMIT_DURATION = 3600  # Rate Limit 1 小时 10 次
CODE_RATE_LIMIT_MAX = 5  # Rate Limit 1 小时 5 次


def send_login_code(mobile_number: str) -> str:

    code_stash = EntityFacade.code_stash

    # Check last send time
    last_time = code_stash.get_last_time(mobile_number)
    if last_time and arrow.now().timestamp - last_time < CODE_FREQUENCY:
        raise exception.LoginCodeSMSTooOften(mobile_number)

    # Check duration limit
    current = code_stash.get_rate_limit_counter(mobile_number)
    if current and current > CODE_RATE_LIMIT_MAX:
        raise exception.LoginCodeSMSOverLimit(mobile_number)

    code_stash.incr_rate_limit_counter(mobile_number, CODE_RATE_LIMIT_DURATION)

    # Generate & Store & Send
    code = generate_random_code(LOGIN_CODE_LENGTH)
    code_stash.store_value(mobile_number, code)
    code_stash.update_last_time(mobile_number, CODE_FREQUENCY)
    EntityFacade.sms_provider.send_message(
        mobile_number,
        ShortMessage(MessageTemplate.LoginCode.value, params=dict(code=code))
    )

    return code


def get_login_code_status(mobile_number: str) -> dict:
    code_stash = EntityFacade.code_stash
    counter = code_stash.get_rate_limit_counter(mobile_number)
    last_time = code_stash.get_last_time(mobile_number)
    return dict(
        counter=counter,
        last_time=last_time
    )


def retrieve_login_code(mobile_number: str, encrypt: bool = False) -> str:

    code = EntityFacade.code_stash.get_value(mobile_number)
    if not code:
        return None
    return double_sha256('{}{}'.format(mobile_number, code)) if encrypt else code


def verify_login_code(mobile_number: str, code: str, encrypt: bool = False) ->bool:
    # 审核账号
    if mobile_number == '13012345678' and code == '0000':
        return True

    stashed_code = retrieve_login_code(mobile_number, encrypt)
    if not stashed_code:
        return False
    return code == stashed_code


def store_first_launch_user_info(
        db: Session, user_id: int, mobile: str, first_launch_info: FirstLaunchInfo):
    """ 保存 App初次启动 时用户填写的信息
    """

    child_relation = first_launch_info.relation if first_launch_info.relation\
        else 7

    # TODO: 把下面两部合并成一个 transaction
    upsert_user_info(db, user_id, mobile=mobile, child_relation=child_relation)

    create_child_transaction(
        db, user_id,
        birth_ts=first_launch_info.birth_ts if first_launch_info.born else None,
        gender=first_launch_info.gender,
        nickname=first_launch_info.nickname
    )


def signup_user(
        db: Session, mobile_number: str, country_code: str,
        first_launch_info: FirstLaunchInfo = None):
    """ 先用 手机号 查找用户
        如果找到 直接返回
        如果没有找到 说明是新用户 执行创建新用户的 transaction
    """

    existing_user = find_user_by_mobile(db, mobile_number)
    if existing_user:
        user_info = find_user_info_by_id(db, existing_user.id)
        return existing_user, user_info

    # TODO: 把下面两部合并成一个 transaction
    new_user, user_info = create_user_transaction(db, country_code, mobile_number)
    if first_launch_info:
        store_first_launch_user_info(db, new_user.id, new_user.mobile, first_launch_info)

    return new_user, user_info
