#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import marshmallow
from flask import g, jsonify, request

from api.decorator import authenticated
from api.schema import (
    ParamUserFollowingSchema,
    UserFollowingItemSchema
)
from api.response import OKResponse, ErrorResponse
from usecase import social as social_usecase
from wrong import error
from . import blueprint as bp


@bp.route('/following', methods=['GET'])
@authenticated
def following():
    try:
        req = ParamUserFollowingSchema().load(request.args)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    following_user_infos = social_usecase.retrieve_user_following(
        g.db, request.current_user_id, req.offset, req.limit
    )

    data = UserFollowingItemSchema(many=True).dump(following_user_infos)
    return jsonify(OKResponse(data))
