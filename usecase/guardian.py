#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from sqlalchemy.orm import Session

from config.const import CHILD_RELATION_INT2CN
from orm import user as orm_user
from usecase import identity as identity_usecase
from util import ui
from wrong import exception


def retrieve_guardian_nickname(db: Session, user_id: int) -> str:
    m_user_info = orm_user.find_user_info_by_id(db, user_id)
    if not m_user_info:
        return None
    if m_user_info.nickname:
        return m_user_info.nickname
    return update_guardian_nickname(db, user_id, m_user_info.child_relation)


def update_guardian_nickname(db: Session, user_id: int, child_relation: int) -> str:
    if not user_id:
        return None
    if not child_relation:
        m_user_info = orm_user.find_user_info_by_id(db, user_id)
        if not m_user_info:
            return None
        child_relation = m_user_info.child_relation

    m_children = orm_user.find_children_by_user_id(db, user_id)
    nickname = ui.build_family_nickname(
        CHILD_RELATION_INT2CN[child_relation], [c.nickname for c in m_children]
    )

    orm_user.upsert_user_info(db, user_id, nickname=nickname)

    return nickname


# Evict `nickname` of a user(guardian) by set it to empty.
def evict_guardian_nickname(db: Session, user_id: int):
    if not user_id:
        return None
    orm_user.upsert_user_info(db, user_id, nickname='')


def retrieve_guardians_by_user_id(
        db: Session, user_id: int) -> List[orm_user.UserGuardianModel]:
    m_guardians = orm_user.find_guardians_by_user_id(db, user_id)
    return m_guardians


def create_guardian(
        db: Session, user_id: int, id_card_no: str, realname: str, mobile: str) -> int:

    existing = orm_user.find_guardians_by_user_id_and_id_card_no(
        db, user_id, id_card_no
    )
    if existing:
        raise exception.IDCardNumberAlreadyExisted(user_id, id_card_no)

    verify_result = identity_usecase.identify_validity(user_id, id_card_no, realname)
    if not verify_result:
        raise exception.InvalidIDCardNumber(user_id, id_card_no, realname)

    return orm_user.create_user_guardian(db, user_id, id_card_no, realname, mobile)
