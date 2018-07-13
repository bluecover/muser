#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

url_carer_apply = 'http://localhost:8003/v1/user/carer/apply?nosig=1'

headers = {
    "User-Agent": "MoreMom/1.0 (iPhone; iOS 11.3.1; Scale/3.00)",
    'x-user-id': '18874430',
    'did': '0900e715cc76264d7da69053863efa45',
    'token': '27c7f4cdf401828bdc38c3d9e250cbeae4cf7616d34ff87d283e0847f30a570f1000021526887669'
}

videos = {
    'intro': {
        'key': 'powerfulio222/2018/04/24/12345678',
        'mime_type': 'video/quicktime',
        'etag': '12345678',
        'size': 123456,
        'persistent_id': 'z1.5ade998d856db843bc8fe6f2',
        'duration': 20.11,
        'width': 1080,
        'height': 1920
    },
    'playground': {
        'key': 'powerfulio222/2018/04/24/ll7hmg810isB2AdQdMWStMcfCIrF',
        'mime_type': 'video/quicktime',
        'etag': 'll7hmg810isB2AdQdMWStMcfCIrF',
        'size': 24949401,
        'persistent_id': 'z1.5adef316856db843bca66e77',
        'duration': 20.22,
        'width': 1080,
        'height': 1920
    },
    'extra': [
        {
            'key': 'powerfulio222/2018/05/11/AABBCC810isB2Ad030WStMcf7112',
            'mime_type': 'video/quicktime',
            'etag': 'AABBCC810isB2Ad030WStMcf7112',
            'size': 24949401,
            'persistent_id': 'z1.5adef316856db843bca66e77',
            'duration': 60.0,
            'width': 1080,
            'height': 1920
        },
    ]
}

address = {
    'lng': 116.48355,
    'lat': 39.960726,
    'province': '北京市',
    'city': '北京市',
    'district': '海淀区',
    'address': '张自忠路3号',
    'name': '段祺瑞执政府旧址',
    'room': '6号楼3单元202室',
    'poi_id': 'eef2d5282cd7d5a73ae4a6b7'
}

birth_certificate = {
    'key': 'birth/1v6njj/2018/04/24/FmmPbkmHKNZ6j2glz1hdJoxOMNLN.jpg',
    'mime_type': 'image/jpeg',
    'etag': 'FmmPbkmHKNZ6j2glz1hdJoxOMNLN'
}

data = {
    'video': videos,
    'degree': 3,
    'address': address,
    'child_count': 2,
    'child_age_min': 0,
    'child_age_max': 3,
    'identify_result': True,
    'birth_certificate': birth_certificate
}

resp = requests.post(url_carer_apply, headers=headers, json=data)
print(resp.json())
