#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session

from entity import subject
from orm import social as social_orm
from orm import user as user_orm
from usecase import guardian as guardian_usecase
from util import qiniu


def retrieve_user_liked_count(db: Session, user_id: int) -> int:
    return social_orm.count_user_liked(db, user_id)


def retrieve_user_followed_count(db: Session, user_id: int) -> int:
    return social_orm.count_user_followed(db, user_id)


def retrieve_user_like(db: Session, from_id: int, to_id: int):
    return social_orm.find_user_like_by_id(db, from_id, to_id)


def retrieve_user_follow(db: Session, from_id: int, to_id: int):
    return social_orm.find_user_follow_by_id(db, from_id, to_id)


def retrieve_user_following(db: Session, user_id: int,
                            offset: int = None, limit: int = None):
    m_user_follows = social_orm.find_user_following(db, user_id, offset, limit)
    following = []
    for uf in m_user_follows:
        m_user_info = user_orm.find_user_info_by_id(db, uf.to_user_id)
        if not m_user_info:
            continue
        user_info = subject.UserInfo.from_object(m_user_info)
        if not user_info.nickname:
            user_info.nickname = guardian_usecase.update_guardian_nickname(
                db, uf.to_user_id, m_user_info.child_relation
            )
        if user_info.avatar_oss:
            user_info.avatar_url = qiniu.url_from_path(m_user_info.avatar_oss)
        else:
            user_info.avatar_url = ""
        following.append(user_info)

    return following


def retrieve_user_social(db: Session, from_id: int, to_id: int):
    liked = retrieve_user_like(db, from_id, to_id) is not None
    like_count = retrieve_user_liked_count(db, to_id)
    followed = retrieve_user_follow(db, from_id, to_id) is not None
    followed_count = retrieve_user_followed_count(db, to_id)
    return dict(
        liked=liked,
        like_count=like_count,
        followed=followed,
        follow_count=followed_count
    )
