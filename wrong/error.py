#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Define API Errors

    An API error object is an instance of `namedtuple`.
"""

from collections import namedtuple

APIError = namedtuple("APIError", ["code", "msg", "wording"])

UnknownError = APIError(1, "Unknown Error", "服务器开小差了")
InvalidParameter = APIError(1001, "Invalid Parameter", "服务器开小差了")
InvalidSignature = APIError(1002, "Invalid Signature", "服务器开小差了")
Unauthorized = APIError(2001, "Unauthorized", "请先登陆")
DeviceEnrollmentFailed = APIError(2002, "Device Enroolment Failed", "设备注册失败")
SingupFailed = APIError(2003, "SingupFailed", "注册失败")
LoginFailed = APIError(2004, "LoginFailed", "登录失败，请重试")
LoginCodeSMSOverLimit = APIError(2005, "Login Code SMS Over Limit", "您获取验证码太频繁了，请稍后重试")
InvalidLoginCode = APIError(2006, "Invalid Login Code", "验证码错误，请重新输入")
LoginCodeSMSTooOften = APIError(2007, "Login Code SMS Too Often", "您获取验证码太频繁了，请稍后重试")
UserIsBanned = APIError(2008, "User Is Banned", "您被禁止登陆")
NonExistentChild = APIError(2102, "Non-existent Child", "孩子不存在")
NonExistentCarer = APIError(2103, "Non-existent Carer", "家庭老师不存在")
NonExistentGuardian = APIError(2104, "Non-existent Guardian", "监护人不存在")
CreateChildFailed = APIError(2105, "Create Child Failed", "孩子添加失败")
CreateGuardianFailed = APIError(2106, "Create Guardian Failed", "监护人添加失败")
InvalidIDCardNumber = APIError(2201, "Invalid ID Card Number", "请填写正确的身份证信息")
IDCardNumberVerificationFailed = APIError(2202, "ID Card Number Verification Failed", "请填写正确的身份证信息")
LivenessVerificationFailed = APIError(2203, "Liveness Verification Failed", "活体认证失败")
IDCardNumberAlreadyExisted = APIError(2204, "ID Card Number Already Existed", "身份证号码已存在")
IDCardNumberOrRealnameAlreadyExisted = APIError(2205, "ID Card Number Or Realname Already Existed", "身份证号码或真实姓名已经存在")
CarerApplicationSubmitFailed = APIError(2301, "Carer Application Submit Failed", "提交失败")
CarerApplicationIdentityNotVerified = APIError(2302, "Carer Application Realname Not Identified", "实名认证未通过")
CarerApplicationAlreadyApplied = APIError(2303, "Carer Application Already Applied", "家庭老师申请已提交")
NonExistentCarerApplication = APIError(2304, "Non-existent Carer Application", "家庭老师申请不存在")
