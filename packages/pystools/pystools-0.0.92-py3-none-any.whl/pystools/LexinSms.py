# -*- coding: utf-8 -*-
import requests
import hashlib

API_URL = "https://sdkv2.lx598.com/msgpool/sdk/"


# 乐信短信接口

class LexinSms:
    def __init__(self, app_id, app_secret, **kwargs):
        self.__dict__.update(locals())
        self.AppID = app_id
        self.AppSecret = app_secret

    @staticmethod
    def md5_hash(string):
        """Return MD5 hash of the given string."""
        return hashlib.md5(string.encode()).hexdigest().upper()

    def send_by_template(self, sign_name, template_code, template_param):
        """Send by template.
        @param template_param: 号码+模板变量值组成的 json，内容示例{"13700000001":"女士##10:10##物流公司##000000","13700000000":"先生##9:40##快递公司##1234567"}  ，其中变量值用##分割,单次最多支持2000个号码
        @param sign_name: 短信签名
        @param template_code: 短信模板ID
        """
        params = {
            'AppID': self.AppID,
            'AppSecret': self.AppSecret,
            'TemplateCode': template_code,
            'TemplateParam': template_param,
            'Format': 'JSON',
            "SignName": sign_name
        }
        response = requests.post(API_URL + "sendByTemplate", data=params)
        return response.text

    def send_sms(self, aimcodes, content):
        """Send SMS."""
        params = {
            'AppID': self.AppID,
            'AppSecret': self.AppSecret,
            'aimcodes': aimcodes,
            'content': content,
            'dataType': 'json'
        }
        response = requests.post(API_URL + "send", data=params)
        return response.text

    def qry_balance(self):
        """Query balance."""
        params = {
            'AppID': self.AppID,
            'AppSecret': self.AppSecret
        }
        response = requests.post(API_URL + "qryBalance", data=params)
        return response.text

    def qry_report(self):
        """Query report."""
        params = {
            'AppID': self.AppID,
            'AppSecret': self.AppSecret
        }
        response = requests.post(API_URL + "qryReport", data=params)
        return response.text

    def receive_sms(self):
        """Receive SMS."""
        params = {
            'AppID': self.AppID,
            'AppSecret': self.AppSecret
        }
        response = requests.post(API_URL + "receiveSms", data=params)
        return response.text


if __name__ == '__main__':
    AppID = "xxx"
    AppSecret = "xxx"
    aimcodes = "xxx"
    # content = "您正在使用本手机号绑定 {%应用名称%} ,验证码：{%验证码%}，有效时间{%有效时间%}分钟。如非本人操作，请忽略"
    content = "您正在绑定小程序,验证码：1234，有效时间10分钟。如非本人操作，请忽略。【灵感涌现】"
    sms = LexinSms(AppID, AppSecret)
    # print(sms.send_sms(aimcodes, content))

    sign_name = '灵感涌现'
    template_code = 'xxx'
    template_param = '{"xxx":"小程序##123456##10"}'
    print(sms.send_by_template(sign_name=sign_name, template_code=template_code, template_param=template_param))
