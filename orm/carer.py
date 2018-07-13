#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
from sqlalchemy.orm import Session

from config.const import CarerApplicationStatus
from orm.orm_mysql import CarerApplicationModel, UserCarerInfoModel
from util import current_timestamp
from wrong import exception


def create_carer_application_transaction(
        db: Session, user_id: int,
        intro_video_id: int, playground_video_id: int, extra_video_ids: List[int],
        address_id: int,
        birth_certificate_oss: str,
        degree: int,
        care_exp: int,
        child_count_max: int,
        child_age_min: int,
        child_age_max: int) -> CarerApplicationModel:

    try:
        """
        # 1. Set Reviewing applications to Disabled
        reviewing_applications = db.query(CarerApplicationModel).filter(
            CarerApplicationModel.user_id == user_id,
            CarerApplicationModel.status==CarerApplicationStatus.Reviewing.value
        ).all()
        for r in reviewing_applications:
            r.status = CarerApplicationStatus.Disabled.value
        """

        application = CarerApplicationModel(
            user_id=user_id,
            intro_video_id=intro_video_id,
            playground_video_id=playground_video_id,
            extra_video_ids=','.join([str(i) for i in extra_video_ids]),
            address_id=address_id,
            birth_certificate_oss=birth_certificate_oss,
            degree=degree,
            care_exp=care_exp,
            child_count_max=child_count_max,
            child_age_min=child_age_min,
            child_age_max=child_age_max,
            create_ts=current_timestamp(),
            status=CarerApplicationStatus.Reviewing.value
        )
        db.merge(application)

        db.commit()

        return application

    except Exception as e:
        # TODO: LOG
        print('create_carer_application_transaction', str(e))

        db.rollback()
        raise


def find_care_application_by_user_id(
        db: Session, user_id: int, status: int = None) ->CarerApplicationModel:
    if status is None:
        m = db.query(CarerApplicationModel).filter(
            CarerApplicationModel.user_id == user_id
        ).first()
    else:
        m = db.query(CarerApplicationModel).filter(
            CarerApplicationModel.user_id == user_id,
            CarerApplicationModel.status == status,
        ).first()
    return m


def approve_carer_application_transaction(db: Session, user_id: int):

    application = db.query(CarerApplicationModel).filter(
        CarerApplicationModel.user_id == user_id
    ).first()
    if not application:
        raise exception.NonExistentCarerApplication(user_id, None)

    try:
        # 1. Copy carer info from `carer_application` to `user_carer_info`
        carer_info = UserCarerInfoModel(
            user_id=user_id,
            intro_video_id=application.intro_video_id,
            playground_video_id=application.playground_video_id,
            extra_video_ids=application.extra_video_ids,
            address_id=application.address_id,
            birth_certificate_oss=application.birth_certificate_oss,
            degree=application.degree,
            care_exp=application.care_exp,
            child_count_max=application.child_count_max,
            child_age_min=application.child_age_min,
            child_age_max=application.child_age_max,
            update_ts=current_timestamp()
        )
        db.merge(carer_info)

        # 2. Set `carer_application` record status to `Approved`
        application.status = CarerApplicationStatus.Approved.value
        application.update_ts = current_timestamp()

        db.commit()

    except Exception as e:
        # TODO: LOG
        print('approve_carer_application_transaction', str(e))

        db.rollback()
        raise


def find_carer_locations_by_city_ids(db: Session, city_ids: List[int]) -> List:
    result = db.query(
        UserCarerInfoModel.user_id,
        UserCarerInfoModel.city_id,
        UserCarerInfoModel.lat,
        UserCarerInfoModel.lng
    ).filter(
        UserCarerInfoModel.city_id.in_(city_ids),
        UserCarerInfoModel.status == 0
    ).all()
    return result


def find_carer_city_info_by_user_id(db: Session, user_id: int):
    result = db.query(
        UserCarerInfoModel.user_id,
        UserCarerInfoModel.city_id,
    ).filter(
        UserCarerInfoModel.user_id == user_id,
        UserCarerInfoModel.status == 0
    ).first()
    return result
