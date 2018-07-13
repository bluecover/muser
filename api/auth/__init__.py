#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api.blueprint import create_blueprint

blueprint = create_blueprint('auth_blueprint', __name__, url_prefix='/v1/auth')

from . import login  # noqa
