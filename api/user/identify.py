#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import marshmallow
from flask import jsonify, g, request

from wrong import error
from api.decorator import authenticated
from api.response import OKResponse, ErrorResponse
from api.schema import UserIdentifyLivenessRequestSchema
from usecase import identity as identity_usecase

from . import blueprint as bp


@bp.route('/identify/liveness', methods=['GET'])
@authenticated
def identify_liveness_get():

    result = identity_usecase.is_user_identity_verified(g.db, request.current_user_id)

    resp = OKResponse({'result': result})
    return jsonify(resp)


@bp.route('/identify/liveness', methods=['POST'])
@authenticated
def identify_liveness_post():
    try:
        req = UserIdentifyLivenessRequestSchema().load(request.json)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    result = identity_usecase.identify_liveness(
        g.db, request.current_user_id,
        req.liveness_id, req.id_card_no, req.realname,
        req.idcard_image, req.live_image,
        req.info
    )

    resp = OKResponse({'result': result})
    return jsonify(resp)
