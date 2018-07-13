#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ

import logging
import redis
import toml
import traceback
from flask import Flask, jsonify, g, request  # noqa
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.utils import import_string

from api.json_encoder import MyJSONEncoder
from api.response import ErrorResponse
from api.signature import verify_signature  # noqa
from base.auth import parse_token  # noqa
from entity import Facade as EntityFacade
from orm import Facade as ModelFacade
from orm import user as user_model  # noqa
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
from wrong import error


ENV_CONFIG = "MORER_CONFIG"


def initialize_facade():

    config_filepath = environ.get(ENV_CONFIG)
    logging.critical("config_filepath: {}".format(config_filepath))

    if not config_filepath:
        config_filepath = "config/default.toml"

    EntityFacade.config = toml.load(config_filepath)
    mysql_config = EntityFacade.config["mysql"]
    redis_config = EntityFacade.config["redis"]

    # MySQL connection
    ModelFacade.initialize(mysql_config)

    # Redis client
    EntityFacade.redis_cli = redis.Redis(
        host=redis_config["host"],
        port=redis_config["port"],
        password=redis_config["password"],
        db=redis_config["db"],
        decode_responses=True
    )

    # SMS facility
    from entity.sms import LoginCodeCodeStash, SMSTaskProxy
    from task import send_mobile_message
    EntityFacade.code_stash = LoginCodeCodeStash(redis_config)
    EntityFacade.sms_provider = SMSTaskProxy(send_mobile_message)

    # OSS reference service
    from entity.oss import OSSCeleryTaskProxy
    from task import add_oss_object_reference
    EntityFacade.oss_provider = OSSCeleryTaskProxy(add_oss_object_reference)


def handle_error(exc):
    code = 500
    if isinstance(exc, HTTPException):
        code = exc.code

    traceback.print_exc()

    data = dict(
        error=str(exc),
        code=code
    )
    return jsonify(ErrorResponse(error.UnknownError, data=data))


blueprints = [
    "api.auth:blueprint",
    "api.recommend:blueprint",
    "api.user:blueprint",
]


def create_app():
    app = Flask(__name__, static_folder=None)
    app.json_encoder = MyJSONEncoder

    # blueprints
    for blueprint_qualname in blueprints:
        blueprint = import_string(blueprint_qualname)
        app.register_blueprint(blueprint)

    # Initilize facades
    initialize_facade()

    # Initialize Sentry
    from raven.contrib.flask import Sentry
    Sentry(app, dsn="http://e87461d1ff1c4d0d9aed94346986bb71:b0b838c8fff7452dbc25f26c0a18ee1c@e.moremom.cn/2")

    # Set exception handler
    for code in default_exceptions:
        app.register_error_handler(code, handle_error)

    return app


app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.before_request
def make_db_session():
    g.db = ModelFacade.make_scoped_session()


@app.before_request
def get_user_id_from_header():
    x_user_id = request.headers.get("x-user-id", None)
    request.current_user_id = x_user_id
    app.logger.warning(request.current_user_id)
    app.logger.warning(request.args)
    app.logger.warning(request.json)


@app.after_request
def release_db_session(response):
    """ Enable Flask to automatically remove database sessions at the
        end of the request or when the application shuts down.
        Ref: http://flask.pocoo.org/docs/patterns/sqlalchemy/
    """
    if hasattr(g, "db"):
        ModelFacade.release_session(g.db)
    return response


# 需要跨域访问的 API, 用于 H5页面分享
CORS_URLS = ["/v1/carer/info", "/v1/recommend/carer/hot"]


@app.after_request
def add_cors_headers(response):
    if request.path in CORS_URLS:
        response.headers['Access-Control-Allow-Origin'] = '*'
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers

    return response
