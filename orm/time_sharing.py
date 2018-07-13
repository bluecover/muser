#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from sqlalchemy import asc
from sqlalchemy.orm import Session

from util import current_timestamp
from .orm_mysql import TimeSharingModel, UserCarerInfoModel


def create_time_sharing(
        db: Session,
        user_id: int,
        carer_info: UserCarerInfoModel,
        start_ts: int, end_ts: int,
        price: int,
        activity_tags: List[str],
        description: str,
        accompany_required: bool) -> int:

    m_time_sharing = TimeSharingModel(
        # data copy from publisher
        user_id=user_id,
        child_age_min=carer_info.child_age_min,
        child_age_max=carer_info.child_age_max,
        child_count_max=carer_info.child_count_max,
        address_id=carer_info.address_id,
        # data new for this instance
        start_ts=start_ts,
        end_ts=end_ts,
        price=price,
        activity=','.join([str(i) for i in activity_tags]),
        description=description,
        accompany_required=accompany_required,
        child_count=0,
        # data for common
        create_ts=current_timestamp(),
        status=0
    )

    db.add(m_time_sharing)
    db.commit()

    return m_time_sharing.id


def find_time_sharing_by_id(db: Session, id_: int) ->TimeSharingModel:
    m = db.query(TimeSharingModel).filter(
        TimeSharingModel.id == id_).first()
    return m


def find_time_sharings_by_ids(
        db: Session,
        ids: List[int],
        order_by: str = None) -> List[TimeSharingModel]:

    query = db.query(TimeSharingModel).filter(
        TimeSharingModel.id.in_(ids)
    )
    if order_by:
        query = query.order_by(asc(order_by))
    m_time_sharings = query.all()
    return m_time_sharings


def find_time_sharing_ids_by_user_id_and_ts(
        db: Session,
        user_id: int,
        from_ts: int, to_ts: int,
        order_by: str = None,
        offset: int = None, limit: int = None) -> List[int]:

    query = db.query(TimeSharingModel.id).filter(
        TimeSharingModel.user_id == user_id,
        TimeSharingModel.end_ts >= from_ts,
        TimeSharingModel.end_ts <= to_ts,
        TimeSharingModel.status == 0
    )

    if order_by:
        query = query.order_by(TimeSharingModel.start_ts.asc())
    if offset is not None and limit:
        query = query.offset(offset).limit(limit)

    m_time_sharing_ids = query.all()

    return m_time_sharing_ids


def find_time_sharings_by_uesr_id_and_ts(
        db: Session,
        user_id: int,
        from_ts: int, to_ts: int,
        order_by: str = None,
        offset: int = None, limit: int = None) -> List[TimeSharingModel]:

    ids = find_time_sharing_ids_by_user_id_and_ts(
        db, user_id, from_ts, to_ts, offset=offset, limit=limit
    )
    return find_time_sharings_by_ids(db, ids, order_by)
