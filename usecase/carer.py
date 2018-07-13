#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict

from sqlalchemy.orm import Session

from api.schema import ObjectInfo, CarerApplyRequestData
from util import qiniu
from config.const import IdentityVerificationStatus, CarerApplicationStatus
from entity import Facade
from orm import address as address_orm
from orm import carer as carer_orm
from orm import user as user_orm
from orm import video as video_orm
from util import DictObject, ui
from wrong import exception

# TODO: REFACTOR
from orm.orm_mysql import VideoModel, UserAddressModel


def _video_orm_to_dict(v: VideoModel) -> dict:
    return DictObject(
        key=v.key,
        mime_type=v.mime_type,
        etag=v.etag,
        size=v.size,
        width=v.width,
        height=v.height,
        duration=v.duration,
        cover_url=qiniu.url(Facade.config["qiniu"]["category"]["vframe"]["bucket"], v.key),
        video_url=qiniu.url(v.bucket, v.key)
    )


def _upsert_video(db: Session, user_id: int, reftag: str, req_video: ObjectInfo) -> int:
    # `cloud` 写死 -> qiniu
    cloud = 'qiniu'
    bucket = Facade.config["qiniu"]["category"]["video"]["bucket"]
    m_video = video_orm.find_video_by_oss_path(db, cloud, bucket, req_video.key)
    if not m_video:
        m_video = video_orm.create_video(
            db, cloud, bucket, req_video.key,
            etag=req_video.etag, mime_type=req_video.mime_type,
            size=req_video.size, duration=req_video.duration,
            width=req_video.width, height=req_video.height,
            persistent_id=req_video.persistent_id
        )
    return m_video.id


def retrieve_carer_videos(db: Session, m_carer) -> Dict[str, dict]:
    intro_video = video_orm.find_video_by_id(db, m_carer.intro_video_id)
    playground_video = video_orm.find_video_by_id(db, m_carer.playground_video_id)
    extra_videos = [
        video_orm.find_video_by_id(db, int(i)) for i in m_carer.extra_video_ids.split(",")
    ] if m_carer.extra_video_ids else []
    return {
        'intro': _video_orm_to_dict(intro_video) if intro_video else None,
        'playground': _video_orm_to_dict(playground_video) if playground_video else None,
        'extra': [_video_orm_to_dict(v) for v in extra_videos]
    }


def videos_dict_to_list(videos: Dict[str, dict]) -> List[dict]:
    videos_list = []
    intro_video = videos.get("intro")
    if intro_video:
        videos_list.append(intro_video)
    playground_video = videos.get("playground")
    if playground_video:
        videos_list.append(playground_video)
    videos_list += videos.get("extra", [])
    return videos_list


def retrieve_carer_application(db: Session, user_id: int, detail: bool=True) -> dict:

    m_carer_application = carer_orm.find_care_application_by_user_id(db, user_id)
    if not m_carer_application:
        return None

    if not detail:
        return m_carer_application

    # Make up videos.
    videos = retrieve_carer_videos(db, m_carer_application)

    # Get address.
    m_address = address_orm.find_user_address_by_id(db, m_carer_application.address_id)
    if not m_address:
        m_address = UserAddressModel()

    identify_result = False
    m_identity = user_orm.find_user_identity(db, user_id)
    if m_identity and (m_identity.status == IdentityVerificationStatus.Passed.value):
        identify_result = True

    birth_certificate = None
    birth_certificate_url = ''
    if m_carer_application.birth_certificate_oss:
        birth_certificate = dict(
            key=m_carer_application.birth_certificate_oss.split(":")[2]
        )
        birth_certificate_url = qiniu.private_url(
            qiniu.url_from_path(m_carer_application.birth_certificate_oss)
        )

    result = DictObject(
        status=m_carer_application.status,
        result=m_carer_application.result,
        video=videos,
        degree=m_carer_application.degree,
        address=DictObject(
            lat=m_address.lat,
            lng=m_address.lng,
            city=m_address.city,
            address=m_address.address,
            name=m_address.name,
            room=m_address.room,
            poi_id=m_address.poi,
        ),
        child_count=m_carer_application.child_count_max,
        child_age_min=m_carer_application.child_age_min,
        child_age_max=m_carer_application.child_age_max,
        identify_result=identify_result,
        birth_certificate=birth_certificate,
        birth_certificate_url=birth_certificate_url,
    )

    return result


def submit_carer_application(
        db: Session, user_id: int,
        apply_data: CarerApplyRequestData) -> int:

    # Precondition
    # 1 realname verification passed 已通过实名认证
    m_identity = user_orm.find_user_identity(db, user_id)
    if not m_identity or (m_identity.status != IdentityVerificationStatus.Passed.value):
        raise exception.CarerApplicationIdentityNotVerified(user_id)

    # Precondition
    # 2 no reviewing application record 没有正在审核中的申请记录
    m_reviewing_application = carer_orm.find_care_application_by_user_id(
        db, user_id, CarerApplicationStatus.Reviewing.value
    )
    if m_reviewing_application:
        raise exception.CarerApplicationAlreadyApplied(user_id)

    # 1. Create videos if not existed
    videos = apply_data.video

    intro_video_id = _upsert_video(db, user_id, 'intro', videos.intro) \
        if videos.intro else None
    playground_video_id = _upsert_video(db, user_id, 'playground', videos.playground) \
        if videos.playground else None
    extra_video_ids = [_upsert_video(db, user_id, 'extra', v) for v in videos.extra] \
        if videos.extra else []

    # 2. Create Address record if not existed
    addr = apply_data.address

    # Get `city_id` from `city_name`
    if addr.city_id:
        city_id = (addr.city_id // 100) * 100  # 参考GB码 -> 市GB码
    else:
        m_city = address_orm.find_city_by_name(db, addr.city)
        city_id = m_city.id if m_city else None

    m_address = address_orm.create_user_address(
        db, user_id,
        lat=addr.lat, lng=addr.lng,
        province=addr.province,
        city=addr.city, city_id=city_id,
        district=addr.district,
        address=addr.address, name=addr.name, room=addr.room,
        poi=addr.poi_id
    )

    # 3. Calculate caring experience.
    birth_certificate = apply_data.birth_certificate
    birth_certificate_image_oss = '{}:{}:{}'.format(
        'qiniu', Facade.config["qiniu"]["category"]["birth"]["bucket"], birth_certificate.key
    )
    care_exp_from_children_age = 0
    m_children = user_orm.find_children_by_user_id(db, user_id)
    if m_children:
        care_exp_from_children_age = max(
            ui.calculate_age(c.birth_ts) if c.birth_ts else 0 for c in m_children
        )

    m_carer_application = carer_orm.create_carer_application_transaction(
        db, user_id,
        intro_video_id,
        playground_video_id,
        extra_video_ids,
        m_address.id,
        birth_certificate_image_oss,
        apply_data.degree,
        care_exp_from_children_age,
        apply_data.child_count,
        apply_data.child_age_min,
        apply_data.child_age_max,
    )

    return m_carer_application.user_id


def approve_carer_application(db: Session, user_id: int):
    carer_orm.approve_carer_application_transaction(db, user_id)


def retrieve_care_info(db: Session, user_id: int) -> dict:

    m_carer_info = user_orm.find_carer_info_by_user_id(db, user_id)
    if not m_carer_info:
        return None

    # Get address.
    m_address = address_orm.find_user_address_by_id(db, m_carer_info.address_id)

    # Make up videos.
    videos = retrieve_carer_videos(db, m_carer_info)

    identified = False
    m_identity = user_orm.find_user_identity(db, user_id)
    if m_identity and (m_identity.status == IdentityVerificationStatus.Passed.value):
        identified = True

    result = DictObject(
        user_id=m_carer_info.user_id,
        identified=identified,
        videos=videos,
        degree=m_carer_info.degree,
        care_exp=m_carer_info.care_exp,
        child_age_min=m_carer_info.child_age_min,
        child_age_max=m_carer_info.child_age_max,
        address=DictObject(
            lat=m_address.lat,
            lng=m_address.lng,
            city=m_address.city,
            address=m_address.address,
            name=m_address.name,
            room=m_address.room
        ),
        city_id=m_carer_info.city_id
    )

    return result
