#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum

LOGIN_CODE_LENGTH = 4

CARER_APPLY_QR_CODE_IMAGE_URL = "http://p6byep6mn.bkt.clouddn.com/qr/moremom_gugu.jpeg"
CARER_APPLY_WX_ID = "moremom_gugu"
MOBILE_CODE_CHINA = "+86"


class Gender(Enum):
    Unknow = 0
    Female = 1
    Male = 2


# 孩子性别
CHILD_GENDER_INT2CN = {
    0: "待定",
    1: "女",
    2: "男",
}


class MessageTemplate(Enum):
    LoginCode = "SMS_129440028"


# 学历
DEGREE_INT2CN = {
    0: "无",
    1: "专科",
    2: "本科",
    3: "硕士",
    4: "博士",
}

# 家人和孩子的关系
CHILD_RELATION_INT2CN = {
    0: "未知",
    1: "妈妈",
    2: "爸爸",
    3: "爷爷",
    4: "奶奶",
    5: "外公",
    6: "外婆",
    7: "其他家人",
}

# 看护人申请 不通过原因
CARER_APPLY_REJECT_REASON = {
    -1: "未提交申请",
    0: "审核通过",
    1: "视频涉黄",
    2: "视频涉政",
    3: "视频涉暴恐",
    4: "经验认证未通过",
    5: "介绍视频没有看护人",
    6: "介绍内容不符合要求",
    7: "场地不符合要求"
}


class IdentityVerificationStatus(Enum):
    Unknown = 0
    Passed = 1
    Failed = 2


class CarerApplicationStatus(Enum):
    NotSubmitted = -1
    Reviewing = 0
    Approved = 1
    Rejected = 2
    Disabled = 3


class UserStatus(Enum):
    Normal = 0
