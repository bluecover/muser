#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ
from datetime import datetime

import celery
import toml
import uuid
from celery.utils.log import get_task_logger
from redis import Redis

from orm import Facade as orm_facade
from usecase import recommend as recommend_usecase
from task import oss, sms


logger = get_task_logger(__name__)

# Configs
config_filepath = environ.get("MORER_CONFIG")
if not config_filepath:
    config_filepath = "config/default.toml"
config = toml.load(config_filepath)
mysql_config = config["mysql"]
redis_config = config["redis"]


app = celery.Celery('task')
app.conf.update(**config["celery"])

app.conf.beat_schedule = {
    'update_recommend_per_hour': {  # 每小时更新一次推荐看护人列表
        'task': 'task.update_recommend_carers',
        'schedule': 300
    }
}


class MyTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print('task done: {0}'.format(retval))
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('task fail, reason: {0}'.format(exc))
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def run(self, *args, **kwargs):
        return super(MyTask, self).run(self, *args, **kwargs)


@app.task(base=MyTask)
def send_mobile_message(phone_number, template_code=None, params=None):
    __business_id = uuid.uuid1()
    return sms.send(__business_id, phone_number, "摩尔妈妈", template_code, params)


@app.task(base=MyTask)
def add_oss_object_reference(user_id, ref_tag, object_info):
    return oss.add_object_reference(user_id, ref_tag, object_info)


from .qiniu_video_fops import query_qiniu_video_fops_result  # noqa


class RecommendUpdateTask(celery.Task):
    _db = None
    _redis = None

    @property
    def db(self):
        if self._db is None:
            orm_facade.initialize(mysql_config)
            self._db = orm_facade.make_session()
        return self._db

    @property
    def redis(self):
        if self._redis is None:
            self._redis = Redis(
                host=redis_config["host"], port=redis_config["port"],
                password=redis_config["password"],
                decode_responses=True
            )
        return self._redis

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self._db:
            self._db.close()


@app.task(bind=True, base=RecommendUpdateTask)
def update_recommend_carers(self):
    logger.warning('config_filepath: {}'.format(config_filepath))
    logger.warning('update_hot_carer_info_list at: {}'.format(datetime.now()))
    recommend_usecase.update_hot_carer_info_list(self.db, self.redis)
