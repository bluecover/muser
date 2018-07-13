#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import celery
import requests
import toml
from celery.utils.log import get_task_logger

from orm import Facade as ModelFacade
from orm.orm_mysql import UserInfoModel, VideoModel, UserCarerInfoModel

from . import app


logger = get_task_logger(__name__)


class DatabaseTask(celery.Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            mysql_config = toml.load('config/local.toml')['mysql']
            ModelFacade.initialize(mysql_config)
            self._db = ModelFacade.make_session()
        return self._db

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self._db:
            self._db.close()


@app.task(bind=True, base=DatabaseTask, default_retry_delay=2, max_retries=3)
def find_user_by_id(self, user_id):
    m = self.db.query(UserInfoModel).filter(UserInfoModel.user_id == user_id).one()
    logger.info(m)
    try:
        raise Exception('find_user_by_id error: id={}'.format(138))
    except Exception as err:
        raise self.retry()


class QueryFopsResultTask(DatabaseTask):
    def on_success(self, retval, task_id, args, kwargs):
        print('task done: {0}'.format(retval))
        return super(QueryFopsResultTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('task fail, reason: {0}'.format(exc))
        return super(QueryFopsResultTask, self).on_failure(exc, task_id, args, kwargs, einfo)


def handle_video_transcode_result(db, m_user_video, i_code, s_key, s_hash):
    m_user_video.pfop_transcode_status = i_code
    cr = db.commit()
    logger.info(('[{}]pfop_transcode_status -> {}, commit result: {}'.format(m_user_video.persistent_id, i_code, cr)))
    if i_code == 0:
        m_carer_info = db.query(UserCarerInfoModel).filter(UserCarerInfoModel.user_id == m_user_video.user_id).first()
        if not m_carer_info:
            logger.error('UserCarerInfo [id:{}] not found by UserVideo [id:{}]'.format(m_user_video.user_id, m_user_video.id))
            return
        if m_user_video.reftag == 'intro':
            m_carer_info.intro_video_id = m_user_video.id
            cr = db.commit()
            logger.info(('[{}]intro_video_id -> {}, commit result: {}'.format(m_carer_info.user_id, m_user_video.id, cr)))
        elif m_user_video.reftag == 'playground':
            m_carer_info.playground_video_id = m_user_video.id
            cr = db.commit()
            logger.info(('[{}]playground_video_id -> {}, commit result: {}'.format(m_carer_info.user_id, m_user_video.id, cr)))


def handle_video_vframe_result(db, m_user_video, i_code, s_key, s_hash):
    m_user_video.pfop_vframe_status = i_code
    cr = db.commit()
    logger.info('[{}]pfop_vframe_status -> {}, commit result: {}'.format(m_user_video.persistent_id, i_code, cr))


@app.task(bind=True, base=QueryFopsResultTask, default_retry_delay=5, max_retries=3)
def query_qiniu_video_fops_result(self, persistent_id):
    url = 'http://api.qiniu.com/status/get/prefop?id={}'.format(persistent_id)
    resp = requests.get(url)
    if resp.status_code != requests.codes.ok:
        raise self.retry()
    result = resp.json()
    logger.info(result)

    result_id = result['id']
    m_user_video = self.db.query(VideoModel).filter(VideoModel.persistent_id == result_id).first()
    if not m_user_video:
        logger.warning('unkonwn persistent id: {}'.format(result_id))
        return result.get('code')

    fops_in_progress = False
    for item in result['items']:
        cmd = item.get('cmd', '')
        code = item.get('code')
        if code not in [0, 3]:
            fops_in_progress = True
        if cmd.startswith('avthumb/mp4'):
            handle_video_transcode_result(self.db, m_user_video, code, item.get('key'), item.get('hash'))
        elif cmd.startswith('vframe/jpg'):
            handle_video_vframe_result(self.db, m_user_video, code, item.get('key'), item.get('hash'))
        else:
            logger.warning('unknonw fops: {}:{}'.format(result_id, cmd))

    if fops_in_progress:
        raise self.retry()

    return result.get('code')


'''
'items': [{
    'cmd': 'avthumb/mp4/vb/1.25m|saveas/dmlkZW8tbXA0LXRlc3Q6cG93ZXJmdWxpbzIyMi8yMDE4LzA0LzI0L2x1NGxsblZzVHduSllDTjNuUkdSeEVuNEJIVlo=',
    'code': 0,
    'desc': 'The fop was completed successfully',
    'hash': 'Fso6nM6km5FZA_ABvlM8s8Izzebi',
    'key': 'powerfulio222/2018/04/24/lu4llnVsTwnJYCN3nRGRxEn4BHVZ',
    'returnOld': 0
}, {
    'cmd': 'vframe/jpg/offset/1|saveas/dmZyYW1lLXRlc3Q6cG93ZXJmdWxpbzIyMi8yMDE4LzA0LzI0L2x1NGxsblZzVHduSllDTjNuUkdSeEVuNEJIVlo=',
    'code': 0,
    'desc': 'The fop was completed successfully',
    'hash': 'FiNnsJpVlijwv8LGsCcS0hdhtqp7',
    'key': 'powerfulio222/2018/04/24/lu4llnVsTwnJYCN3nRGRxEn4BHVZ',
    'returnOld': 0
}]
'''
