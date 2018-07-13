#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import toml
from orm import Facade
from orm.orm_mysql import UserCarerInfoModel, PlaygroundModel, UserAddressModel
from tool.randname import random_han_name


config = toml.load('config/local.toml')
Facade.initialize(config['mysql'])


def build_random_address():
    return {
        'district': random_han_name(2) + '区',
        'street': '{}路{}号{}'.format(random_han_name(3), random.randint(1, 50)),
        'room': '{}单元{}室'.format(random.randint(1, 10), random.randint(8, 100))
    }


good_address = [
    {
        'district': '朝阳区',
        'street': '亮马桥路27号院',
        'room': '1903号大鱼公司'
    },
    {
        'district': '海淀区',
        'street': '张自忠路3号段祺瑞执政府旧址',
        'room': '6号楼3单元202室'
    }
]

address_lsit = good_address + [build_random_address() for _ in range(0, 3)]


playground_1 = PlaygroundModel(
    id=1,
    user_id=137,
    address_id=1,
    create_ts=int(time.time())
)
playground_2 = PlaygroundModel(
    id=2,
    user_id=138,
    address_id=2,
    create_ts=int(time.time())
)

carer_1 = UserCarerInfoModel(
    user_id=137,
    intro_video_url='http://p5zmpa3g9.bkt.clouddn.com/FnFeKTEBuzjeWnju8jyINabMLzh2',
    intro_video_cover_url='http://p64mbauav.bkt.clouddn.com/FnFeKTEBuzjeWnju8jyINabMLzh2.jpg',
    playground_video_url='http://p5zmpa3g9.bkt.clouddn.com/IMG_0181.mp4',
    playground_video_cover_url='http://p64mbauav.bkt.clouddn.com/IMG_0181.mp4.jpg',
    id_card_pic_url='',
    birth_certificate_url='',
    degree=1,
    care_exp=2,
    child_age_min=1,
    child_age_max=6,
    playground_id=1,
    create_ts=int(time.time())
)

carer_2 = UserCarerInfoModel(
    user_id=138,
    intro_video_url='http://p5zmpa3g9.bkt.clouddn.com/video/2018/04/1114gq_FseK9glvYqKgECLnupyZSWDWXjTn',
    intro_video_cover_url='http://p64mbauav.bkt.clouddn.com/video/2018/04/1114gq_FseK9glvYqKgECLnupyZSWDWXjTn.jpg',
    playground_video_url='http://p5zmpa3g9.bkt.clouddn.com/test.mp4',
    playground_video_cover_url='http://p64mbauav.bkt.clouddn.com/test.mp4.jpg',
    id_card_pic_url='',
    birth_certificate_url='',
    degree=2,
    care_exp=1,
    child_age_min=5,
    child_age_max=8,
    playground_id=2,
    create_ts=int(time.time())
)


session = Facade.make_session()
session.query(UserAddressModel.delete)
session.query(PlaygroundModel.delete)
session.query(UserCarerInfoModel.delete)
session.add(playground_1)
session.add(playground_2)
session.add(carer_1)
session.add(carer_2)
session.commit()
