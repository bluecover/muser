#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from orm.exc import is_duplicate_entry_exception
from orm.orm_mysql import UserAddressModel, CityModel
from util import current_timestamp


def create_user_address(
        db: Session, user_id: int, lat: Decimal, lng: Decimal,
        province: str = None,
        city: str = None, city_id: int = None,
        district: str = None,
        address: str = None, name: str = None, room: str = None,
        poi: str = None) -> int:
    """ Create `user_address` record if not existed.
        Igonre `Duplicate Entry` error.
    """
    try:
        m_address = UserAddressModel(
            user_id=user_id,
            lat=lat, lng=lng,
            province=province,
            city=city, city_id=city_id,
            district=district,
            address=address, name=name, room=room,
            status=0,
            poi=poi,
            create_ts=current_timestamp()
        )
        db.add(m_address)
        db.commit()
        return m_address

    except IntegrityError as exc:
        db.rollback()
        if is_duplicate_entry_exception(exc):
            return m_address
        else:
            raise


def find_user_address_by_id(db: Session, id_: int):
    m = db.query(UserAddressModel).filter(UserAddressModel.id == id_).first()
    return m


def find_city_by_name(db: Session, name: str) -> CityModel:
    if len(name) < 2:
        return None
    names = [name, name + "市", name + "县"]
    if name[-1] in ["市", "县"]:
        names.append(name[0:-1])
    m = db.query(CityModel).filter(CityModel.name.in_(names)).first()
    return m
