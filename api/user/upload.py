#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import marshmallow
from flask import jsonify, g, request  # noqa

from api.decorator import authenticated
from api.schema import UserUploadDoneRequestSchema
from api.response import OKResponse, ErrorResponse
from wrong import error

from . import blueprint as bp


@bp.route('/upload/done', methods=['POST'])
@authenticated
def upload_done():
    try:
        req = UserUploadDoneRequestSchema().load(request.json)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    if req['category'] == 'video':
        pass

    result = {}

    resp = OKResponse(result)
    return jsonify(resp)
