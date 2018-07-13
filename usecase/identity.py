#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from flask import current_app
from sqlalchemy.orm import Session

from api.schema import ObjectInfo
from config.const import IdentityVerificationStatus
from entity import Facade
from orm import user as user_orm
from util.idcard import parse_id_card

# 商汤为服务地址
URL_IDENTIFY_VALIDITY = "http://localhost:8089/identify/validity"
URL_IDENTIFY_LIVENESS = "http://localhost:8089/identify/liveness"
# URL_IDENTIFY_VALIDITY = "http://dapi.moremom.cn/internal/identify/validity"
# URL_IDENTIFY_LIVENESS = "http://dapi.moremom.cn/internal/identify/liveness"

# 商汤请求相关参数
IDENTIFY_SERVICE_TIMEOUT = 60
IDENTIFY_CODE_SUCCESS = 1000
IDENTIFY_PASS_THRESHOLD = 0.8


def identify_validity(user_id: int, id_card_no: str, realname: str) ->bool:
    """ 调用商汤微服务接口
        验证 身份证号 和 姓名 是否匹配
        并保存相关信息
    """

    validity_verify_req_data = dict(
        user_id=user_id,
        id_number=id_card_no,
        realname=realname
    )

    try:
        resp = requests.post(
            URL_IDENTIFY_VALIDITY,
            data=validity_verify_req_data,
            timeout=IDENTIFY_SERVICE_TIMEOUT
        )
        if resp.status_code != requests.codes.ok:
            return False
    except requests.exceptions.Timeout as err:
        current_app.logger.warning("identify validity timeout: {} {} {}".format(
            user_id, id_card_no, realname))
        raise

    verify_result = resp.json()
    validity = verify_result.get("validity")

    # TODO: LOG validity identify result

    return validity


def identify_liveness(
        db: Session, user_id: int,
        liveness_id: str, id_card_no: str, realname: str,
        id_card_image: ObjectInfo = None, live_image: ObjectInfo = None,
        info: str = None) -> bool:
    """ 调用商汤微服务接口
        验证 活体信息 和 身份证信息 是否匹配
        并保存相关信息
    """

    liveness_verify_req_data = dict(
        user_id=user_id,
        liveness_id=liveness_id,
        id_number=id_card_no,
        realname=realname
    )

    try:
        resp = requests.post(
            URL_IDENTIFY_LIVENESS,
            data=liveness_verify_req_data,
            timeout=IDENTIFY_SERVICE_TIMEOUT
        )
        if resp.status_code != requests.codes.ok:
            return False
    except requests.exceptions.Timeout as err:
        current_app.logger.warning("identify service timeout: {} {} {} {}".format(
            user_id, id_card_no, realname, liveness_id))
        raise

    verify_result = resp.json()

    if verify_result.get("code") == IDENTIFY_CODE_SUCCESS and \
       verify_result.get("verification_score") > IDENTIFY_PASS_THRESHOLD:
        verify_pass = True
        status = IdentityVerificationStatus.Passed.value
    else:
        verify_pass = False
        status = IdentityVerificationStatus.Failed.value

    id_card_image_oss = ''
    if id_card_image:
        id_card_image_oss = ':'.join(['qiniu', Facade.config["qiniu"]["category"]["identity"]["bucket"], id_card_image.key])

    liveness_image_oss = ''
    if live_image:
        liveness_image_oss = ':'.join(['qiniu', Facade.config["qiniu"]["category"]["identity"]["bucket"], live_image.key])

    # TODO: Extract Method to `update_identify_verify_result`
    user_orm.upsert_user_identify(
        db, user_id, liveness_id, id_card_no, realname, status,
        id_card_image_oss=id_card_image_oss,
        liveness_image_oss=liveness_image_oss
    )

    # TODO: LOG liveness identify result

    return verify_pass


def verify_and_parse_id_card_no(user_id: int, id_card_no: str, realname: str):
    """ 验证并解析身份证号
    """
    verify_result = identify_validity(user_id, id_card_no, realname)
    if not verify_result:
        return None
    id_card_info = parse_id_card(id_card_no)
    return id_card_info


def is_user_identity_verified(db: Session, user_id: int) -> bool:
    m_user_identity = user_orm.find_user_identity(db, user_id)
    if not m_user_identity:
        return False
    return m_user_identity.status == IdentityVerificationStatus.Passed.value
