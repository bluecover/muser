#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session


class Facade(object):
    Engine = None
    SessionMaker = None

    DefaultHost = "localhost"
    DefaultUser = "root"
    DefaultPassword = "000"
    DefaultPort = 3306
    DefaultDB = "moremom"

    @staticmethod
    def initialize(config: dict):
        mysql_dsn = "mysql://{user}:{password}@{host}:{port}/{db}?{params}".format(
            host=config.get("host", Facade.DefaultHost),
            port=config.get("port", Facade.DefaultPort),
            user=config.get("user", Facade.DefaultUser),
            password=config.get("password", Facade.DefaultPassword),
            db=config.get("db", Facade.DefaultDB),
            params=config.get("params", "")
        )
        Facade.Engine = create_engine(mysql_dsn, pool_recycle=3600)
        Facade.SessionMaker = sessionmaker(bind=Facade.Engine)

    @staticmethod
    def make_session() -> Session:
        return Facade.SessionMaker()

    @staticmethod
    def make_scoped_session() -> Session:
        return scoped_session(Facade.SessionMaker)

    @staticmethod
    def release_session(session: Session):
        session.remove()
