#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import \
    TINYINT, SMALLINT, INTEGER, BIGINT, \
    VARCHAR, TEXT, \
    DECIMAL, NUMERIC, \
    TIMESTAMP, DATE, DATETIME
from sqlalchemy.sql.schema import DefaultClause
from sqlalchemy.sql.elements import TextClause


_ = TINYINT
_ = SMALLINT
_ = INTEGER
_ = BIGINT
_ = VARCHAR
_ = TEXT
_ = DECIMAL
_ = NUMERIC
_ = TIMESTAMP
_ = DATE
_ = DATETIME


Base = declarative_base()


class ChildModel(Base):
    __tablename__ = 'child'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    id_card_no = Column('id_card_no', VARCHAR(length=18))
    realname = Column('realname', VARCHAR(length=16))
    nickname = Column('nickname', VARCHAR(length=16))
    birth_ts = Column('birth_ts', INTEGER(display_width=10))
    gender = Column('gender', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    status = Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10))
    update_ts = Column('update_ts', INTEGER(display_width=10))


class TimeSharingModel(Base):
    __tablename__ = 'time_sharing'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), nullable=False)
    child_age_min = Column('child_age_min', INTEGER(display_width=11), nullable=False, comment='接待孩子最小年龄')
    child_age_max = Column('child_age_max', INTEGER(display_width=11), nullable=False, comment='接待孩子最大年龄')
    child_count_max = Column('child_count_max', INTEGER(display_width=11), nullable=False, comment='最多接待多少孩子')
    address_id = Column('address_id', INTEGER(display_width=11, unsigned=True), nullable=False, comment='活动地址 id')
    city_id = Column('city_id', INTEGER(display_width=11))
    start_ts = Column('start_ts', INTEGER(display_width=10), nullable=False)
    end_ts = Column('end_ts', INTEGER(display_width=10), nullable=False)
    price = Column('price', INTEGER(display_width=11), nullable=False)
    activity = Column('activity', VARCHAR(length=64), server_default=DefaultClause(TextClause("''")), comment='活动内容标签')
    description = Column('description', VARCHAR(length=128), server_default=DefaultClause(TextClause("''")), comment='详细描述')
    accompany_required = Column('accompany_required', TINYINT(display_width=4), nullable=False, server_default=DefaultClause(TextClause('1')), comment='是否必须家人陪同')
    child_count = Column('child_count', INTEGER(display_width=11), nullable=False, comment='已报名孩子数量')
    status = Column('status', TINYINT(display_width=4), server_default=DefaultClause(TextClause('0')), comment='0 正常 -1 删除')
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))


class TimeSharingOrderModel(Base):
    __tablename__ = 'time_sharing_order'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False)
    order_no = Column('order_no', INTEGER(display_width=10), comment='订单号')
    buyer_id = Column('buyer_id', INTEGER(display_width=11), nullable=False, comment='下单user_id')
    guardian_id = Column('guardian_id', INTEGER(display_width=11), comment='guardian的 user_id')
    guardian_name = Column('guardian_name', VARCHAR(length=16), nullable=False)
    guardian_id_card_no = Column('guardian_id_card_no', VARCHAR(length=18), nullable=False)
    guardian_mobile = Column('guardian_mobile', VARCHAR(length=11), nullable=False)
    child_id = Column('child_id', INTEGER(display_width=11), comment='参加活动的child_id')
    child_nickname = Column('child_nickname', VARCHAR(length=16), nullable=False)
    child_name = Column('child_name', VARCHAR(length=16), nullable=False)
    child_id_card_no = Column('child_id_card_no', VARCHAR(length=18), nullable=False)
    time_sharing_id = Column('time_sharing_id', INTEGER(display_width=20), nullable=False)
    start_ts = Column('start_ts', INTEGER(display_width=10), nullable=False, comment='活动开始ts')
    end_ts = Column('end_ts', INTEGER(display_width=10), nullable=False, comment='活动结束ts')
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='订单状态 1 待支付 2 进行中（已支付） 3 已取消 4 已完成 5 已关闭 ')
    refund_status = Column('refund_status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='退款状态 0 无退款 1 退款中 2 已退款 ')
    fund_status = Column('fund_status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='退款状态 0 无放款 1放款中 2 已放款')
    seller_id = Column('seller_id', INTEGER(display_width=11), nullable=False)
    address_id = Column('address_id', INTEGER(display_width=11), nullable=False)
    city_id = Column('city_id', INTEGER(display_width=11))
    insurance_id = Column('insurance_id', INTEGER(display_width=11))
    remark = Column('remark', VARCHAR(length=100))
    cancel_reason = Column('cancel_reason', TINYINT(display_width=3), server_default=DefaultClause(TextClause('0')), comment='取消原因 家长：100 订单有误 101 已和看护人沟通 102 计划有变 103 其他 看护人：200')
    create_ts = Column('create_ts', INTEGER(display_width=10), nullable=False, server_default=DefaultClause(TextClause('0')))
    payment_ts = Column('payment_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    update_ts = Column('update_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    finish_ts = Column('finish_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    close_ts = Column('close_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('order_no', Column('order_no', INTEGER(display_width=10), comment='订单号'), unique=True),
    )


class UserModel(Base):
    __tablename__ = 'user'
    id = Column('id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    code = Column('code', VARCHAR(length=8), nullable=False)
    mobile = Column('mobile', VARCHAR(length=11), nullable=False, server_default=DefaultClause(TextClause('0')))
    password = Column('password', VARCHAR(length=64), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=11, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('create_ts_status', Column('create_ts', INTEGER(display_width=11, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0'))), Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))),
        Index('mobile_UNIQUE', Column('mobile', VARCHAR(length=11), nullable=False, server_default=DefaultClause(TextClause('0'))), Column('code', VARCHAR(length=8), nullable=False), unique=True),
    )


class UserAddressModel(Base):
    __tablename__ = 'user_address'
    id = Column('id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), comment='用户 id')
    lat = Column('lat', DECIMAL(precision=10, scale=6), comment='纬度')
    lng = Column('lng', DECIMAL(precision=10, scale=6), comment='经度')
    province = Column('province', VARCHAR(length=8), DefaultClause(TextClause("''")), comment='省/直辖市 如:北京市')
    city = Column('city', VARCHAR(length=12), DefaultClause(TextClause("''")), comment='城市 如:北京市')
    city_id = Column('city_id', INTEGER(display_width=11))
    district = Column('district', VARCHAR(length=8), DefaultClause(TextClause("''")), comment='区 如:海淀区')
    address = Column('address', VARCHAR(length=64), comment='街道地址 如:亮马桥路27号院1903号')
    name = Column('name', VARCHAR(length=32), DefaultClause(TextClause("''")), comment='住宅、建筑、公司等名称 如:大鱼公司')
    room = Column('room', VARCHAR(length=32), DefaultClause(TextClause("''")), comment='用户填写的房间号 如:2楼2018室')
    poi = Column('poi', VARCHAR(length=40), DefaultClause(TextClause("''")), comment='第三方 SDK 给的 Point of Interest')
    status = Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10))
    __table_args__ = (
        Index('user_address_user_id_city_district_address_name_room', 'user_id', 'city', 'district', 'address', 'name', 'room', unique=True),
    )


class CarerApplicationModel(Base):
    __tablename__ = 'carer_application'
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), primary_key=True, autoincrement=False)
    intro_video_id = Column('intro_video_id', INTEGER(display_width=11, unsigned=True), nullable=False, comment='个人视频 id')
    playground_video_id = Column('playground_video_id', INTEGER(display_width=11, unsigned=True), comment='场地视频 id')
    extra_video_ids = Column('extra_video_ids', VARCHAR(length=64), server_default=DefaultClause(TextClause("''")), comment='其他视频 id 逗号分割的字符列表 如 1,2,3')
    address_id = Column('address_id', INTEGER(display_width=11, unsigned=True), comment='地址 id')
    birth_certificate_oss = Column('birth_certificate_oss', VARCHAR(length=255), comment='出生证明文件 OSS 路径')
    care_exp = Column('care_exp', INTEGER(display_width=11), server_default=DefaultClause(TextClause('0')), comment='带娃经验(年)')
    degree = Column('degree', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='学历 0 无 1 专科 2 本科 3 硕士 4 博士')
    child_count_max = Column('child_count_max', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='最多接待多少孩子')
    child_age_min = Column('child_age_min', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='接待孩子最小年龄')
    child_age_max = Column('child_age_max', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='接待孩子最大年龄')
    result = Column('result', TINYINT(display_width=1), nullable=False, comment='不通过原因 | 0 审核通过 | 1 视频涉黄 | 2 视频涉政 | 3 视频涉暴恐 | 4 经验认证未通过 | 5 介绍视频没有看护人 | 6 介绍内容不符合要求 | 7 场地不符合要求')
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='-1 删除 0 审核中 1 通过 2 拒绝 3 失效')
    create_ts = Column('create_ts', INTEGER(display_width=10))
    update_ts = Column('update_ts', INTEGER(display_width=10))


class UserCarerInfoModel(Base):
    __tablename__ = 'user_carer_info'
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False, autoincrement=False)
    intro_video_id = Column('intro_video_id', INTEGER(display_width=11, unsigned=True), nullable=False, comment='个人视频 id')
    playground_video_id = Column('playground_video_id', INTEGER(display_width=11, unsigned=True), nullable=False, comment='场地视频 id')
    extra_video_ids = Column('extra_video_ids', VARCHAR(length=64), server_default=DefaultClause(TextClause("''")), nullable=False, comment='其他视频 id 逗号分割的字符列表 如 1,2,3')
    address_id = Column('address_id', INTEGER(display_width=11, unsigned=True), comment='地址 id')
    city_id = Column('city_id', INTEGER(display_width=11))
    lat = Column('lat', DECIMAL(precision=10, scale=6), comment='纬度')
    lng = Column('lng', DECIMAL(precision=10, scale=6), comment='经度')
    birth_certificate_oss = Column('birth_certificate_oss', VARCHAR(length=255), comment='出生证明文件 OSS 路径')
    degree = Column('degree', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='学历 0 无 1 专科 2 本科 3 硕士 4 博士')
    care_exp = Column('care_exp', INTEGER(display_width=11), server_default=DefaultClause(TextClause('0')), comment='带娃经验(年)')
    child_count_max = Column('child_count_max', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='最多接待多少孩子')
    child_age_min = Column('child_age_min', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='接待孩子最小年龄')
    child_age_max = Column('child_age_max', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='接待孩子最大年龄')
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='0 正常 -1 删除')
    update_ts = Column('update_ts', INTEGER(display_width=10))


class UserChildModel(Base):
    __tablename__ = 'user_child'
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), primary_key=True)
    child_id = Column('child_id', INTEGER(display_width=11, unsigned=True), primary_key=True)
    create_ts = Column('create_ts', INTEGER(display_width=10))
    status = Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('user_child_user_id_child_id_status_uindex', Column('user_id', INTEGER(display_width=11)), Column('child_id', INTEGER(display_width=11)), Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0'))), unique=True),
    )


class UserGuardianModel(Base):
    __tablename__ = 'user_guardian'
    id = Column('id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), nullable=False)
    id_card_no = Column('id_card_no', VARCHAR(length=18), nullable=False)
    realname = Column('realname', VARCHAR(length=16), nullable=False)
    mobile = Column('mobile', VARCHAR(length=11))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('user_guardian_id_card_no_UNIQUE', Column('id_card_no', VARCHAR(length=12)), unique=True),
    )


class UserIdentityModel(Base):
    __tablename__ = 'user_identity'
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False, autoincrement=False)
    id_card_no = Column('id_card_no', VARCHAR(length=18), nullable=False)
    name = Column('name', VARCHAR(length=16), nullable=False)
    liveness_id = Column('liveness_id', VARCHAR(length=36))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    id_card_image_oss = Column('id_card_image_oss', VARCHAR(length=255))
    liveness_image_oss = Column('liveness_image_oss', VARCHAR(length=255))
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))


class UserInfoModel(Base):
    __tablename__ = 'user_info'
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False, autoincrement=False)
    id_card_no = Column('id_card_no', VARCHAR(length=18))
    realname = Column('realname', VARCHAR(length=16))
    mobile = Column('mobile', VARCHAR(length=11))
    child_relation = Column('child_relation', TINYINT(display_width=4))
    degree = Column('degree', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    nickname = Column('nickname', VARCHAR(length=32))
    country = Column('country', SMALLINT(display_width=6), server_default=DefaultClause(TextClause('1')))
    status = Column('status', TINYINT(display_width=4), server_default=DefaultClause(TextClause('0')))
    update_ts = Column('update_ts', INTEGER(display_width=10))
    avatar_oss = Column('avatar_oss', VARCHAR(length=255))
    born = Column('born', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))


class VideoModel(Base):
    __tablename__ = 'video'
    id = Column('id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    cloud = Column('cloud', VARCHAR(length=16), nullable=False)
    bucket = Column('bucket', VARCHAR(length=64), nullable=False)
    key = Column('key', VARCHAR(length=128), nullable=False)
    etag = Column('etag', VARCHAR(length=32))
    mime_type = Column('mime_type', VARCHAR(length=16))
    size = Column('size', INTEGER(display_width=10, unsigned=True))
    duration = Column('duration', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    width = Column('width', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    height = Column('height', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    persistent_id = Column('persistent_id', VARCHAR(length=32))
    pfop_vframe_status = Column('pfop_vframe_status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    pfop_transcode_status = Column('pfop_transcode_status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('video_cloud_bucket_key_index_unique', 'cloud', 'bucket', 'key', unique=True),
    )


class UserFollowModel(Base):
    __tablename__ = 'user_follow'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False)
    from_user_id = Column('from_user_id', INTEGER(display_width=11), nullable=False)
    to_user_id = Column('to_user_id', INTEGER(display_width=11), nullable=False)
    city_id = Column('city_id', INTEGER(display_width=11))
    status = Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    update_ts = Column('update_ts', INTEGER(display_width=11), server_default=DefaultClause(TextClause('0')))


class UserLikeModel(Base):
    __tablename__ = 'user_like'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False)
    from_user_id = Column('from_user_id', INTEGER(display_width=11), nullable=False)
    to_user_id = Column('to_user_id', INTEGER(display_width=11), nullable=False)
    city_id = Column('city_id', INTEGER(display_width=11))
    status = Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    update_ts = Column('update_ts', INTEGER(display_width=11), server_default=DefaultClause(TextClause('0')))


class WalletModel(Base):
    __tablename__ = 'wallet'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    customer_id = Column('customer_id', INTEGER(display_width=11))
    balance = Column('balance', INTEGER(display_width=11))
    freezed = Column('freezed', INTEGER(display_width=11))
    cashable = Column('cashable', INTEGER(display_width=11))
    uncashable = Column('uncashable', INTEGER(display_width=11))
    update_ts = Column('update_ts', INTEGER(display_width=10))
    __table_args__ = (
        Index('customer_id_UNIQUE', Column('customer_id', INTEGER(display_width=11)), unique=True),
    )


class CityModel(Base):
    __tablename__ = 'city'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    name = Column('name', VARCHAR(length=16), nullable=False)
    pinyin = Column('pinyin', VARCHAR(length=64))


class MidModel(Base):
    __tablename__ = 'mid'
    auto = Column('auto', INTEGER(display_width=11), autoincrement=True, primary_key=True, nullable=False)
    base = Column('base', INTEGER(display_width=11), primary_key=True)
    random = Column('random', INTEGER(display_width=11), primary_key=True)
    tag = Column('tag', VARCHAR(length=16))
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    ts = Column('ts', TIMESTAMP(), server_default=DefaultClause(TextClause('CURRENT_TIMESTAMP')))
    __table_args__ = (
        Index('mid_auto_base_random', 'auto', 'base', 'random', unique=True),
    )
