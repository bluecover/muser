#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Tuple

import pandas as pd
from redis import Redis
from sqlalchemy.orm import Session

from entity import lbs
from orm import address as address_orm
from orm import user as user_orm
from orm import carer as carer_orm


class RedisKeys(Enum):
    KOLAll = "hot:carer:kol:all"
    KOLOfCity = "hot:carer:kol:{city}"
    CarerLocations = "carer:location:{city}"
    ShareTime = "hot:carer:share:{city}"
    ReserveTime = "hot:carer:reserve:{city}"
    Like = "hot:carer:like:{city}"
    Follow = "hot:carer:follow:{city}"


SQL_CITY_USERS_ORDER_BY_SHARE_TIME = """
    SELECT user_id, city_id, sum(end_ts-start_ts) AS time FROM time_sharing
    WHERE city_id IS NOT NULL
    GROUP BY user_id, city_id
    ORDER BY time DESC
    LIMIT 30 OFFSET 0
"""

SQL_CITY_USERS_ORDER_BY_RESERVE_TIME = """
    SELECT seller_id, city_id, sum(end_ts-start_ts) AS time FROM time_sharing_order
    WHERE city_id IS NOT NULL
    GROUP BY seller_id, city_id
    ORDER BY time DESC
    LIMIT 30 OFFSET 0
"""

SQL_CITY_USERS_ORDER_BY_LIKE = """
    SELECT to_user_id, city_id, count(*) as count FROM user_like
    WHERE city_id IS NOT NULL
    GROUP BY to_user_id, city_id
    ORDER BY count DESC
    LIMIT 30 OFFSET 0
"""

SQL_CITY_USERS_ORDER_BY_FOLLOW = """
    SELECT to_user_id, city_id, count(*) as count FROM user_follow
    WHERE city_id IS NOT NULL
    GROUP BY to_user_id, city_id
    ORDER BY count DESC
    LIMIT 30 OFFSET 0
"""


def retrieve_city_carers_with_location(db: Session) -> Dict[int, List]:
    sql_city_ids = """
        SELECT DISTINCT city_id
        FROM user_address;
    """
    city_ids = [r[0] for r in db.execute(sql_city_ids).fetchall()]
    carer_locations = carer_orm.find_carer_locations_by_city_ids(db, city_ids)
    df = pd.DataFrame(carer_locations, columns=["user_id", "city_id", "lat", "lng"])
    result = dict()
    for city_id in city_ids:
        values = df[df.city_id == city_id].values
        result[city_id] = values
    return result


def _group_city_carers_by_order(db: Session, sql: str) -> Dict[int, List[int]]:
    sql_result = db.execute(sql).fetchall()
    df = pd.DataFrame(sql_result, columns=["user_id", "city_id", "value"])
    city_ids = df.city_id.unique()
    city_top_user_ids = dict()
    for id_ in city_ids:
        top_user_ids = df[df.city_id == id_]\
            .sort_values(by=['value'], ascending=False)\
            .user_id.unique()
        city_top_user_ids[id_] = top_user_ids
    return city_top_user_ids


def _update_user_id_list(redis: Redis, key: str, user_ids: List[int]):
    redis.delete(key)
    redis.rpush(key, *user_ids)


def _update_redis_city_user_id_list(redis: Redis, key_format: str, city_user_ids: Dict[int, List[int]]):
    for city, user_ids in city_user_ids.items():
        key = key_format.format(city=city)
        redis.delete(key)
        redis.rpush(key, *user_ids)


def _merge_and_unique_lists(*lists) -> List:
    seen = dict()
    result = []
    for list_ in lists:
        for i in list_:
            if i not in result:
                result.append(i)
                seen[i] = True
    return result


def _offset_and_limit(list_: List, offset: int, limit: int) ->List:
    if offset is not None and limit is not None:
        return list_[offset:offset + limit]
        if offset >= 0 and offset < len(list_):
            left = offset
        else:
            left = 0
        if limit <= 0:
            limit = len(list_)
        return list_[left:left + limit]
    else:
        return list_


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)


def _group_city_kol(db: Session) -> Tuple[List[int], Dict[int, List]]:
    sql_kol_user_ids = """
        SELECT DISTINCT user_id
        FROM user_kol
        WHERE status=0;
    """
    all_kol = list()
    city_kol_map = dict()
    kol_user_ids = [r[0] for r in db.execute(sql_kol_user_ids).fetchall()]
    for user_id in kol_user_ids:
        city_info = carer_orm.find_carer_city_info_by_user_id(db, user_id)
        if not city_info:
            continue
        all_kol.append(user_id)
        city_kol_map.setdefault(city_info.city_id, []).append(user_id)

    return all_kol, city_kol_map


def update_hot_carer_info_list(db: Session, redis: Redis):
    city_carer_locations = retrieve_city_carers_with_location(db)
    for city_id, carer_locations in city_carer_locations.items():
        key = RedisKeys.CarerLocations.value.format(city=city_id)
        L = [json.dumps(list(cl), cls=DecimalEncoder) for cl in carer_locations]
        if not L:
            continue
        redis.delete(key)
        redis.rpush(key, *L)

    all_kol_carers, city_kol_carers = _group_city_kol(db)
    _update_user_id_list(redis, RedisKeys.KOLAll.value, all_kol_carers)
    _update_redis_city_user_id_list(redis, RedisKeys.KOLOfCity.value, city_kol_carers)

    city_top_carers_by_sharing_time = _group_city_carers_by_order(db, SQL_CITY_USERS_ORDER_BY_SHARE_TIME)
    _update_redis_city_user_id_list(redis, RedisKeys.ShareTime.value, city_top_carers_by_sharing_time)

    city_top_carers_by_reserved_time = _group_city_carers_by_order(db, SQL_CITY_USERS_ORDER_BY_RESERVE_TIME)
    _update_redis_city_user_id_list(redis, RedisKeys.ReserveTime.value, city_top_carers_by_reserved_time)

    city_top_carers_by_like = _group_city_carers_by_order(db, SQL_CITY_USERS_ORDER_BY_LIKE)
    _update_redis_city_user_id_list(redis, RedisKeys.Like.value, city_top_carers_by_like)

    city_top_carers_by_follow = _group_city_carers_by_order(db, SQL_CITY_USERS_ORDER_BY_FOLLOW)
    _update_redis_city_user_id_list(redis, RedisKeys.Follow.value, city_top_carers_by_follow)


def _retrieve_city_top_user_ids(redis: Redis, city: int) -> List[str]:
    sharing_time_list = redis.lrange(RedisKeys.ShareTime.value.format(city=city), 0, -1)
    reserved_time_list = redis.lrange(RedisKeys.ReserveTime.value.format(city=city), 0, -1)
    liked_count_list = redis.lrange(RedisKeys.Like.value.format(city=city), 0, -1)
    follower_time_list = redis.lrange(RedisKeys.Follow.value.format(city=city), 0, -1)

    total = _merge_and_unique_lists(
        sharing_time_list,
        reserved_time_list,
        liked_count_list,
        follower_time_list
    )
    return total


def _retrieve_all_kol_user_ids(redis: Redis, city: int) -> List[str]:
    kol_list = redis.lrange(RedisKeys.KOLAll.value, 0, -1)
    return kol_list


def _retrieve_city_kol_user_ids(redis: Redis, city: int) -> List[str]:
    kol_list = redis.lrange(RedisKeys.KOLOfCity.value.format(city=city), 0, -1)
    return kol_list


def _sort_user_ids_by_distance_to_a_location(
        db: Session, redis: Redis,
        user_id_list: List[str],
        lat: Decimal, lng: Decimal) -> List[int]:
    distance = dict()
    carer_info_list = []
    for user_id in user_id_list:
        m_carer_info = user_orm.find_carer_info_by_user_id(db, int(user_id))
        if not m_carer_info:
            continue
        m_address = address_orm.find_user_address_by_id(db, m_carer_info.address_id)
        if not m_address:
            continue
        if lat and lng and m_address.lat and m_address.lng:
            distance[m_carer_info.user_id] = lbs.distance_m(
                (lat, lng),
                (m_address.lat, m_address.lng)
            )
        else:
            distance[m_carer_info.user_id] = sys.maxsize
        carer_info_list.append(m_carer_info)

    carer_info_list.sort(key=lambda c: distance[c.user_id])
    return [c.user_id for c in carer_info_list]


def retrieve_hot_carer_id_list(
        db: Session, redis: Redis, city_id: int, lat: Decimal, lng: Decimal,
        offset: int, limit: int) -> List[int]:

    kol_user_ids = _retrieve_all_kol_user_ids(redis, city_id)
    kol_user_ids_sorted_by_distance = _sort_user_ids_by_distance_to_a_location(
        db, redis, kol_user_ids, lat, lng)

    city_top_user_ids = _retrieve_city_top_user_ids(redis, city_id)
    kol_user_id_set = set(kol_user_ids)
    city_top_user_ids_except_kol = [user_id for user_id in city_top_user_ids if user_id not in kol_user_id_set]
    city_top_user_ids_sorted_by_distance = _sort_user_ids_by_distance_to_a_location(
        db, redis, city_top_user_ids_except_kol, lat, lng)

    total_user_ids = kol_user_ids_sorted_by_distance + city_top_user_ids_sorted_by_distance

    return _offset_and_limit(total_user_ids, offset, limit)


def retrieve_city_carer_locations(redis: Redis, city_id: int) -> List[dict]:
    carer_location_list_str = redis.lrange(
        RedisKeys.CarerLocations.value.format(city=city_id), 0, -1
    )
    carer_locations = []
    for s in carer_location_list_str:
        L = json.loads(s)
        carer_locations.append(dict(
            user_id=L[0],
            city_id=L[1],
            lat=Decimal(float(L[2])),
            lng=Decimal(float(L[3])),
        ))
    return carer_locations


def retrieve_nearby_carer_id_list(
        db: Session, redis: Redis, city_id: int, lat: Decimal, lng: Decimal,
        offset: int, limit: int) -> List[int]:

    carer_locations = retrieve_city_carer_locations(redis, city_id)
    for cl in carer_locations:
        if lat and lng and cl["lat"] and cl["lng"]:
            cl["distance"] = lbs.distance_m((lat, lng), (cl["lat"], cl["lng"]))
        else:
            cl["distance"] = sys.maxsize

    carer_locations.sort(key=lambda c: c["distance"])
    return _offset_and_limit([c["user_id"] for c in carer_locations], offset, limit)


if __name__ == '__main__':

    import toml
    from orm import Facade as orm_facade  # noqa
    config = toml.load("config/default.toml")
    mysql_config = config["mysql"]
    redis_config = config["redis"]
    orm_facade.initialize(mysql_config)
    session = orm_facade.make_scoped_session()
    redis_cli = Redis(host=redis_config["host"], port=6379, decode_responses=True)

    update_hot_carer_info_list(session, redis_cli)

    lat, lng = 39.960725, 116.483551

    nearby_carer_id_list = retrieve_nearby_carer_id_list(session, redis_cli, 110100, lat, lng,
                                                         offset=None, limit=None)
    print(nearby_carer_id_list)

    carer_id_list = retrieve_hot_carer_id_list(
        session, redis_cli, 110100, lat, lng, offset=None, limit=None
    )

    for id_ in carer_id_list:
        c = user_orm.find_carer_info_by_user_id(session, int(id_))
        m_address = address_orm.find_user_address_by_id(session, c.address_id)
        distance = lbs.distance_m(
            (lat, lng),
            (m_address.lat, m_address.lng)
        )
        print(distance)
