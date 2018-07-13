#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import g, request, jsonify

from api.decorator import authenticated
from api.response import OKResponse
from api.schema import UserProfileSchema
from orm import point
from . import blueprint as bp


@bp.route('/profile', methods=['GET'])
@authenticated
def profile():

    balance = 0
    wallet = point.find_user_wallet(g.db, request.current_user_id)
    if wallet:
        balance = wallet.balance if wallet .balance else 0

    profile = dict(
        point_balance=balance,
        point_notification_count=0,
        order_notification_count=0
    )

    data = UserProfileSchema().dump(profile)
    return jsonify(OKResponse(data))
