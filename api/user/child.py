#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import marshmallow
from flask import jsonify, g, request

from api.decorator import authenticated
from api.response import OKResponse, ErrorResponse
from api.schema import ChildSchema, UserChildUpdateDataSchema, UserChildDeleteRequestSchema
from usecase import child as child_usecase
from wrong import exception
from wrong import error

from . import blueprint as bp


@bp.route('/child/me', methods=['GET'])
@authenticated
def child_me_get():
    result = child_usecase.retrieve_children_by_user_id(g.db, request.current_user_id)
    data = ChildSchema(many=True).dump(result)
    resp = OKResponse(data)
    return jsonify(resp)


@bp.route('/child/me', methods=['POST'])
@authenticated
def child_me_post():
    try:
        req = UserChildUpdateDataSchema().load(request.json)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    user_id = request.current_user_id

    try:
        result = child_usecase.create_or_update_child(
            g.db, user_id, req.id, req.id_card_no, req.realname, req.nickname
        )
        return jsonify(OKResponse(
            {"id": result}
        ))

    except exception.UserException as exc:
        return jsonify(ErrorResponse(exc.error, data=str(exc)))


@bp.route('/child/delete', methods=['POST'])
@authenticated
def child_me_delete():
    try:
        req = UserChildDeleteRequestSchema().load(request.json)
    except marshmallow.ValidationError as err:
        return jsonify(
            ErrorResponse(error.InvalidParameter, data=err.messages))

    user_id = request.current_user_id

    result = child_usecase.delete_child(g.db, user_id, int(req.id))
    if not result:
        return jsonify(ErrorResponse(error.InvalidParameter, data={
            "action": "delete_last_child",
            "id": req.id
        }))

    resp = OKResponse(result)
    return jsonify(resp)
