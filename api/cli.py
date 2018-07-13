#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from gunicorn.app.wsgiapp import WSGIApplication

from api.wapp import app
from entity import Facade as EntityFacade
from orm import Facade as orm_facade
from usecase import carer as carer_usecase
from usecase import recommend as recommend_usecase
from task import query_qiniu_video_fops_result


@app.shell_context_processor
def shell_context():
    return {'app': app}


def print_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        line = urllib.parse.unquote(
            "{:35s} {:30s} {}".format(rule.rule, methods, rule.endpoint)
        )
        output.append(line)
    for line in sorted(output):
        print(line)


@app.cli.command()
@click.option('--host', '-h', default='localhost')
@click.option('--port', '-p', default=8003)
@click.option('--workers', '-w', default=4)
@click.option('--timeout', '-t', default=3600)
def wsgi_server(host, port, workers, timeout):
    wsgi_app = WSGIApplication()
    wsgi_app.load_wsgiapp = lambda: app
    wsgi_app.cfg.set('bind', '%s:%s' % (host, port))
    wsgi_app.cfg.set('workers', workers)
    wsgi_app.cfg.set('timeout', timeout)
    wsgi_app.cfg.set('pidfile', None)
    wsgi_app.cfg.set('accesslog', '-')
    wsgi_app.cfg.set('errorlog', '-')
    wsgi_app.chdir()
    wsgi_app.run()


@app.cli.command()
@click.option('--host', default='localhost')
@click.option('--port', type=int, default=8003)
def debug_server(host, port):
    app.run(host, port)


@app.cli.command()
@click.option('--token', '-t', help='七牛文件上传 token')
@click.argument('filepath', required=True, metavar='filepath')
def qiniu_upload(token, filepath):
    print("upload local file: {}".format(filepath))
    from qiniu import etag, put_file
    ret, info = put_file(token, key=None, file_path=filepath, params={})
    print(ret)
    print(info)
    if ret:
        assert ret['etag'] == etag(filepath)


@app.cli.command()
@click.argument('persistent_id')
def query_fops_result(persistent_id):
    query_qiniu_video_fops_result.delay(persistent_id)


@app.cli.command()
@click.argument('user_id')
def approve_carer_apply(user_id):
    session = orm_facade.make_scoped_session()
    carer_usecase.approve_carer_application(session, user_id)
    session.close()


@app.cli.command()
def update_recommend():
    session = orm_facade.make_scoped_session()
    recommend_usecase.update_hot_carer_info_list(session, EntityFacade.redis_cli)
    session.close()


if __name__ == '__main__':
    debug_server()
