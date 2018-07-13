#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session

from orm.orm_mysql import WalletModel


def find_user_wallet(db: Session, user_id: int) ->WalletModel:
    w = db.query(WalletModel).filter(
        WalletModel.customer_id == user_id
    ).first()
    return w
