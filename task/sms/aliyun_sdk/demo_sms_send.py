# -*- coding: utf-8 -*-
import sys
import uuid

from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT
"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass
except Exception as err:
    raise err

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

ACCESS_KEY_ID = "LTAI7dT85swg955B"
ACCESS_KEY_SECRET = "UE2FfNEkUfiO3zxeh3iWfe9MvlP2NR"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    smsRequest.set_method(MT.POST)

    # 数据提交格式
    smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse


#if __name__ == '__main__':
#    __business_id = uuid.uuid1()
#    #print(__business_id)
#    params = "{\"code\":\"12345\"}"
#    #params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
#    resposne = send_sms(__business_id, "15727300213", "摩尔妈妈", "SMS_129440028", params)
#    print(resposne)
