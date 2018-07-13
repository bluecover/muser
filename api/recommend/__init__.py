#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api.blueprint import create_blueprint

blueprint = create_blueprint('recommend_blueprint', __name__, url_prefix='/v1/recommend')

from . import handler  # noqa
