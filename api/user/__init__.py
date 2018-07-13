#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api.blueprint import create_blueprint

blueprint = create_blueprint('user_blueprint', __name__, url_prefix='/v1/user')

from . import carer  # noqa
from . import child  # noqa
from . import guardian  # noqa
from . import identify  # noqa
from . import info  # noqa
from . import profile  # noqa
from . import social  # noqa
