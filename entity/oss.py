#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class OSSCeleryTaskProxy():

    def __init__(self, oss_task_add_ref):
        self.oss_task_add_ref = oss_task_add_ref

    def add_object_reference(self, i_user_id, s_ref_tag, d_object_info):
        self.oss_task_add_ref.delay(i_user_id, s_ref_tag, d_object_info)
