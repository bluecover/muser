#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session

from api.schema import ObjectInfo
from entity import Facade, subject
from orm import user as user_model
from usecase import guardian as guardian_usecase
from usecase import identity as identity_usecase
from wrong import exception


def retrieve_user_info(db: Session, user_id: int) -> subject.UserInfo:
    m_user_info = user_model.find_user_info_by_id(db, user_id)
    if not m_user_info:
        return None
    user_info = subject.UserInfo.from_object(m_user_info)

    if not user_info.nickname:
        user_info.nickname = guardian_usecase.update_guardian_nickname(
            db, user_id, m_user_info.child_relation
        )

    return user_info


def update_user_info(
        db: Session, user_id: int, id_card_no: str, realname: str,
        mobile: str, child_relation: int, avatar: ObjectInfo = None):

    # 身份证号 和 姓名 必须都有, 否则无法进行实名认证
    if (id_card_no and not realname) or (not id_card_no and realname):
        raise exception.InvalidIDCardNumber(user_id, id_card_no, realname)

    if id_card_no:
        m_existing = user_model.find_user_info_by_id(db, user_id)
        if m_existing and m_existing.id_card_no:
            raise exception.IDCardNumberOrRealnameAlreadyExisted(
                user_id, id_card_no, realname
            )
        id_card_info = identity_usecase.verify_and_parse_id_card_no(
            user_id, id_card_no, realname
        )
        if not id_card_info:
            raise exception.InvalidIDCardNumber(user_id, id_card_no, realname)

    avatar_oss = ""
    if avatar:
        avatar_oss = ":".join(
            ["qiniu", Facade.config["qiniu"]["category"]["avatar"]["bucket"], avatar.key]
        )
        """
        from kombu.exceptions import OperationalError as KombuOperationalError  # noqa
        from entity import Facade as EntityFacade  # noqa
        try:
            oss_provider = EntityFacade.oss_provider
            oss_provider.add_object_reference(i_user_id, "avatar", avatar)
        except KombuOperationalError as err:
            print("add_object_reference", err)
        """

    if child_relation:
        # Evict nickname if `child_relation` is to be updated
        result = user_model.upsert_user_info(
            db, user_id, id_card_no, realname, mobile, child_relation, avatar_oss,
            nickname=""
        )
    else:
        result = user_model.upsert_user_info(
            db, user_id, id_card_no, realname, mobile, child_relation, avatar_oss,
        )

    return result


def store_preset_user_info(
        db: Session, user_id: int,
        born: bool,
        nickname: str,
        relation: int,
        birth_ts: int = None,
        gender: int = None):

    user_model.upsert_user_info(db, user_id, child_relation=relation, born=born, nickname='')

    user_model.create_child_transaction(
        db, user_id,
        nickname=nickname,
        birth_ts=birth_ts,
        gender=gender
    )
