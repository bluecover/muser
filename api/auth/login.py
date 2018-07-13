#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import marshmallow
import requests
from flask import current_app, g, jsonify, request

from api.response import OKResponse, ErrorResponse
from api.schema import ParamAuthMobileCodeSchema, AuthMobileLoginRequestSchema
from base.auth import create_token
from config.const import MOBILE_CODE_CHINA, UserStatus
from usecase import login as login_usecase
from wrong import error, exception
from . import blueprint as bp


WHITE_LIST = [
    "18612250030",
    "13521522428",
    "18612982458",
    "13810400576",
    "18612852759"
]


@bp.route("/mobile/code", methods=["GET"])
def mobile_code_get():
    try:
        req = ParamAuthMobileCodeSchema().load(request.args)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    try:
        code = login_usecase.send_login_code(req.mobile)
    except exception.LoginException as exc:
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # White list for debug user.
    if req.mobile in WHITE_LIST:
        status = login_usecase.get_login_code_status(req.mobile)
        bearychat = "https://hook.bearychat.com/=bwD6u/incoming/38e28a304b97b7b67335c3be1cb2fe81"
        msg = "{} 码 {}\n1小时内发送次数 {}".format(
            req.mobile, code,
            status["counter"]
        )
        requests.post(bearychat, json={"text": msg})

    current_app.logger.warning("mobile_code_get:{}:{}".format(req.mobile, code))

    return jsonify(OKResponse(
        {
            "mobile": req.mobile,
            "code": None,
            "retry_time": None  # 暂时没有显示发送次数的需求
        }
    ))


@bp.route("/mobile/login", methods=["POST"])
def mobile_login():
    try:
        req = AuthMobileLoginRequestSchema().load(request.json)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    if not login_usecase.verify_login_code(req.mobile, req.password):
        return jsonify(ErrorResponse(error.InvalidLoginCode))

    m_user, m_user_info = login_usecase.signup_user(
        g.db, req.mobile, MOBILE_CODE_CHINA, req.child_info
    )
    if not m_user:
        return jsonify(ErrorResponse(error.LoginFailed))

    if m_user.status != UserStatus.Normal.value:
        return jsonify(ErrorResponse(error.UserIsBanned))

    token = create_token(request.headers["did"], m_user.id)

    current_app.logger.warning("mobile_login:{}:{}:{}".format(m_user.id, m_user.mobile, token))

    return jsonify(OKResponse({
        "user_id": m_user.id,
        "token": token,
        "relation": m_user_info.child_relation
    }))


@bp.route("/logout", methods=["POST"])
async def logout():
    return jsonify(OKResponse(None))
