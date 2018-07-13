#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wrong import error


class LoginException(Exception):
    pass


class LoginCodeSMSTooOften(LoginException):
    def __init__(self, mobile_number: str):
        self.error = error.LoginCodeSMSTooOften
        self.mobile_number = mobile_number


class LoginCodeSMSOverLimit(LoginException):
    def __init__(self, mobile_number: str):
        self.error = error.LoginCodeSMSOverLimit
        self.mobile_number = mobile_number


class ORMException(Exception):
    pass


class ORMCreateChildFailed(ORMException):
    def __init__(self, user_id: int, child_id: int):
        self.error = error.InvalidIDCardNumber
        self.user_id = user_id
        self.child_id = child_id


class UserException(Exception):
    pass


class InvalidIDCardNumber(UserException):
    def __init__(self, user_id: int, id_card_no: str, name: str):
        self.error = error.InvalidIDCardNumber
        self.user_id = user_id
        self.id_card_no = id_card_no
        self.name = name


class NonExistentUser(UserException):
    def __init__(self, user_id: int):
        self.error = error.NonExistentUser
        self.user_id = user_id


class NonExistentChild(UserException):
    def __init__(self, user_id: int, child_id: int):
        self.error = error.NonExistentChild
        self.user_id = user_id
        self.child_id = child_id


class NonExistentCarer(UserException):
    def __init__(self, user_id: int):
        self.error = error.NonExistentCarer
        self.user_id = user_id


class NonExistentGuardian(UserException):
    def __init__(self, user_id: int, guardian_id: int):
        self.error = error.NonExistentGuardian
        self.user_id = user_id
        self.guardian_id = guardian_id


class IDCardNumberVerificationFailed(UserException):
    def __init__(self, user_id: int, id_card_no: str, name: str):
        self.error = error.IDCardNumberVerificationFailed
        self.user_id = user_id
        self.id_card_no = id_card_no
        self.name = name


class IDCardNumberAlreadyExisted(UserException):
    def __init__(self, user_id: int, id_card_no: str):
        self.error = error.IDCardNumberAlreadyExisted
        self.user_id = user_id
        self.id_card_no = id_card_no


class IDCardNumberOrRealnameAlreadyExisted(UserException):
    def __init__(self, user_id: int, id_card_no: str, realname: str):
        self.error = error.IDCardNumberOrRealnameAlreadyExisted
        self.user_id = user_id
        self.id_card_no = id_card_no
        self.realname = realname


class CarerApplicationException(UserException):
    pass


class CarerApplicationIdentityNotVerified(CarerApplicationException):
    def __init__(self, user_id: int):
        self.error = error.CarerApplicationIdentityNotVerified
        self.user_id = user_id


class CarerApplicationAlreadyApplied(CarerApplicationException):
    def __init__(self, user_id: int):
        self.error = error.CarerApplicationAlreadyApplied
        self.user_id = user_id


class NonExistentCarerApplication(CarerApplicationException):
    def __init__(self, user_id: int, application_id: int):
        self.error = error.NonExistentCarerApplication
        self.user_id = user_id
        self.application_id = application_id
