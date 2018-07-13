#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from orm.orm_mysql import UserFollowModel, UserLikeModel

STATUS_LIKED = STATUS_FOLLOWED = 0

STATUS_UNLIKED = STATUS_UNFOLLOWED = 1


def count_user_liked(db: Session, user_id: int):
    c = db.query(func.count(distinct(UserLikeModel.from_user_id))).filter(
        UserLikeModel.to_user_id == user_id,
        UserLikeModel.status == STATUS_LIKED
    ).scalar()
    return c


def count_user_followed(db: Session, user_id: int):
    c = db.query(func.count(distinct(UserFollowModel.from_user_id))).filter(
        UserFollowModel.to_user_id == user_id,
        UserFollowModel.status == STATUS_FOLLOWED
    ).scalar()
    return c


def find_user_like_by_id(db: Session, from_id: int, to_id: int) -> int:
    like = db.query(UserLikeModel).filter(
        UserLikeModel.from_user_id == from_id,
        UserLikeModel.to_user_id == to_id,
        UserLikeModel.status == STATUS_LIKED
    ).first()
    return like


def find_user_follow_by_id(db: Session, from_id: int, to_id: int) -> int:
    follow = db.query(UserFollowModel).filter(
        UserFollowModel.from_user_id == from_id,
        UserFollowModel.to_user_id == to_id,
        UserFollowModel.status == STATUS_FOLLOWED
    ).first()
    return follow


def find_user_following(db: Session, user_id: int,
                        offset: int = None, limit: int = None) ->List[UserFollowModel]:
    query = db.query(UserFollowModel).filter(
        UserFollowModel.from_user_id == user_id,
        UserFollowModel.status == STATUS_FOLLOWED
    ).order_by(UserFollowModel.create_ts.desc())
    if offset is not None and limit:
        query = query.offset(offset).limit(limit)
    m = query.all()
    return m
