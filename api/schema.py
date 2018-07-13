# -*- coding: utf-8 -*-

''' Generated codes

Marshmallow schema classes accord with model definitions in Swagger.
BE VERY CAREFUL to change this file manually.

'''

import marshmallow
from base import validator


''' SCHEMAS FROM QUERY PARAMETERS.
'''


class ParamAuthMobileCode(object):
    __slots__ = ['mobile', '_original_data']

    def __init__(self, mobile, original_data=None):
        self.mobile = mobile
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ParamAuthMobileCodeSchema(marshmallow.Schema):
    mobile = marshmallow.fields.String(required=True, validate=validator.v_mobile)  # 明文手机号

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ParamAuthMobileCode(**data)
        return obj


class ParamOssUploadToken(object):
    __slots__ = ['cloud', 'category', 'user', '_original_data']

    def __init__(self, cloud=None, category=None, user=None, original_data=None):
        self.cloud = cloud
        self.category = category
        self.user = user
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ParamOssUploadTokenSchema(marshmallow.Schema):
    cloud = marshmallow.fields.String()  # 云服务商 目前只用qiniu qiniu
    category = marshmallow.fields.String()  # 上传文件类别 avatar: 头像 video: 视频 identity: 识别 birth: 出生证
    user = marshmallow.fields.String()  # 用户 ID hello123

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ParamOssUploadToken(**data)
        return obj


class ParamOssDownloadUrl(object):
    __slots__ = ['cloud', 'domain', 'key', '_original_data']

    def __init__(self, cloud=None, domain=None, key=None, original_data=None):
        self.cloud = cloud
        self.domain = domain
        self.key = key
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ParamOssDownloadUrlSchema(marshmallow.Schema):
    cloud = marshmallow.fields.String()  # 云服务商 目前只用qiniu
    domain = marshmallow.fields.String()  # 公开的 base URL
    key = marshmallow.fields.String()  # 文件在 OSS 上的 bucket/key 存储路径

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ParamOssDownloadUrl(**data)
        return obj


class ParamUserCarerInfo(object):
    __slots__ = ['user_id', 'lng', 'lat', '_original_data']

    def __init__(self, user_id, lng=None, lat=None, original_data=None):
        self.user_id = user_id
        self.lng = lng
        self.lat = lat
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ParamUserCarerInfoSchema(marshmallow.Schema):
    user_id = marshmallow.fields.String(required=True)  # 看护人的用户ID 123
    lng = marshmallow.fields.Decimal()  # 经度 116.483765
    lat = marshmallow.fields.Decimal()  # 纬度 39.961914

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ParamUserCarerInfo(**data)
        return obj


class ParamUserFollowing(object):
    __slots__ = ['offset', 'limit', '_original_data']

    def __init__(self, offset=None, limit=None, original_data=None):
        self.offset = offset
        self.limit = limit
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ParamUserFollowingSchema(marshmallow.Schema):
    offset = marshmallow.fields.Integer(missing=0)  # 偏移
    limit = marshmallow.fields.Integer(missing=20)  # 数量

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ParamUserFollowing(**data)
        return obj


class ParamRecommendCarerHot(object):
    __slots__ = ['offset', 'limit', 'city_id', 'lat', 'lng', 'child_born', 'child_birth_ts', 'child_gender', 'child_relation', 'child_nickname', '_original_data']

    def __init__(self, offset=None, limit=None, city_id=None, lat=None, lng=None, child_born=None, child_birth_ts=None, child_gender=None, child_relation=None, child_nickname=None, original_data=None):
        self.offset = offset
        self.limit = limit
        self.city_id = city_id
        self.lat = lat
        self.lng = lng
        self.child_born = child_born
        self.child_birth_ts = child_birth_ts
        self.child_gender = child_gender
        self.child_relation = child_relation
        self.child_nickname = child_nickname
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ParamRecommendCarerHotSchema(marshmallow.Schema):
    offset = marshmallow.fields.Integer(missing=0)  # 偏移
    limit = marshmallow.fields.Integer(missing=5)  # 数量
    city_id = marshmallow.fields.Integer()  # 城市编号
    lat = marshmallow.fields.Decimal()
    lng = marshmallow.fields.Decimal()
    child_born = marshmallow.fields.Integer()  # 孩子是否已出生 1
    child_birth_ts = marshmallow.fields.Integer()  # 孩子出生日期 时间戳 北京时间 1523264525
    child_gender = marshmallow.fields.Integer()
    child_relation = marshmallow.fields.Integer()  # 用户和孩子的关系 2
    child_nickname = marshmallow.fields.String()  # 孩子的昵称 卖马的秦琼

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ParamRecommendCarerHot(**data)
        return obj


class ParamRecommendCarerNearby(object):
    __slots__ = ['offset', 'limit', 'city_id', 'lat', 'lng', 'child_born', 'child_birth_ts', 'child_gender', 'child_relation', 'child_nickname', '_original_data']

    def __init__(self, offset=None, limit=None, city_id=None, lat=None, lng=None, child_born=None, child_birth_ts=None, child_gender=None, child_relation=None, child_nickname=None, original_data=None):
        self.offset = offset
        self.limit = limit
        self.city_id = city_id
        self.lat = lat
        self.lng = lng
        self.child_born = child_born
        self.child_birth_ts = child_birth_ts
        self.child_gender = child_gender
        self.child_relation = child_relation
        self.child_nickname = child_nickname
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ParamRecommendCarerNearbySchema(marshmallow.Schema):
    offset = marshmallow.fields.Integer(missing=0)  # 偏移
    limit = marshmallow.fields.Integer(missing=5)  # 数量
    city_id = marshmallow.fields.Integer()  # 城市编号
    lat = marshmallow.fields.Decimal()
    lng = marshmallow.fields.Decimal()
    child_born = marshmallow.fields.Integer()  # 孩子是否已出生 1
    child_birth_ts = marshmallow.fields.Integer()  # 孩子出生日期 时间戳 北京时间 1523264525
    child_gender = marshmallow.fields.Integer()
    child_relation = marshmallow.fields.Integer()  # 用户和孩子的关系 2
    child_nickname = marshmallow.fields.String()  # 孩子的昵称 卖马的秦琼

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ParamRecommendCarerNearby(**data)
        return obj


''' SCHEMAS FROM MODEL DEFINITIONS.
'''


class Address(object):
    __slots__ = ['lat', 'lng', 'province', 'city', 'city_id', 'district', 'address', 'name', 'room', 'poi_id', '_original_data']

    def __init__(self, city, lat=None, lng=None, province=None, city_id=None, district=None, address=None, name=None, room=None, poi_id=None, original_data=None):
        self.lat = lat
        self.lng = lng
        self.province = province
        self.city = city
        self.city_id = city_id
        self.district = district
        self.address = address
        self.name = name
        self.room = room
        self.poi_id = poi_id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class AddressSchema(marshmallow.Schema):
    lat = marshmallow.fields.Decimal()  # example: 39.961914
    lng = marshmallow.fields.Decimal()  # example: 116.483765
    province = marshmallow.fields.String()  # 省份/直辖市 example: 北京市
    city = marshmallow.fields.String(required=True)  # 城市 example: 北京市
    city_id = marshmallow.fields.Integer()  # 城市编号 example: 110100
    district = marshmallow.fields.String()  # 区 example: 海淀区
    address = marshmallow.fields.String()  # 详细地址 example: 张自忠路3号段
    name = marshmallow.fields.String()  # 机构名 example: 段祺瑞执政府旧址
    room = marshmallow.fields.String()  # 用户填写的门牌号 example: 6号楼3单元202室
    poi_id = marshmallow.fields.String()  # point of interest example: eef2d5282cd7d5a73ae4a6b7

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = Address(**data)
        return obj


class AuthMobileCodeResponseData_Data(object):
    __slots__ = ['code', 'mobile', 'retry_time', '_original_data']

    def __init__(self, code=None, mobile=None, retry_time=None, original_data=None):
        self.code = code
        self.mobile = mobile
        self.retry_time = retry_time
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class AuthMobileCodeResponseData_DataSchema(marshmallow.Schema):
    code = marshmallow.fields.Integer()  # 登陆验证码 example: 9527
    mobile = marshmallow.fields.String()  # 待登陆手机号 example: 13611112222
    retry_time = marshmallow.fields.String()  # retry within xx seconds example: 2

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = AuthMobileCodeResponseData_Data(**data)
        return obj


class AuthMobileLoginRequest_ChildInfo(object):
    __slots__ = ['born', 'nickname', 'birth_ts', 'gender', 'relation', '_original_data']

    def __init__(self, born=None, nickname=None, birth_ts=None, gender=None, relation=None, original_data=None):
        self.born = born
        self.nickname = nickname
        self.birth_ts = birth_ts
        self.gender = gender
        self.relation = relation
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class AuthMobileLoginRequest_ChildInfoSchema(marshmallow.Schema):
    born = marshmallow.fields.Boolean()  # 孩子是否已出生 example: True
    nickname = marshmallow.fields.String()  # 孩子昵称 example: powerfulio
    birth_ts = marshmallow.fields.Integer()  # 孩子出生日期 时间戳 北京时间 example: 1523264525
    gender = marshmallow.fields.Integer()  # example: 1
    relation = marshmallow.fields.Integer()  # 用户和孩子的关系 example: 1

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = AuthMobileLoginRequest_ChildInfo(**data)
        return obj


class AuthMobileLoginResponseData(object):
    __slots__ = ['user_id', 'token', 'relation', '_original_data']

    def __init__(self, user_id=None, token=None, relation=None, original_data=None):
        self.user_id = user_id
        self.token = token
        self.relation = relation
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class AuthMobileLoginResponseDataSchema(marshmallow.Schema):
    user_id = marshmallow.fields.String(validate=validator.v_enc_id)  # example: uuid_user_1
    token = marshmallow.fields.String()  # Token From Server example: token_123ABC
    relation = marshmallow.fields.Integer()  # 用户和孩子的关系 example: 1

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = AuthMobileLoginResponseData(**data)
        return obj


class CarerApplyResponseData(object):
    __slots__ = ['verify_date', 'qr', 'wx_id', '_original_data']

    def __init__(self, verify_date=None, qr=None, wx_id=None, original_data=None):
        self.verify_date = verify_date
        self.qr = qr
        self.wx_id = wx_id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class CarerApplyResponseDataSchema(marshmallow.Schema):
    verify_date = marshmallow.fields.String()  # 预计审核完成日期 example: 2018-05-01
    qr = marshmallow.fields.URL(relative=True)  # 微信群二维码 URL example: http://qiniu.com//birth_cert.jpg
    wx_id = marshmallow.fields.String()  # 微信号 example: more_fat_gay

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = CarerApplyResponseData(**data)
        return obj


class CarerApplyResult(object):
    __slots__ = ['status', 'reason', '_original_data']

    def __init__(self, status=None, reason=None, original_data=None):
        self.status = status
        self.reason = reason
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class CarerApplyResultSchema(marshmallow.Schema):
    status = marshmallow.fields.Integer()  # 看护人申请状态 example: 1
    reason = marshmallow.fields.String()  # 审核未通过原因 example: 视频涉暴恐

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = CarerApplyResult(**data)
        return obj


class Child(object):
    __slots__ = ['id', 'nickname', 'realname', 'gender', 'age', 'id_card_no', '_original_data']

    def __init__(self, id=None, nickname=None, realname=None, gender=None, age=None, id_card_no=None, original_data=None):
        self.id = id
        self.nickname = nickname
        self.realname = realname
        self.gender = gender
        self.age = age
        self.id_card_no = id_card_no
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ChildSchema(marshmallow.Schema):
    id = marshmallow.fields.Integer(validate=validator.v_enc_id)  # example: uuid_child_1
    nickname = marshmallow.fields.String()  # 昵称 example: powerfulio
    realname = marshmallow.fields.String()  # 真实姓名 example: 刘小力
    gender = marshmallow.fields.String()  # example: 女
    age = marshmallow.fields.Integer()  # example: 1
    id_card_no = marshmallow.fields.String()  # 身份证号 example: 220324199608192318

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = Child(**data)
        return obj


class ChildUpdateResponseData(object):
    __slots__ = ['id', '_original_data']

    def __init__(self, id=None, original_data=None):
        self.id = id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ChildUpdateResponseDataSchema(marshmallow.Schema):
    id = marshmallow.fields.String(validate=validator.v_enc_id)  # example: uuid_child_1

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ChildUpdateResponseData(**data)
        return obj


class CreateGuardianRequestData(object):
    __slots__ = ['id_card_no', 'realname', 'mobile', '_original_data']

    def __init__(self, id_card_no, realname, mobile, original_data=None):
        self.id_card_no = id_card_no
        self.realname = realname
        self.mobile = mobile
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class CreateGuardianRequestDataSchema(marshmallow.Schema):
    id_card_no = marshmallow.fields.String(required=True)  # 身份证号 example: 220324199608192318
    realname = marshmallow.fields.String(required=True)  # 真实姓名 example: 姜太公
    mobile = marshmallow.fields.String(required=True, validate=validator.v_mobile)  # 手机号 example: 13618810002

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = CreateGuardianRequestData(**data)
        return obj


class Guardian(object):
    __slots__ = ['id', 'id_card_no', 'realname', 'mobile', '_original_data']

    def __init__(self, id=None, id_card_no=None, realname=None, mobile=None, original_data=None):
        self.id = id
        self.id_card_no = id_card_no
        self.realname = realname
        self.mobile = mobile
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class GuardianSchema(marshmallow.Schema):
    id = marshmallow.fields.Integer()  # 监护人 ID example: 123
    id_card_no = marshmallow.fields.String()  # 身份证号 example: 220324199608192318
    realname = marshmallow.fields.String()  # 真实姓名 example: 姜太公
    mobile = marshmallow.fields.String(validate=validator.v_mobile)  # 手机号 example: 13618810002

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = Guardian(**data)
        return obj


class GuardianCreateResponseData(object):
    __slots__ = ['id', '_original_data']

    def __init__(self, id=None, original_data=None):
        self.id = id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class GuardianCreateResponseDataSchema(marshmallow.Schema):
    id = marshmallow.fields.Integer()  # 创建的监护人 ID example: 123

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = GuardianCreateResponseData(**data)
        return obj


class OSSDownloadURLResponseData(object):
    __slots__ = ['url', '_original_data']

    def __init__(self, url=None, original_data=None):
        self.url = url
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class OSSDownloadURLResponseDataSchema(marshmallow.Schema):
    url = marshmallow.fields.URL(relative=True)  # 加密后的 URL example: image

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = OSSDownloadURLResponseData(**data)
        return obj


class ObjectInfo(object):
    __slots__ = ['key', 'mime_type', 'etag', 'size', 'persistent_id', 'width', 'height', 'duration', '_original_data']

    def __init__(self, key, mime_type=None, etag=None, size=None, persistent_id=None, width=None, height=None, duration=None, original_data=None):
        self.key = key
        self.mime_type = mime_type
        self.etag = etag
        self.size = size
        self.persistent_id = persistent_id
        self.width = width
        self.height = height
        self.duration = duration
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ObjectInfoSchema(marshmallow.Schema):
    key = marshmallow.fields.String(required=True)  # qiniu oss key example: user_id_123/avatar/2018/03/138/etag.jpg
    mime_type = marshmallow.fields.String()  # 文件类型 mimeType example: image/jpeg
    etag = marshmallow.fields.String()  # 使用 qiniu sdk 计算的 etag example: 7DsdkdFSKkdljfksQWET-TUI
    size = marshmallow.fields.Integer()  # 文件大小 example: 536123
    persistent_id = marshmallow.fields.String()  # 七牛持久化操作 ID 用于查询视频转码和截图等异步操作的结果 example: z1.5ade998d856db843bc8fe6f2
    width = marshmallow.fields.Integer()  # 分辨率 宽 example: 1080
    height = marshmallow.fields.Integer()  # 分辨率 高 example: 1920
    duration = marshmallow.fields.Decimal()  # 播放时长 example: 10.0

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ObjectInfo(**data)
        return obj


class ShareListResponseDataItem(object):
    __slots__ = ['id', 'start_ts', 'end_ts', 'accompanied', 'child_count', 'child_count_max', 'price', 'price_per_hour', 'tags', 'description', '_original_data']

    def __init__(self, id, start_ts, end_ts, accompanied, child_count, child_count_max, price, price_per_hour, tags=None, description=None, original_data=None):
        self.id = id
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.accompanied = accompanied
        self.child_count = child_count
        self.child_count_max = child_count_max
        self.price = price
        self.price_per_hour = price_per_hour
        self.tags = tags
        self.description = description
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ShareListResponseDataItemSchema(marshmallow.Schema):
    id = marshmallow.fields.Integer(required=True)  # 共享时间 ID example: 123
    start_ts = marshmallow.fields.Integer(required=True)  # 几点开始接待孩子 时间戳 example: 1524644418
    end_ts = marshmallow.fields.Integer(required=True)  # 几点结束 时间戳 example: 1524644418
    accompanied = marshmallow.fields.Boolean(required=True)  # 是否必须家长陪同 example: True
    child_count = marshmallow.fields.Integer(required=True)  # 已报名孩子数量 example: 3
    child_count_max = marshmallow.fields.Integer(required=True)  # 最多接待多少孩子 example: 14
    price = marshmallow.fields.Integer(required=True)  # 价格(摩尔豆) example: 60
    price_per_hour = marshmallow.fields.Integer(required=True)  # 每小时单位价格(摩尔豆) example: 30
    tags = marshmallow.fields.List(marshmallow.fields.String())  # 活动内容标签 example: ['看书', '写字']
    description = marshmallow.fields.String()  # 活动描述 example: 一起看欧洲冠军杯决赛

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ShareListResponseDataItem(**data)
        return obj


class SharePublishRequest(object):
    __slots__ = ['start_ts', 'end_ts', 'price', 'tags', 'description', 'accompanied', '_original_data']

    def __init__(self, tags, start_ts=None, end_ts=None, price=None, description=None, accompanied=None, original_data=None):
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.price = price
        self.tags = tags
        self.description = description
        self.accompanied = accompanied
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class SharePublishRequestSchema(marshmallow.Schema):
    start_ts = marshmallow.fields.Integer()  # 几点开始接待孩子 时间戳 example: 1524644418
    end_ts = marshmallow.fields.Integer()  # 几点结束 时间戳 example: 1524644418
    price = marshmallow.fields.Integer()  # 价格(摩尔豆) example: 60
    tags = marshmallow.fields.List(marshmallow.fields.Integer(), required=True)  # 活动内容标签 ID example: [2, 3, 4]
    description = marshmallow.fields.String()  # 补充描述 example: 请出入想补充的信息 我想和孩子一起玩玩
    accompanied = marshmallow.fields.Boolean(missing=True)  # 是否必须家长陪同 example: True

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = SharePublishRequest(**data)
        return obj


class SharePublishResponseData(object):
    __slots__ = ['id', '_original_data']

    def __init__(self, id, original_data=None):
        self.id = id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class SharePublishResponseDataSchema(marshmallow.Schema):
    id = marshmallow.fields.String(required=True, validate=validator.v_enc_id)  # 本次发布的活动 ID example: 123

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = SharePublishResponseData(**data)
        return obj


class ShareTagsResponseItem(object):
    __slots__ = ['id', 'text', '_original_data']

    def __init__(self, id, text, original_data=None):
        self.id = id
        self.text = text
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ShareTagsResponseItemSchema(marshmallow.Schema):
    id = marshmallow.fields.Integer(required=True)  # 标签 ID example: 3
    text = marshmallow.fields.String(required=True)  # 标签文字 example: 唱歌

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ShareTagsResponseItem(**data)
        return obj


class Status(object):
    __slots__ = ['code', 'msg', '_original_data']

    def __init__(self, code, msg, original_data=None):
        self.code = code
        self.msg = msg
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class StatusSchema(marshmallow.Schema):
    code = marshmallow.fields.Integer(required=True)  # 错误码，成功为 0
    msg = marshmallow.fields.String(required=True)  # 错误信息

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = Status(**data)
        return obj


class UploadTokenResponseData(object):
    __slots__ = ['token', 'expiration', '_original_data']

    def __init__(self, token=None, expiration=None, original_data=None):
        self.token = token
        self.expiration = expiration
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UploadTokenResponseDataSchema(marshmallow.Schema):
    token = marshmallow.fields.String()  # 上传token example: EWEEKOOgH774kafCEiLp7dMwQmQ7aqmnTFTlJXzf:yIeNbSmjYbeENyi3ZIj
    expiration = marshmallow.fields.String()  # token过期时间(UTC) example: 2018-03-26 04:31:24

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UploadTokenResponseData(**data)
        return obj


class UserChildDeleteRequest(object):
    __slots__ = ['id', '_original_data']

    def __init__(self, id, original_data=None):
        self.id = id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserChildDeleteRequestSchema(marshmallow.Schema):
    id = marshmallow.fields.String(required=True)  # 孩子 id example: 123

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserChildDeleteRequest(**data)
        return obj


class UserChildUpdateData(object):
    __slots__ = ['id', 'uuid', 'nickname', 'realname', 'id_card_no', '_original_data']

    def __init__(self, id=None, uuid=None, nickname=None, realname=None, id_card_no=None, original_data=None):
        self.id = id
        self.uuid = uuid
        self.nickname = nickname
        self.realname = realname
        self.id_card_no = id_card_no
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserChildUpdateDataSchema(marshmallow.Schema):
    id = marshmallow.fields.Integer()  # 孩子 id example: 112
    uuid = marshmallow.fields.String(validate=validator.v_enc_id)  # example: uuid_child_1
    nickname = marshmallow.fields.String()  # 昵称 example: powerfulio
    realname = marshmallow.fields.String()  # 真实姓名 example: 刘小力
    id_card_no = marshmallow.fields.String(validate=validator.v_id_number)  # 身份证号 example: 220***********2318

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserChildUpdateData(**data)
        return obj


class UserFollowingItem(object):
    __slots__ = ['user_id', 'avatar_url', 'nickname', '_original_data']

    def __init__(self, user_id=None, avatar_url=None, nickname=None, original_data=None):
        self.user_id = user_id
        self.avatar_url = avatar_url
        self.nickname = nickname
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserFollowingItemSchema(marshmallow.Schema):
    user_id = marshmallow.fields.Integer()  # 用户 ID example: 123
    avatar_url = marshmallow.fields.URL(relative=True)  # 个人头像图片 URL example: qiniu.com/image/2018/03/11/avatar.jpg
    nickname = marshmallow.fields.String()  # 用户昵称 example: 煎饼侠的姥爷

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserFollowingItem(**data)
        return obj


class UserIdentifyLivenessResponseData(object):
    __slots__ = ['result', '_original_data']

    def __init__(self, result=None, original_data=None):
        self.result = result
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserIdentifyLivenessResponseDataSchema(marshmallow.Schema):
    result = marshmallow.fields.Integer()  # 检测是否通过 example: 1

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserIdentifyLivenessResponseData(**data)
        return obj


class UserInfo(object):
    __slots__ = ['user_id', 'nickname', 'realname', 'mobile', 'id_card_no', 'child_relation', 'degree', 'avatar_url', 'is_carer', 'carer_apply_status', 'children_nicknames', '_original_data']

    def __init__(self, user_id=None, nickname=None, realname=None, mobile=None, id_card_no=None, child_relation=None, degree=None, avatar_url=None, is_carer=None, carer_apply_status=None, children_nicknames=None, original_data=None):
        self.user_id = user_id
        self.nickname = nickname
        self.realname = realname
        self.mobile = mobile
        self.id_card_no = id_card_no
        self.child_relation = child_relation
        self.degree = degree
        self.avatar_url = avatar_url
        self.is_carer = is_carer
        self.carer_apply_status = carer_apply_status
        self.children_nicknames = children_nicknames
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserInfoSchema(marshmallow.Schema):
    user_id = marshmallow.fields.Integer()  # 用户 id example: 12356789
    nickname = marshmallow.fields.String()  # 昵称 example: 刘小力的妈妈
    realname = marshmallow.fields.String()  # 真实姓名 example: 刘大力
    mobile = marshmallow.fields.String(validate=validator.v_mobile)  # 手机号 example: 13618810002
    id_card_no = marshmallow.fields.String(validate=validator.v_id_number)  # 身份证号 example: 220***********2318
    child_relation = marshmallow.fields.String()  # 和孩子的关系 example: 妈妈
    degree = marshmallow.fields.String()  # 最高学历 example: 博士
    avatar_url = marshmallow.fields.URL(relative=True)  # 个人头像图片 URL example: qiniu.com/image/2018/03/11/avatar.jpg
    is_carer = marshmallow.fields.Boolean()  # 是否已经是看护人(审核通过至少一次) example: True
    carer_apply_status = marshmallow.fields.Integer()  # 当前看护人申请状态
    children_nicknames = marshmallow.fields.List(marshmallow.fields.String())  # 孩子们的昵称

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserInfo(**data)
        return obj


class UserInfoPresetRequest(object):
    __slots__ = ['born', 'nickname', 'relation', 'birth_ts', 'gender', '_original_data']

    def __init__(self, born, nickname, relation, birth_ts=None, gender=None, original_data=None):
        self.born = born
        self.nickname = nickname
        self.relation = relation
        self.birth_ts = birth_ts
        self.gender = gender
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserInfoPresetRequestSchema(marshmallow.Schema):
    born = marshmallow.fields.Boolean(required=True)  # 孩子是否已出生
    nickname = marshmallow.fields.String(required=True)  # 孩子昵称 example: 小宝贝
    relation = marshmallow.fields.Integer(required=True)  # 孩子关系 example: 1
    birth_ts = marshmallow.fields.Integer()  # 孩子出生日期 时间戳 example: 1523264525
    gender = marshmallow.fields.Integer()  # example: 1

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserInfoPresetRequest(**data)
        return obj


class UserInfoUpdateResponseData(object):
    __slots__ = ['id', '_original_data']

    def __init__(self, id, original_data=None):
        self.id = id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserInfoUpdateResponseDataSchema(marshmallow.Schema):
    id = marshmallow.fields.String(required=True, validate=validator.v_enc_id)  # example: uuid_user_1

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserInfoUpdateResponseData(**data)
        return obj


class UserProfile(object):
    __slots__ = ['point_balance', 'point_notification_count', 'order_notification_count', '_original_data']

    def __init__(self, point_balance=None, point_notification_count=None, order_notification_count=None, original_data=None):
        self.point_balance = point_balance
        self.point_notification_count = point_notification_count
        self.order_notification_count = order_notification_count
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserProfileSchema(marshmallow.Schema):
    point_balance = marshmallow.fields.Integer()  # 摩尔豆余额 example: 2260
    point_notification_count = marshmallow.fields.Integer()  # 摩尔豆相关未读消息数量 example: 2
    order_notification_count = marshmallow.fields.Integer()  # 订单相关未读消息数量 example: 2

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserProfile(**data)
        return obj


class UserUploadDoneRequest(object):
    __slots__ = ['cloud', 'category', 'key', 'etag', 'persistentId', 'mimeType', 'size', 'reftag', '_original_data']

    def __init__(self, cloud, category, key, etag, persistentId=None, mimeType=None, size=None, reftag=None, original_data=None):
        self.cloud = cloud
        self.category = category
        self.key = key
        self.etag = etag
        self.persistentId = persistentId
        self.mimeType = mimeType
        self.size = size
        self.reftag = reftag
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserUploadDoneRequestSchema(marshmallow.Schema):
    cloud = marshmallow.fields.String(required=True)  # 云服务(qiniu) example: qiniu
    category = marshmallow.fields.String(required=True)  # 应用层 category example: video
    key = marshmallow.fields.String(required=True)  # oss key example: user_id_123/avatar/2018/03/138/etag.jpg
    etag = marshmallow.fields.String(required=True)  # 使用 qiniu sdk 计算的 etag example: 7DsdkdFSKkdljfksQWET-TUI
    persistentId = marshmallow.fields.String()  # 七牛上传文件成功后返回的 persistentId example: z1.5ad99a2b856db843bcfff1de
    mimeType = marshmallow.fields.String()  # 文件类型 mimeType example: image/jpeg
    size = marshmallow.fields.Integer()  # 文件大小 example: 536123
    reftag = marshmallow.fields.String()  # 引用tag 表示该文件的使用方式 如: avatar、intro-video example: intro-video

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserUploadDoneRequest(**data)
        return obj


class UserUploadDoneResponseData(object):
    __slots__ = ['id', '_original_data']

    def __init__(self, id, original_data=None):
        self.id = id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserUploadDoneResponseDataSchema(marshmallow.Schema):
    id = marshmallow.fields.String(required=True, validate=validator.v_enc_id)  # 文件 ID example: 123

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserUploadDoneResponseData(**data)
        return obj


class UserVideo(object):
    __slots__ = ['key', 'mime_type', 'etag', 'size', 'width', 'height', 'duration', 'cover_url', 'video_url', '_original_data']

    def __init__(self, key=None, mime_type=None, etag=None, size=None, width=None, height=None, duration=None, cover_url=None, video_url=None, original_data=None):
        self.key = key
        self.mime_type = mime_type
        self.etag = etag
        self.size = size
        self.width = width
        self.height = height
        self.duration = duration
        self.cover_url = cover_url
        self.video_url = video_url
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserVideoSchema(marshmallow.Schema):
    key = marshmallow.fields.String()  # qiniu oss key example: user_id_123/avatar/2018/03/138/etag.jpg
    mime_type = marshmallow.fields.String()  # 文件类型 mimeType example: image/jpeg
    etag = marshmallow.fields.String()  # 使用 qiniu sdk 计算的 etag example: 7DsdkdFSKkdljfksQWET-TUI
    size = marshmallow.fields.Integer()  # 视频文件大小(字节) example: 10240002
    width = marshmallow.fields.Integer()  # 视频分辨率 宽 example: 800
    height = marshmallow.fields.Integer()  # 视频分辨率 高 example: 600
    duration = marshmallow.fields.Decimal()  # 视频播放时长 example: 10.0
    cover_url = marshmallow.fields.URL(relative=True)  # 视频快照截图 URL example: http://p5zmpa3g9.bkt.clouddn.com/cover.jpg
    video_url = marshmallow.fields.URL(relative=True)  # 视频URL example: http://p5zmpa3g9.bkt.clouddn.com/video.mp4

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserVideo(**data)
        return obj


class AuthMobileCodeResponseData(object):
    __slots__ = ['status', 'data', '_original_data']

    def __init__(self, status, data=None, original_data=None):
        self.status = status
        self.data = data
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class AuthMobileCodeResponseDataSchema(marshmallow.Schema):
    status = marshmallow.fields.Nested(StatusSchema(), required=True)
    data = marshmallow.fields.Nested(AuthMobileCodeResponseData_DataSchema())

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = AuthMobileCodeResponseData(**data)
        return obj


class AuthMobileLoginRequest(object):
    __slots__ = ['mobile', 'password', 'child_info', '_original_data']

    def __init__(self, mobile, password, child_info=None, original_data=None):
        self.mobile = mobile
        self.password = password
        self.child_info = child_info
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class AuthMobileLoginRequestSchema(marshmallow.Schema):
    mobile = marshmallow.fields.String(required=True, validate=validator.v_mobile)  # 明文手机号
    password = marshmallow.fields.String(required=True, validate=marshmallow.validate.Length(min=4, max=4))  # 登录时发送的验证码
    child_info = marshmallow.fields.Nested(AuthMobileLoginRequest_ChildInfoSchema())

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = AuthMobileLoginRequest(**data)
        return obj


class CarerApplicationData_Video(object):
    __slots__ = ['intro', 'playground', 'extra', '_original_data']

    def __init__(self, intro=None, playground=None, extra=None, original_data=None):
        self.intro = intro
        self.playground = playground
        self.extra = extra
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class CarerApplicationData_VideoSchema(marshmallow.Schema):
    intro = marshmallow.fields.Nested(UserVideoSchema())
    playground = marshmallow.fields.Nested(UserVideoSchema())
    extra = marshmallow.fields.List(marshmallow.fields.Nested(UserVideoSchema()))

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = CarerApplicationData_Video(**data)
        return obj


class CarerApplyRequestData_Video(object):
    __slots__ = ['intro', 'playground', 'extra', '_original_data']

    def __init__(self, intro=None, playground=None, extra=None, original_data=None):
        self.intro = intro
        self.playground = playground
        self.extra = extra
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class CarerApplyRequestData_VideoSchema(marshmallow.Schema):
    intro = marshmallow.fields.Nested(ObjectInfoSchema())
    playground = marshmallow.fields.Nested(ObjectInfoSchema())
    extra = marshmallow.fields.List(marshmallow.fields.Nested(ObjectInfoSchema()))

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = CarerApplyRequestData_Video(**data)
        return obj


class CarerInfoGetResponseData(object):
    __slots__ = ['user_id', 'nickname', 'identified', 'degree', 'care_exp', 'child_age_min', 'child_age_max', 'avatar_url', 'address', 'distance', 'liked', 'like_count', 'followed', 'follow_count', 'videos', '_original_data']

    def __init__(self, user_id=None, nickname=None, identified=None, degree=None, care_exp=None, child_age_min=None, child_age_max=None, avatar_url=None, address=None, distance=None, liked=None, like_count=None, followed=None, follow_count=None, videos=None, original_data=None):
        self.user_id = user_id
        self.nickname = nickname
        self.identified = identified
        self.degree = degree
        self.care_exp = care_exp
        self.child_age_min = child_age_min
        self.child_age_max = child_age_max
        self.avatar_url = avatar_url
        self.address = address
        self.distance = distance
        self.liked = liked
        self.like_count = like_count
        self.followed = followed
        self.follow_count = follow_count
        self.videos = videos
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class CarerInfoGetResponseDataSchema(marshmallow.Schema):
    user_id = marshmallow.fields.Integer()  # 用户 id example: 123
    nickname = marshmallow.fields.String()  # 昵称 example: 小番茄的妈妈
    identified = marshmallow.fields.Boolean()  # 是否实名认证 example: True
    degree = marshmallow.fields.String()  # 学历 example: 硕士
    care_exp = marshmallow.fields.Integer()  # 带娃经验(年) example: 5
    child_age_min = marshmallow.fields.Integer()  # 接待孩子最小年龄
    child_age_max = marshmallow.fields.Integer()  # 接待孩子最大年龄 example: 6
    avatar_url = marshmallow.fields.URL(relative=True)  # 头像图片 URL example: qiniu.com/image/2018/03/11/avatar.jpg
    address = marshmallow.fields.Nested(AddressSchema())
    distance = marshmallow.fields.String()  # 与用户的距离 example: 3.1km(>=1000米) 128m(<1000m)
    liked = marshmallow.fields.Boolean()  # 是否赞过
    like_count = marshmallow.fields.Integer()  # 点赞次数 example: 100
    followed = marshmallow.fields.Boolean()  # 是否已关注
    follow_count = marshmallow.fields.Integer()  # 关注人数 example: 28
    videos = marshmallow.fields.List(marshmallow.fields.Nested(UserVideoSchema()))  # 看护人的视频

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = CarerInfoGetResponseData(**data)
        return obj


class RecommendCarerResponseDataItem(object):
    __slots__ = ['user_id', 'nickname', 'avatar_url', 'address', 'address_name', 'distance', 'liked', 'like_count', 'followed', 'follow_count', 'videos', '_original_data']

    def __init__(self, user_id=None, nickname=None, avatar_url=None, address=None, address_name=None, distance=None, liked=None, like_count=None, followed=None, follow_count=None, videos=None, original_data=None):
        self.user_id = user_id
        self.nickname = nickname
        self.avatar_url = avatar_url
        self.address = address
        self.address_name = address_name
        self.distance = distance
        self.liked = liked
        self.like_count = like_count
        self.followed = followed
        self.follow_count = follow_count
        self.videos = videos
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class RecommendCarerResponseDataItemSchema(marshmallow.Schema):
    user_id = marshmallow.fields.String(validate=validator.v_enc_id)  # 用户 id example: 123456
    nickname = marshmallow.fields.String()  # 昵称 example: xxx的妈妈
    avatar_url = marshmallow.fields.URL(relative=True)  # 头像图片 URL example: qiniu.com/image/2018/03/11/avatar.jpg
    address = marshmallow.fields.String()  # 简短地址
    address_name = marshmallow.fields.String()  # user_address 里的 name 字段
    distance = marshmallow.fields.String()  # 距离 example: 1.2km(821m)
    liked = marshmallow.fields.Boolean()  # 是否赞过 example: True
    like_count = marshmallow.fields.Integer()  # 被点赞次数 example: 100
    followed = marshmallow.fields.Boolean()  # 是否收藏过
    follow_count = marshmallow.fields.Integer()  # 被收藏次数 example: 28
    videos = marshmallow.fields.List(marshmallow.fields.Nested(UserVideoSchema()))  # 看护人的视频

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = RecommendCarerResponseDataItem(**data)
        return obj


class UserIdentifyLivenessRequest(object):
    __slots__ = ['realname', 'id_card_no', 'liveness_id', 'idcard_image', 'live_image', 'info', '_original_data']

    def __init__(self, realname, id_card_no, liveness_id, idcard_image=None, live_image=None, info=None, original_data=None):
        self.realname = realname
        self.id_card_no = id_card_no
        self.liveness_id = liveness_id
        self.idcard_image = idcard_image
        self.live_image = live_image
        self.info = info
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserIdentifyLivenessRequestSchema(marshmallow.Schema):
    realname = marshmallow.fields.String(required=True)  # 真实姓名 example: 刘大力
    id_card_no = marshmallow.fields.String(required=True)  # 身份证号 example: 220326199308125277
    liveness_id = marshmallow.fields.String(required=True)  # 活体检测 ID example: 86be940bea6c4b35a2e0e9829b20d51d
    idcard_image = marshmallow.fields.Nested(ObjectInfoSchema())
    live_image = marshmallow.fields.Nested(ObjectInfoSchema())
    info = marshmallow.fields.String()  # 其他有用信息 格式化成 json 串

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserIdentifyLivenessRequest(**data)
        return obj


class UserInfoUpdateRequest(object):
    __slots__ = ['realname', 'mobile', 'id_card_no', 'child_relation', 'degree', 'avatar', '_original_data']

    def __init__(self, realname=None, mobile=None, id_card_no=None, child_relation=None, degree=None, avatar=None, original_data=None):
        self.realname = realname
        self.mobile = mobile
        self.id_card_no = id_card_no
        self.child_relation = child_relation
        self.degree = degree
        self.avatar = avatar
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserInfoUpdateRequestSchema(marshmallow.Schema):
    realname = marshmallow.fields.String()  # 真实姓名 example: 刘大力
    mobile = marshmallow.fields.String(validate=validator.v_mobile)  # 手机号 example: 13618810002
    id_card_no = marshmallow.fields.String(validate=validator.v_id_number)  # 身份证号 example: 220324199608192318
    child_relation = marshmallow.fields.Integer()  # 和孩子的关系 example: 1
    degree = marshmallow.fields.Integer()  # 最高学历 example: 1
    avatar = marshmallow.fields.Nested(ObjectInfoSchema())

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = UserInfoUpdateRequest(**data)
        return obj


class CarerApplicationData(object):
    __slots__ = ['video', 'degree', 'address', 'child_count', 'child_age_min', 'child_age_max', 'identify_result', 'status', 'result', 'birth_certificate', 'birth_certificate_url', '_original_data']

    def __init__(self, video=None, degree=None, address=None, child_count=None, child_age_min=None, child_age_max=None, identify_result=None, status=None, result=None, birth_certificate=None, birth_certificate_url=None, original_data=None):
        self.video = video
        self.degree = degree
        self.address = address
        self.child_count = child_count
        self.child_age_min = child_age_min
        self.child_age_max = child_age_max
        self.identify_result = identify_result
        self.status = status
        self.result = result
        self.birth_certificate = birth_certificate
        self.birth_certificate_url = birth_certificate_url
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class CarerApplicationDataSchema(marshmallow.Schema):
    video = marshmallow.fields.Nested(CarerApplicationData_VideoSchema())  # 个人、场地及其他介绍视频
    degree = marshmallow.fields.String()  # 学历 example: 硕士
    address = marshmallow.fields.Nested(AddressSchema())
    child_count = marshmallow.fields.Integer()  # 接待孩子数 example: 10
    child_age_min = marshmallow.fields.Integer()  # 接待孩子最小年龄
    child_age_max = marshmallow.fields.Integer()  # 接待孩子最大年龄 example: 6
    identify_result = marshmallow.fields.Boolean()  # 是否实名认证 example: True
    status = marshmallow.fields.Integer()  # 看护人申请状态 example: 1
    result = marshmallow.fields.String()  # 审核未通过原因 example: 视频涉暴恐
    birth_certificate = marshmallow.fields.Nested(ObjectInfoSchema())
    birth_certificate_url = marshmallow.fields.URL(relative=True)  # 出生证明图片 URL example: qiniu.com/image/2018/03/11/birth.jpg

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = CarerApplicationData(**data)
        return obj


class CarerApplyRequestData(object):
    __slots__ = ['video', 'degree', 'address', 'child_count', 'child_age_min', 'child_age_max', 'identify_result', 'birth_certificate', '_original_data']

    def __init__(self, video, degree, address, birth_certificate, child_count=None, child_age_min=None, child_age_max=None, identify_result=None, original_data=None):
        self.video = video
        self.degree = degree
        self.address = address
        self.child_count = child_count
        self.child_age_min = child_age_min
        self.child_age_max = child_age_max
        self.identify_result = identify_result
        self.birth_certificate = birth_certificate
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class CarerApplyRequestDataSchema(marshmallow.Schema):
    video = marshmallow.fields.Nested(CarerApplyRequestData_VideoSchema(), required=True)
    degree = marshmallow.fields.Integer(required=True)  # 最高学历 example: 1
    address = marshmallow.fields.Nested(AddressSchema(), required=True)
    child_count = marshmallow.fields.Integer()  # 接待孩子数 example: 10
    child_age_min = marshmallow.fields.Integer()  # 接待孩子最小年龄 example: 1
    child_age_max = marshmallow.fields.Integer()  # 接待孩子最大年龄 example: 6
    identify_result = marshmallow.fields.Boolean()  # 实名认证结果 example: True
    birth_certificate = marshmallow.fields.Nested(ObjectInfoSchema(), required=True)

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = CarerApplyRequestData(**data)
        return obj
