#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import marshmallow
from flask import g, jsonify, request

from api.decorator import authenticated
from api.response import OKResponse, ErrorResponse
from api.schema import (
    ParamUserCarerInfoSchema,
    CarerApplyRequestDataSchema,
    CarerInfoGetResponseDataSchema,
    CarerApplicationDataSchema
)
from config.const import (
    CARER_APPLY_QR_CODE_IMAGE_URL,
    CARER_APPLY_REJECT_REASON,
    CARER_APPLY_WX_ID,
    DEGREE_INT2CN,
)
from entity import lbs
from usecase import carer as carer_usecase
from usecase import identity as identity_usecase
from usecase import social as social_usecase
from usecase import user_info as user_info_usecase
from util.ui import distance_display
from wrong import error, exception
from . import blueprint as bp


@bp.route('/carer/info', methods=['GET'])
def carer_info():
    try:
        req = ParamUserCarerInfoSchema().load(request.args)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    target_user_id = req.user_id

    user_info = user_info_usecase.retrieve_user_info(g.db, target_user_id)
    if not user_info:
        return jsonify(ErrorResponse(error.NonExistentUser))

    carer_info = carer_usecase.retrieve_care_info(g.db, target_user_id)
    if not carer_info:
        return jsonify(ErrorResponse(error.NonExistentCarer))

    # Nickname
    carer_info.nickname = user_info.nickname

    # Videos
    carer_info.videos = carer_usecase.videos_dict_to_list(carer_info.videos)

    # Distance
    distance = 0
    if req.lat and req.lng and carer_info.address.lat and carer_info.address.lng:
        distance = lbs.distance_m(
            (req.lat, req.lng),
            (carer_info.address.lat, carer_info.address.lng)
        )
    carer_info['distance'] = distance_display(distance)

    # Degree
    carer_info.degree = DEGREE_INT2CN[carer_info.degree]

    # Like & Follow
    social_info = social_usecase.retrieve_user_social(
        g.db, request.current_user_id, target_user_id
    )
    carer_info.update(social_info)

    result = CarerInfoGetResponseDataSchema().dump(carer_info)

    resp = OKResponse(result)
    return jsonify(resp)


@bp.route('/carer/apply', methods=['GET'])
@authenticated
def carer_apply_get():
    application = carer_usecase.retrieve_carer_application(
        g.db, request.current_user_id
    )
    if not application:
        # 如果没有申请记录 返回实名认证结果
        identify_result = identity_usecase.is_user_identity_verified(
            g.db, request.current_user_id
        )
        return jsonify(
            ErrorResponse(
                error.NonExistentCarerApplication,
                data=dict(identify_result=identify_result)
            )
        )

    application.result = CARER_APPLY_REJECT_REASON.get(application.result, "")

    result = CarerApplicationDataSchema().dump(application)
    return jsonify(OKResponse(result))


@bp.route('/carer/apply', methods=['POST'])
@authenticated
def carer_apply_post():
    try:
        req = CarerApplyRequestDataSchema().load(request.json)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    try:
        result = carer_usecase.submit_carer_application(
            g.db, request.current_user_id, req
        )

        # TODO: Review carer application
        # carer_usecase.approve_carer_application(
        #    g.db, request.current_user_id
        # )

    except exception.CarerApplicationException as exc:
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    result = dict(
        qr=CARER_APPLY_QR_CODE_IMAGE_URL,
        wx_id=CARER_APPLY_WX_ID
    )

    return jsonify(OKResponse(result))


@bp.route('/carer/apply_result', methods=['GET'])
@authenticated
def carer_apply_result():
    application = carer_usecase.retrieve_carer_application(
        g.db, request.current_user_id, detail=False
    )
    if not application:
        result = dict(
            status=-1,
            reason=CARER_APPLY_REJECT_REASON.get(-1, "")
        )
    else:
        result = dict(
            status=application.status,
            reason=CARER_APPLY_REJECT_REASON.get(application.result, "")
        )
    return jsonify(OKResponse(result))
