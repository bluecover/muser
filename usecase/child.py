#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import arrow
from typing import List

from sqlalchemy.orm import Session

from entity.subject import Child
from config.const import CHILD_GENDER_INT2CN
from orm import user as user_model
from usecase import guardian as guardian_usecase
from usecase import identity as identity_usecase
from util.ui import calculate_age, obscure_id_card_no
from wrong import exception


def retrieve_children_by_user_id(db: Session, user_id: int) -> List[Child]:
    child_ids = user_model.find_child_ids_by_user_id(db, user_id)
    m_children = user_model.find_children_by_ids(db, child_ids)
    children = []
    for m_child in m_children:
        # TODO: SUBJECT.Child ?
        child = Child.from_object(m_child)
        child.gender = CHILD_GENDER_INT2CN[m_child.gender if m_child.gender else 0]
        child.age = calculate_age(m_child.birth_ts) if m_child.birth_ts else 0
        child.id_card_no = obscure_id_card_no(m_child.id_card_no) if m_child.id_card_no else ''
        children.append(child)
    return children


def create_or_update_child(
        db: Session,
        user_id: int,
        child_id: int = None,
        id_card_no: str = None,
        realname: str = None,
        nickname: str = None) -> int:
    """ Create child if `child_id` is None.
        Update child if `child_id` is not None.
    """
    if not child_id:
        result = create_child_transaction(
            db, user_id,
            id_card_no=id_card_no, realname=realname,
            nickname=nickname
        )
    else:
        result = update_child(
            db, user_id, child_id,
            id_card_no=id_card_no, realname=realname,
            nickname=nickname
        )

    if nickname or not child_id:
        guardian_usecase.evict_guardian_nickname(db, user_id)

    return result


def create_child_transaction(
        db: Session,
        user_id: int,
        id_card_no: str = None,
        realname: str = None,
        nickname: str = None) -> int:

    # 身份证号 和 姓名 必须都有, 否则无法进行实名认证
    if (id_card_no and not realname) or (not id_card_no and realname):
        raise exception.InvalidIDCardNumber(user_id, id_card_no, realname)

    # 生日 和 性别 由身份证号解析得出
    # 如果暂时没有身份证号 就用默认值
    birth_ts = None
    gender = 0

    if id_card_no:
        id_card_info = identity_usecase.verify_and_parse_id_card_no(user_id, id_card_no, realname)
        if not id_card_info:
            raise exception.InvalidIDCardNumber(user_id, id_card_no, realname)
        birth_ts = arrow.get(id_card_info.date_birth).timestamp
        gender = id_card_info.gender

    result_id = user_model.create_child_transaction(
        db, user_id,
        id_card_no=id_card_no,
        realname=realname,
        nickname=nickname,
        birth_ts=birth_ts,
        gender=gender
    )

    return result_id


def update_child(
        db: Session,
        user_id: int, child_id: int,
        id_card_no: str = None,
        realname: str = None,
        nickname: str = None) -> int:

    # 身份证号 和 姓名 必须都有, 否则无法进行实名认证
    if (id_card_no and not realname) or (not id_card_no and realname):
        raise exception.InvalidIDCardNumber(user_id, id_card_no, realname)

    m_existing = user_model.find_child_by_id(db, child_id)
    if not m_existing:
        raise exception.NonExistentChild(user_id, child_id)

    birth_ts = None
    gender = None

    # Update `id_card_no` and `realname` if not existing.
    if id_card_no:
        if not m_existing.id_card_no:
            id_card_info = identity_usecase.verify_and_parse_id_card_no(user_id, id_card_no, realname)
            if not id_card_info:
                raise exception.InvalidIDCardNumber(user_id, id_card_no, realname)
            birth_ts = arrow.get(id_card_info.date_birth).timestamp
            gender = id_card_info.gender
        else:
            raise exception.IDCardNumberOrRealnameAlreadyExisted(user_id, id_card_no, realname)

    result = user_model.update_child(
        db,
        user_id=user_id, child_id=child_id,
        nickname=nickname, realname=realname,
        id_card_no=id_card_no,
        birth_ts=birth_ts,
        gender=gender
    )

    return result.id


def delete_child(db: Session, user_id: int, child_id: int) -> bool:
    child_count = user_model.user_child_count(db, user_id)
    if child_count == 1:
        return False

    user_model.soft_delete_child(db, user_id, child_id)

    guardian_usecase.evict_guardian_nickname(db, user_id)

    return True
