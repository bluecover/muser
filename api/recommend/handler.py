#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from decimal import Decimal

import marshmallow
from flask import current_app, g, jsonify, request

from api.schema import (
    ParamRecommendCarerHotSchema,
    ParamRecommendCarerNearbySchema,
    RecommendCarerResponseDataItemSchema
)
from api.response import OKResponse, ErrorResponse
from entity import Facade as EntityFacade
from entity import lbs
from usecase import carer as carer_usecase
from usecase import recommend as recommend_usecase  # noqa
from usecase import social as social_usecase
from usecase import user_info as user_info_usecase
from util import qiniu
from util.ui import distance_display
from wrong import error
from . import blueprint as bp


def _build_recommend_carer_info(
        user_id: int, city_id: int, lat: Decimal = None, lng: Decimal = None) -> dict:

    user_info = user_info_usecase.retrieve_user_info(g.db, user_id)

    if not user_info:
        return None

    carer_info = carer_usecase.retrieve_care_info(g.db, user_id)
    social_info = social_usecase.retrieve_user_social(g.db, request.current_user_id, user_id)

    address = carer_info.address
    distance = None
    if lat and lng and address.lat and address.lng:
        distance = lbs.distance_m(
            (lat, lng),
            (address.lat, address.lng)
        )

    if carer_info.city_id == city_id:
        address_name = address.name
    else:
        address_name = address.city

    return dict(
        user_id=user_id,
        videos=carer_usecase.videos_dict_to_list(carer_info.videos),
        nickname=user_info.nickname,
        avatar_url=qiniu.url_from_path(user_info.avatar_oss) if user_info.avatar_oss else "",
        address=(address.address or "") + (address.name or "") + (address.room or ""),
        address_name=address_name,
        distance=distance_display(distance),
        liked=social_info["liked"],
        like_count=social_info["like_count"],
        followed=social_info["followed"],
        follow_count=social_info["follow_count"]
    )


@bp.route("/carer/hot", methods=["GET"])
def hot_carers():
    try:
        req = ParamRecommendCarerHotSchema().load(request.args)
    except marshmallow.ValidationError as err:
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    if req.city_id:
        req.city_id = (req.city_id // 100) * 100  # 参考GB码 -> 市GB码

    if req.lat and req.lng and req.city_id:
        hot_carer_ids = recommend_usecase.retrieve_hot_carer_id_list(
            g.db, EntityFacade.redis_cli, req.city_id, req.lat, req.lng,
            req.offset, req.limit
        )
    else:
        # TODO: KOL
        CITY_ID_BEIJINT = 110100
        hot_carer_ids = recommend_usecase.retrieve_hot_carer_id_list(
            g.db, EntityFacade.redis_cli, CITY_ID_BEIJINT, req.lat, req.lng,
            req.offset, req.limit
        )

    current_app.logger.warning(hot_carer_ids)

    carers = []
    for id_ in hot_carer_ids:
        c = _build_recommend_carer_info(id_, req.city_id, req.lat, req.lng)
        if not c:
            current_app.logger.warning("invalid user id: %s", id_)
            continue
        carers.append(c)

    data = RecommendCarerResponseDataItemSchema(many=True).dump(carers)
    return jsonify(OKResponse(data))


@bp.route("/carer/nearby", methods=["GET"])
def nearby_carers():
    try:
        req = ParamRecommendCarerNearbySchema().load(request.args)
    except marshmallow.ValidationError as err:
        return jsonify(
            ErrorResponse(error.InvalidParameter, data=err.messages))

    if req.lat and req.lng and req.city_id:
        city_id = (req.city_id // 100) * 100  # 参考GB码 -> 市GB码
        recommend_carer_ids = recommend_usecase.retrieve_nearby_carer_id_list(
            g.db, EntityFacade.redis_cli, city_id, req.lat, req.lng,
            req.offset, req.limit
        )
    else:
        recommend_carer_ids = recommend_usecase.retrieve_hot_carer_id_list(
            g.db, EntityFacade.redis_cli, req.city_id, req.lat, req.lng,
            req.offset, req.limit
        )

    carers = []
    for id_ in recommend_carer_ids:
        c = _build_recommend_carer_info(id_, None, req.lat, req.lng)
        if not c:
            current_app.logger.warning("invalid user id: %s", id_)
            continue
        carers.append(c)

    data = RecommendCarerResponseDataItemSchema(many=True).dump(carers)
    return jsonify(OKResponse(data))
