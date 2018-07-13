#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import marshmallow
from flask import g, jsonify, request

from api.decorator import authenticated
from api.response import OKResponse, ErrorResponse
from api.schema import (
    UserInfoSchema,
    UserInfoUpdateRequestSchema,
    UserInfoPresetRequestSchema
)
from config.const import (
    DEGREE_INT2CN,
    CHILD_RELATION_INT2CN,
    CarerApplicationStatus
)
from usecase import carer as carer_usecase
from usecase import child as child_usecase
from usecase import user_info as user_info_usecase
from util import qiniu
from util.ui import obscure_mobile_no, obscure_id_card_no
from wrong import error, exception
from . import blueprint as bp


@bp.route('/info/me', methods=['GET'])
@authenticated
def info_me_get():
    user_info = user_info_usecase.retrieve_user_info(g.db, request.current_user_id)
    if not user_info:
        return jsonify(ErrorResponse(error.InvalidParameter))

    # Resolve `is_carer`
    carer_info = carer_usecase.retrieve_care_info(g.db, request.current_user_id)
    user_info.is_carer = carer_info is not None

    # Resolve `children_nicknames`
    children = child_usecase.retrieve_children_by_user_id(g.db, request.current_user_id)
    children_nicknames = [c.nickname for c in children]
    user_info.children_nicknames = children_nicknames

    # Resolve ui text
    if user_info.mobile:
        user_info.mobile = obscure_mobile_no(user_info.mobile)
    if user_info.id_card_no:
        user_info.id_card_no = obscure_id_card_no(user_info.id_card_no)
    if user_info.degree is not None:
        user_info.degree = DEGREE_INT2CN[user_info.degree]
    if user_info.child_relation is not None:
        user_info.child_relation = CHILD_RELATION_INT2CN[user_info.child_relation]
    if user_info.avatar_oss:
        user_info.avatar_url = qiniu.url_from_path(user_info.avatar_oss)
    if user_info.realname:
        user_info.realname = user_info.realname

    # Resolve `carer_apply_status`
    carer_application = carer_usecase.retrieve_carer_application(
        g.db, request.current_user_id
    )
    if not carer_application:
        user_info.carer_apply_status = CarerApplicationStatus.NotSubmitted.value
    else:
        user_info.carer_apply_status = carer_application.status

    data = UserInfoSchema().dump(user_info)
    resp = OKResponse(data)
    return jsonify(resp)


@bp.route('/info/me', methods=['POST'])
@authenticated
def info_me_post():
    try:
        req = UserInfoUpdateRequestSchema().load(request.json)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    try:
        result = user_info_usecase.update_user_info(
            g.db, request.current_user_id,
            req.id_card_no, req.realname,
            req.mobile,
            req.child_relation,
            req.avatar
        )
        return jsonify(OKResponse(result))

    except exception.UserException as exc:
        return jsonify(ErrorResponse(exc.error, data=str(exc)))


@bp.route('/info/preset', methods=['POST'])
@authenticated
def preset_user_info():
    try:
        req = UserInfoPresetRequestSchema().load(request.json)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    try:
        result = user_info_usecase.store_preset_user_info(
            g.db, request.current_user_id,
            req.born,
            req.nickname,
            req.relation,
            req.birth_ts,
            req.gender
        )
        return jsonify(OKResponse(result))

    except exception.UserException as exc:
        return jsonify(ErrorResponse(exc.error, data=str(exc)))
