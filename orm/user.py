#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
from typing import List

import arrow
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from util import current_timestamp
from util.hash import md5
from orm import mid as mid_orm
from orm.exc import is_duplicate_entry_exception
from orm.orm_mysql import (
    UserModel, UserInfoModel, ChildModel, UserChildModel,
    UserIdentityModel, UserCarerInfoModel, UserGuardianModel,
    MidModel
)
from wrong.exception import ORMCreateChildFailed


def find_user_by_id(db: Session, id_: int):
    m_user = db.query(UserModel).filter(UserModel.id == id_).first()
    return m_user


def find_user_by_mobile(db: Session, mobile_number: str):
    m_user = db.query(UserModel).filter(UserModel.mobile == mobile_number).first()
    return m_user


def find_user_info_by_id(db: Session, id_: int):
    m_user_info = db.query(UserInfoModel).filter(UserInfoModel.user_id == id_).first()
    return m_user_info


def create_user_transaction(
        db: Session, mobile_code: str, mobile_number: str,
        mid_base: int = 0x01, mid_random_max: int = 0xF):

    now = arrow.now()
    password = md5('{}{}'.format(now.timestamp, random.randint(0, 10000000)))

    try:
        mid = MidModel(
            base=mid_base,
            random=random.randint(1, mid_random_max),
            tag="user_id",
            create_ts=now.timestamp,
            ts=now.datetime
        )
        db.add(mid)
        db.flush()

        user_id = mid_orm.mid_to_int(mid)

        m_user = UserModel(
            id=user_id,
            code=mobile_code,
            mobile=mobile_number,
            password=password,
            create_ts=now.timestamp
        )
        db.add(m_user)

        m_user_info = UserInfoModel(
            user_id=user_id,
            mobile=mobile_number,
            child_relation=0
        )
        db.add(m_user_info)

        db.commit()

    except Exception as e:
        db.rollback()
        # TODO: LOG
        print('create_user_transaction', str(e))
        raise

    return m_user, m_user_info


def upsert_user_info(
            db: Session, user_id: int,
            id_card_no: str = None, realname: str = None,
            mobile: str = None, child_relation: int = None,
            avatar_oss: str = None,
            nickname: str = None,
            born: bool = None):

    m_user_info = UserInfoModel(user_id=user_id)
    if id_card_no:
        m_user_info.id_card_no = id_card_no
    if realname:
        m_user_info.realname = realname
    if mobile:
        m_user_info.mobile = mobile
    if child_relation:
        m_user_info.child_relation = child_relation
    if avatar_oss:
        m_user_info.avatar_oss = avatar_oss
    if nickname is not None:
        m_user_info.nickname = nickname
    if born is not None:
        m_user_info.born = born

    m_user_info.update_ts = current_timestamp()

    db.merge(m_user_info)
    db.commit()
    return user_id


def find_child_by_id(db: Session, child_id: int) -> int:
    m_child = db.query(ChildModel).filter(ChildModel.id == child_id).first()
    return m_child


def find_child_ids_by_user_id(db, i_user_id):
    child_ids = db.query(UserChildModel.child_id).filter(
        UserChildModel.user_id == i_user_id,
        UserChildModel.status == 0
    ).all()
    return child_ids


def find_user_id_by_child_id(db, i_child_id):
    user_id = db.query(UserChildModel.user_id).filter(
        UserChildModel.child_id == i_child_id,
        UserChildModel.status == 0
    ).first()
    return user_id


def find_children_by_ids(db, ids):
    m_children = db.query(ChildModel).filter(ChildModel.id.in_(ids)).all()
    return m_children


def find_children_by_user_id(db, i_user_id):
    child_ids = find_child_ids_by_user_id(db, i_user_id)
    return find_children_by_ids(db, child_ids)


def create_child_transaction(
        db: Session, user_id: str,
        id_card_no: str = None,
        realname: str = None,
        nickname: str = None,
        birth_ts: int = None,
        gender: int = None) -> int:

    try:
        m_child = ChildModel(
            id_card_no=id_card_no,
            realname=realname,
            nickname=nickname,
            birth_ts=birth_ts,
            gender=gender,
            status=0,
            create_ts=current_timestamp()
        )
        db.add(m_child)
        db.flush()

        m_user_child = UserChildModel(
            user_id=user_id, child_id=m_child.id, create_ts=current_timestamp()
        )
        db.add(m_user_child)
        db.commit()

    except Exception as e:
        # TODO: LOG exception

        db.rollback()
        print(e)
        child_id = m_child.id if m_child else None
        raise ORMCreateChildFailed(user_id, child_id)

    return m_child.id


def update_child(
        db: Session,
        user_id: int, child_id: int,
        id_card_no: str = None, realname: str = None,
        nickname: str = None,
        birth_ts: int = None,
        gender: int = None) -> int:

    m_child = ChildModel(id=child_id)
    if id_card_no:
        m_child.id_card_no = id_card_no,
    if realname:
        m_child.realname = realname
    if nickname:
        m_child.nickname = nickname
    if birth_ts is not None:
        m_child.birth_ts = birth_ts
    if gender is not None:
        m_child.gender = gender
    m_child.update_ts = current_timestamp()

    db.merge(m_child)
    db.commit()

    return m_child


def soft_delete_child(db, i_user_id, i_child_id):
    m_user_child = db.query(UserChildModel).filter(
        UserChildModel.user_id == i_user_id,
        UserChildModel.child_id == i_child_id
    ).first()
    m_user_child.status = -1
    db.commit()


def user_child_count(db, i_user_id):
    count = db.query(UserChildModel).filter(
        UserChildModel.user_id == i_user_id,
        UserChildModel.status == 0
    ).count()
    return count


def find_guardians_by_user_id_and_id_card_no(
        db: Session, user_id: int, id_card_no: str) ->UserGuardianModel:
    m_guardian = db.query(UserGuardianModel).filter(
        UserGuardianModel.user_id == user_id,
        UserGuardianModel.id_card_no == id_card_no
    ).first()
    return m_guardian


def find_guardians_by_user_id(db: Session, user_id: int) ->List[UserGuardianModel]:
    m_guardians = db.query(UserGuardianModel).filter(
        UserGuardianModel.user_id == user_id
    ).all()
    return m_guardians


def create_user_guardian(db: Session, user_id: int,
                         id_card_no: str, realname: str, mobile: str) -> int:
    try:
        m_guardian = UserGuardianModel(
            user_id=user_id,
            id_card_no=id_card_no,
            realname=realname,
            mobile=mobile,
            create_ts=current_timestamp(),
            status=0
        )
        db.add(m_guardian)
        db.commit()
        return m_guardian

    except IntegrityError as exc:
        db.rollback()
        if is_duplicate_entry_exception(exc):
            return m_guardian
        else:
            raise


def upsert_user_identify(db, i_user_id, liveness_id, id_card_no, name, status,
                         id_card_image_oss=None, liveness_image_oss=None):

    m_user_identify = UserIdentityModel(
        user_id=i_user_id,
        id_card_no=id_card_no,
        name=name,
        liveness_id=liveness_id,
        status=status,
        id_card_image_oss=id_card_image_oss,
        liveness_image_oss=liveness_image_oss,
        create_ts=int(time.time())
    )
    db.merge(m_user_identify)
    result = db.commit()
    return result


def find_user_identity(db: Session, user_id: int):
    m_user_identity = db.query(UserIdentityModel).filter(
        UserIdentityModel.user_id == user_id
    ).first()
    return m_user_identity


def find_carer_info_by_user_id(db, i_user_id):
    m_carer_info = db.query(UserCarerInfoModel).filter(
        UserCarerInfoModel.user_id == i_user_id).first()
    return m_carer_info
