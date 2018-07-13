#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' 上传视频到七牛并执行异步操作:
        1 转码为 mp4
        2 截取视频第一帧, 保存为 jpg 图片作为视频封面
    成功会返回 persistentId, 用于查询异步转码的结果
    上传结果查询: http://api.qiniu.com/status/get/prefop?id=<persistentId>
'''

from qiniu import Auth, urlsafe_base64_encode, etag, put_file


access_key = "EWEEKOOgH774kafCEiLp7dMwQmQ7aqmnTFTlJXzf"
secret_key = "vE_TtAZM_4mM4Hi4MCTVYK39A5Lzrdnq2wJVB8gA"


def upload_image(bucket, local):
    pass


def upload_video(bucket, local):
    bucket_mp4_video = 'video-mp4-test'
    bucket_video_cover_image = 'vframe-test'
    pipeline = 'video-transcode'
    q = Auth(access_key, secret_key)

    # 构造视频转码参数
    fops_transcode = 'avthumb/mp4/vb/1.25m'
    save_key = '$(endUser)/$(year)/$(mon)/$(day)/$(etag).mp4'
    saveas_key = urlsafe_base64_encode('{}:{}'.format(bucket_mp4_video, save_key))
    fops_transcode = '{}|saveas/{}'.format(fops_transcode, saveas_key)

    # 构造截图参数
    fops_vframe = 'vframe/jpg/offset/1'
    save_key = '$(endUser)/$(year)/$(mon)/$(day)/$(etag).jpg'
    saveas_key = urlsafe_base64_encode('{}:{}'.format(bucket_video_cover_image, save_key))
    fops_vframe = '{}|saveas/{}'.format(fops_vframe, saveas_key)

    persistentOps = ';'.join([fops_transcode, fops_vframe])
    print('persistentOps: {}'.format(persistentOps))
    policy = {
        'scope': '{}:$(endUser)'.format(bucket),
        'saveKey': '$(endUser)/$(year)/$(mon)/$(day)/$(etag)$(ext)',
        'endUser': 'powerful222',
        'persistentOps': persistentOps,
        'persistentPipeline': pipeline
    }
    token = q.upload_token(bucket, policy=policy)

    ret, info = put_file(token, None, local)
    print(ret)
    print(info)
    assert ret['key'] == etag(local)
