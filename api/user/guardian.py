#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import marshmallow
from flask import g, jsonify, request

from api.decorator import authenticated
from api.response import OKResponse, ErrorResponse
from api.schema import CreateGuardianRequestDataSchema
from usecase import guardian as guardian_usecase
from util.ui import obscure_id_card_no, obscure_mobile_no
from wrong import error, exception
from . import blueprint as bp


@bp.route('/guardian', methods=['GET'])
@authenticated
def guardian_get():
    orm_guardians = guardian_usecase.retrieve_guardians_by_user_id(
        g.db, request.current_user_id
    )
    result = [
        dict(
            id=guardian.id,
            id_card_no=obscure_id_card_no(guardian.id_card_no),
            realname=guardian.realname,
            mobile=obscure_mobile_no(guardian.mobile)
        )
        for guardian in orm_guardians
    ]
    return jsonify(OKResponse(result))


@bp.route('/guardian', methods=['POST'])
@authenticated
def guardian_post():
    try:
        req = CreateGuardianRequestDataSchema().load(request.json)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    try:
        result = guardian_usecase.create_guardian(
            g.db, request.current_user_id, req.id_card_no, req.realname, req.mobile
        )
    except exception.UserException as exc:
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    return jsonify(OKResponse(
        {"id": result.id}
    ))
