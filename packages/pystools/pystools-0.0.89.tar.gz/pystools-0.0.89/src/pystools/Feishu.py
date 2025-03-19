import json
import os
from urllib.parse import urlencode, unquote
import requests
import urllib3 as urllib3
from requests_toolbelt import MultipartEncoder
from .Logger import Loggings

urllib3.disable_warnings()
FEISHU_HTTP_POOL = urllib3.PoolManager(num_pools=1000, cert_reqs='CERT_NONE')
# 其他请求
_http_pool = urllib3.PoolManager(num_pools=5000, cert_reqs='CERT_NONE')
# const
TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal"
MESSAGE_URI = "/open-apis/im/v1/messages"
# 回复消息
MESSAGES_REPLY = '/open-apis/im/v1/messages/:message_id/reply'
DRIVE_PERMISSIONS_URI = "/open-apis/drive/v1/permissions/:token/public"
# 判断当前用户对某文档是否有某权限
DRIVE_PERMISSION_MEMBER_PERMITTED = "/open-apis/drive/permission/member/permitted"
# 获取协作者列表
DRIVE_PERMISSIONS_MEMBERS = '/open-apis/drive/v1/permissions/:token/members'

# 列出记录（旧）
# 新增记录
BITABLE_RECORDS = "/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records"

# 新增多条记录
BITABLE_RECORDS_BATCH_CREATE = "/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/batch_create"

# 查询记录
BITABLE_RECORDS_SEARCH = "/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/search"

# 删除记录/检索记录/更新记录
BITABLE_RECORD = "/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/:record_id"

# 批量删除记录
BITABLE_RECORDS_BATCH_DELETE = "/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/batch_delete"

# 更新多条记录
BITABLE_RECORDS_BATCH_UPDATE = "/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/batch_update"

# 批量获取记录
BITABLE_RECORDS_BATCH_GET = "/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/batch_get"

# 下载素材
MEDIAS_DOWNLOAD = "/open-apis/drive/v1/medias/:file_token/download"
# 获取素材临时下载链接
MEDIAS_BATCH_GET_TMP_DOWNLOAD_URL = "/open-apis/drive/v1/medias/batch_get_tmp_download_url"
# 云文档/下载文件
DRIVE_FILES_DOWNLOAD = "/open-apis/drive/v1/files/:file_token/download"
# 获取用户或机器人所在的群列表
CHATS = "/open-apis//im/v1/chats"
# 批量获取用户id
USERS_BATCH_GET_ID = "/open-apis/contact/v3/users/batch_get_id"
# 上传素材
MEDIAS_UPLOAD_ALL = "/open-apis/drive/v1/medias/upload_all"

# ------
# 创建文档
DOCUMENT_CREATE = '/open-apis/docx/v1/documents'
# 创建块
DOCUMENT_BLOCK_CREATE = '/open-apis/docx/v1/documents/:document_id/blocks/:block_id/children'
# 获取块(或所有块)
DOCUMENT_BLOCKS = "/open-apis/docx/v1/documents/:document_id/blocks/:block_id"

# ------

# 获取用户信息
CONTACT_USERS = '/open-apis/contact/v3/users/:user_id'
# 获取机器人信息
BOT_INFO = '/open-apis/bot/v3/info'
# 订阅云文档事件
FILES_SUBSCRIBE = '/open-apis/drive/v1/files/:file_token/subscribe'
# 获取应用信息
APPLICATIONS_INFO = '/open-apis/application/v6/applications/:app_id'
# 创建群
CHATS_CREATE = '/open-apis/im/v1/chats'
# 将用户或机器人拉入群聊
chat_members = '/open-apis/im/v1/chats/:chat_id/members'

# 多维表格列出字段
TABLES_FIELDS = '/open-apis/bitable/v1/apps/:app_token/tables/:table_id/fields/:field_id'

lark_host = "https://open.feishu.cn"


class Feishu(object):

    # 多维表格-新增记录、更新记录
    def bitable_records(self, app_token, table_id, param={}, record_id=None, req_body={}, **kwargs):

        """
        新增多维表格记录
        update_bitable_record([('(A)状态', "处理中"), ('(A)结果', "正在处理")])
        或使用
        ```
        update_data = {
            "app_token":file_token,
            "table_id" : table_id,
            "req_body" : {
                "fields": {
                        "(A)内容链接": "测试"
                }
            }
        }
        res = feishu.bitable_records(**update_data)
        ```

        更新多维表格记录

        update_bitable_record([('(A)状态', "处理中"), ('(A)结果', "正在处理")],record_id)
                    或使用
                    ```
        update_data = {
            "app_token":file_token,
            "table_id" : table_id,
            "record_id" : record_id,
            "req_body" : {
                "fields": {
                        "(A)内容链接": "测试"
                }
            }
        }
        res = feishu.bitable_records(**update_data)
        ```
        """
        self.__dict__.update(locals())

        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, BITABLE_RECORDS
        ).replace(":app_token", app_token).replace(":table_id", table_id)
        action = "GET"
        if req_body:
            action = "POST"
        if record_id:
            url = "{}/{}".format(url, record_id)
            if req_body:
                action = "PUT"
        if param:
            url = url + "?" + urlencode(param)
        resp = self.req_feishu_api(action, url=url, req_body=req_body)
        return resp.get("data") if resp else None

    def bitable_records_batch_create(self, app_token, table_id, req_body={}, param={}, **kwargs):

        """
        req_body = {
                "records": [
                    {
                        "fields": {
                            "多行文本": "多行文本内容",
                            "条码": "qawqe",
                            "数字": 100,
                            "货币": 3,
                            "评分": 3,
                            "进度": 0.25,
                            "单选": "选项1",
                            "多选": ["选项1", "选项2"],
                            "日期": 1674206443000,
                            "复选框": true,
                            "人员": [
                                {
                                    "id": "ou_2910013f1e6456f16a0ce75ede950a0a"
                                },
                                {
                                    "id": "ou_e04138c9633dd0d2ea166d79f548ab5d"
                                }
                            ],
                            "群组": [
                                {
                                    "id": "oc_cd07f55f14d6f4a4f1b51504e7e97f48"
                                }
                            ],
                            "电话号码": "13026162666",
                            "超链接": {
                                "text": "飞书多维表格官网",
                                "link": "https://www.feishu.cn/product/base"
                            },
                            "附件": [
                                {
                                    "file_token": "Vl3FbVkvnowlgpxpqsAbBrtFcrd"
                                }
                            ],
                            "单向关联": ["recHTLvO7x", "recbS8zb2m"],
                            "双向关联": ["recHTLvO7x", "recbS8zb2m"],
                            "地理位置": "116.397755,39.903179"
                        }
                    }
                ]
            }
        """

        self.__dict__.update(locals())

        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, BITABLE_RECORDS_BATCH_CREATE
        ).replace(":app_token", app_token).replace(":table_id", table_id)
        action = "POST"
        if param:
            url = url + "?" + urlencode(param)
        resp = self.req_feishu_api(action, url=url, req_body=req_body)
        return resp.get("data") if resp else None

    # 多维表格-新增记录/列出记录
    def bitable_records_search(self, app_token, table_id, param={}, req_body={}, **kwargs):

        """
        根据条件查询多维表格记录
        ```
        query_data = {
            "app_token":file_token,
            "param" : {'page_size':100,'page_token':"eVQrYzJBNDNONlk4VFZBZVlSdzlKdFJ4bVVHVExENDNKVHoxaVdiVnViQT0="},
            "table_id" : table_id,
            "req_body" : {
                          "view_id": "vewqhz51lk",
                          "field_names": [
                            "字段1",
                            "字段2"
                          ],
                          "sort": [
                            {
                              "field_name": "多行文本",
                              "desc": true
                            }
                          ],
                          "filter": {
                            "conjunction": "and",
                            "conditions": [
                              {
                                "field_name": "字段1",
                                "operator": "is",
                                "value": [
                                  "文本内容"
                                ]
                              }
                            ]
                          },
                          "automatic_fields": false #控制是否返回自动计算的字段
                        }
        }
        print(feishu.drive_permissions_members(token=file_token, type="bitable"))
        res = feishu.bitable_records_search(**query_data)
        ```
        """
        self.__dict__.update(locals())

        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, BITABLE_RECORDS_SEARCH
        ).replace(":app_token", app_token).replace(":table_id", table_id)
        action = "POST"
        if param:
            url = url + "?" + urlencode(param)
        resp = self.req_feishu_api(action, url=url, req_body=req_body)
        return resp.get("data") if resp else None

    def update_bitable_record(self, file_token, table_id, update_data, record_id=None, **kwargs):
        """
        更新多维表格的数据
        :param feishu:
        :param file_token:
        :param table_id:
        :param update_data: 格式如 [('(A)状态', "处理中"), ('(A)结果', "正在处理")]
        :param record_id: 如果不传，就是新增一条数据
        :return:
        """
        self.__dict__.update(locals())
        # update_data 是一个数组，里面是元组，元组里面是字段名和字段值
        data = {
            'fields': {
                # '(A)状态': "处理中",
                # '(A)结果': "正在处理"
            }
        }
        # 将update_data里面的数据添加到data里面
        for item in update_data:
            data['fields'][item[0]] = item[1]
        res = self.bitable_records(file_token, table_id, record_id=record_id, req_body=data)
        return res
    

    def update_bitable_record2(self, file_token, table_id, update_data, record_id=None, **kwargs):
        """
        更新多维表格的数据
        :param feishu:
        :param file_token:
        :param table_id:
        :param update_data: 格式如 [{'(A)状态': "处理中"}, {'(A)结果': "正在处理"}]
        :param record_id: 如果不传，就是新增一条数据
        :return:
        """
        self.__dict__.update(locals())
        # update_data 是一个数组，里面是字典，字典里面是字段名和字段值
        data = {
            'fields': {
                # '(A)状态': "处理中",
                # '(A)结果': "正在处理"
            }
        }
        # 将update_data里面的数据添加到data里面
        for item in update_data:
            data['fields'].update(item)
        res = self.bitable_records(file_token, table_id, record_id=record_id, req_body=data)
        return res

    def __init__(self, app_id, app_secret,
                 print_feishu_log=True, logger=Loggings(), **kwargs):

        """
        :param app_id:
        :param app_secret:
        :param lark_host:

        """
        self.__dict__.update(locals())
        if not app_id or not app_secret:
            raise ValueError("app_id or app_secret is empty")

        self.logger = logger
        self._tenant_access_token = ""

        self._app_id = app_id
        self._app_secret = app_secret
        self.print_feishu_log = print_feishu_log

    @property
    def tenant_access_token(self):
        return self._tenant_access_token

    def _authorize_tenant_access_token(self):
        # get tenant_access_token and set, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal
        url = "{}{}".format(lark_host, TENANT_ACCESS_TOKEN_URI)
        req_body = {"app_id": self._app_id, "app_secret": self._app_secret}
        response = self.req_feishu_api("POST", url, req_body)
        self._tenant_access_token = response.get("tenant_access_token", "")

    def _check_error_response(self, resp, check_code, check_status, url=None, req_body=None, headers=None):
        # check if the response contains error information
        self._handle_resp_code(resp, url)
        if check_status:
            if resp.status != 200:
                try:
                    response_dict = json.loads(resp.data.decode('utf-8'))
                    raise LarkException(code=response_dict.get("code", -1), msg=resp.data.decode('utf-8'), url=url,
                                        req_body=req_body, headers=headers)
                except:
                    raise LarkException(code=resp.status, msg="response status: {}  ,response data: {} ".format(
                        resp.status, resp.data.decode('utf-8')),
                                        url=url,
                                        req_body=req_body, headers=headers)
        # response_dict = resp.json()
        if check_code:
            response_dict = json.loads(resp.data.decode('utf-8'))
            code = response_dict.get("code", -1)
            if code != 0:
                self.logger.error("url:{},response:{}".format(url, response_dict))
                raise LarkException(code=code, msg=response_dict.get("msg"), url=url, req_body=req_body,
                                    headers=headers)

    def _handle_resp_code(self, resp, req_url):
        try:
            response_dict = json.loads(resp.data.decode('utf-8'))
            code = response_dict.get("code")
            if code != 0:
                msg_type = 'post'
                msg = {
                    "zh_cn": {
                        "title": '接口请求异常',
                        "content": [
                            [{
                                "tag": "text",
                                "text": '请求接口: {}\n'.format(req_url)
                            },
                                {
                                    "tag": "text",
                                    "text": '返回异常: {} \n'.format(
                                        json.dumps(response_dict, ensure_ascii=False, indent=4, separators=(',', ': ')))
                                }
                            ],
                            [{
                                "tag": "text",
                                "text": "使用方法见 :\n"
                            }, {
                                "tag": "a",
                                "href": "https://zhidateam.feishu.cn/docx/HXwhdg00eoXYPmxb1VncvcNbnvv",
                                "text": "机器人使用手册"
                            }]
                        ]
                    }
                }
                self.notify_send(msg_type, msg)
        except:
            self.logger.info("{} 返回值不是json格式".format(req_url))

    def req_feishu_api(self, action, url, req_body={}, check_code=True, check_status=True):
        # sleep(0.1)
        if self.print_feishu_log:
            self.logger.info("{} 请求飞书接口：{}".format(action, unquote(url)))
            self.logger.info("请求体：{}".format(req_body))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.tenant_access_token,
        }
        if req_body:
            encoded_body_data = json.dumps(req_body, cls=MyEncoder, indent=4).encode("utf-8")
            resp = FEISHU_HTTP_POOL.request(method=action, headers=headers, url=url, body=encoded_body_data)
        else:
            resp = FEISHU_HTTP_POOL.request(method=action, headers=headers, url=url)
        resp_data = resp.data
        resp_header = resp.info()
        content_type = resp_header.get('Content-Type')

        Content_Disposition = resp_header.get('Content-Disposition')
        if Content_Disposition:
            if 'attachment' in Content_Disposition:
                if str(content_type).__contains__("json"):
                    resp_msg = resp.data.decode('utf-8')
                    try:
                        resp_dict = json.loads(resp_msg)
                    except:
                        return {'content_type': content_type, 'file_bytes': resp_data}
                    code = resp_dict.get("code", None)
                    msg = resp_dict.get("msg", None)
                    error = resp_dict.get("error", None)
                    if code and msg and error:
                        raise LarkException(code=code, msg=json.dumps(resp_dict, ensure_ascii=False), url=url,
                                            req_body=req_body, headers=headers)

                return {'content_type': content_type, 'file_bytes': resp_data}

        resp_msg = resp.data.decode('utf-8')
        if self.print_feishu_log:
            self.logger.info("飞书接口响应：{}".format(resp_msg))

        self._check_error_response(resp, check_code, check_status, unquote(url), headers)
        try:
            response_dict = json.loads(resp_msg)
            return response_dict
        except:
            return resp_msg

        # # resp.release_conn()
        # if str(content_type).__contains__("json") or str(content_type).__contains__("text/plain"):
        #     # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'[{}, {}:{} ]: '.format(sys._getframe(1).f_code.co_name, sys._getframe().f_code.co_name,
        #     #                               sys._getframe().f_lineno + 1), "飞书接口响应", resp.data.decode('utf-8'))
        #     resp_msg = resp.data.decode('utf-8')
        #     if print_feishu_log:
        #         self.logger.info("飞书接口响应：{}".format(resp_msg))
        #
        #     self._check_error_response(resp, check_code, check_status, unquote(url))
        #     try:
        #         response_dict = json.loads(resp_msg)
        #         return response_dict
        #     except:
        #         return resp_msg
        #
        # else:
        #     # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'[{}, {}:{} ]: '.format(sys._getframe(1).f_code.co_name, sys._getframe().f_code.co_name,
        #     #                               sys._getframe().f_lineno + 1), "飞书接口响应", "二进制文件流" )
        #     if print_feishu_log:
        #         self.logger.info("飞书接口响应  二进制文件流")
        #     return {"content_type": content_type, "file_bytes": resp_data}

    # 云文档权限设置，加参数表示更新
    # https://open.feishu.cn/open-apis/drive/v1/permissions/:token/public
    # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/drive-v1/permission-public/patch
    def drive_permissions(self, token, file_type, req_body={}, **kwargs):
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}?type={}".format(
            lark_host, DRIVE_PERMISSIONS_URI, file_type
        ).replace(":token", token)
        action = "GET"
        if req_body:
            action = "PATCH"
        resp = self.req_feishu_api(action, url=url, req_body=req_body)
        return resp.get("data") if resp else None

    def bitable_record_delete(self, file_token, table_id, record_id, **kwargs):
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, BITABLE_RECORD
        ).replace(":app_token", file_token).replace(":table_id", table_id).replace(":record_id", record_id)
        action = "DELETE"
        resp = self.req_feishu_api(action, url=url)
        return resp.get("data") if resp else None

    def bitable_records_batch_delete(self, file_token, table_id, record_ids: list, **kwargs):
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, BITABLE_RECORDS_BATCH_DELETE
        ).replace(":app_token", file_token).replace(":table_id", table_id)
        action = "POST"
        req_body = {
            "records": record_ids
        }
        resp = self.req_feishu_api(action, url=url, req_body=req_body)
        return resp.get("data") if resp else None

    def bitable_record(self, file_token, table_id, record_id, **kwargs):
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, BITABLE_RECORD
        ).replace(":app_token", file_token).replace(":table_id", table_id).replace(":record_id", record_id)
        action = "GET"
        resp = self.req_feishu_api(action, url=url)
        return resp.get("data") if resp else None

    def bitable_records_batch_get(self, file_token, table_id, record_ids: list, with_shared_url=False,
                                  automatic_fields=True, user_id_type="open_id", **kwargs):
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, BITABLE_RECORDS_BATCH_GET
        ).replace(":app_token", file_token).replace(":table_id", table_id)
        action = "POST"
        req_body = {
            "record_ids": record_ids,
            "with_shared_url": with_shared_url,
            "automatic_fields": automatic_fields,
            "user_id_type": user_id_type
        }
        resp = self.req_feishu_api(action, url=url, req_body=req_body)
        return resp.get("data") if resp else None

    def bitable_records_batch_update(self, file_token, table_id, req_body, param={}, **kwargs):
        '''
        req_body = {
                "records": [
                    {
                        "record_id": "reclAqylTN",
                        "fields": {
                            "索引": "索引列多行文本类型",
                            "多行文本": "多行文本内容",
                            "数字": 100,
                            "单选": "选项3",
                            "多选": [
                                "选项1",
                                "选项2"
                            ],
                            "日期": 1674206443000,
                            "条码": "qawqe",
                            "复选框": true,
                            "人员": [
                                {
                                    "id": "ou_2910013f1e6456f16a0ce75ede950a0a"
                                },
                                {
                                    "id": "ou_e04138c9633dd0d2ea166d79f548ab5d"
                                }
                            ],
                            "群组": [
                                {
                                    "id": "oc_cd07f55f14d6f4a4f1b51504e7e97f48"
                                }
                            ],
                            "电话号码": "13026162666",
                            "超链接": {
                                "text": "飞书多维表格官网",
                                "link": "https://www.feishu.cn/product/base"
                            },
                            "附件": [
                                {
                                    "file_token": "Vl3FbVkvnowlgpxpqsAbBrtFcrd"
                                }
                            ],
                            "单向关联": [
                                "recHTLvO7x",
                                "recbS8zb2m"
                            ],
                            "双向关联": [
                                "recHTLvO7x",
                                "recbS8zb2m"
                            ],
                            "地理位置": "116.397755,39.903179",
                            "评分": 3,
                            "货币": 3,
                            "进度": 0.25
                        }
                    }
                ]
            }
        '''
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, BITABLE_RECORDS_BATCH_UPDATE
        ).replace(":app_token", file_token).replace(":table_id", table_id)
        action = "POST"
        if param:
            url = url + "?" + urlencode(param)
        resp = self.req_feishu_api(action, url=url, req_body=req_body)
        return resp.get("data") if resp else None

    def medias_download(self, file_token, param={}):
        file_res = self.medias_download_to_bytes(file_token, param={})
        file_bytes = file_res.get("file_bytes")

        subfix = file_res.get("content_type").split("/")[1]
        filename = file_token + "." + subfix

        return filename, file_bytes

    def medias_download_to_bytes(self, file_token, param={}):
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, MEDIAS_DOWNLOAD
        ).replace(":file_token", file_token)
        if param:
            url = url + "?" + urlencode(param)
        resp = self.req_feishu_api("GET", url=url, check_code=False)
        content_type = resp.get("content_type")
        file_bytes = resp.get("file_bytes")
        res = {"content_type": content_type, "file_bytes": file_bytes}
        return res

    def medias_batch_get_tmp_download_url(self, file_tokens):
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, MEDIAS_BATCH_GET_TMP_DOWNLOAD_URL
        )

        url = url + "?" + urlencode({"file_tokens": file_tokens})
        resp = self.req_feishu_api("GET", url=url, check_code=False)
        return resp.get("data") if resp else None

    def drive_files_download_to_bytes(self, file_token):
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, DRIVE_FILES_DOWNLOAD
        ).replace(":file_token", file_token)
        resp = self.req_feishu_api("GET", url=url, check_code=False)
        content_type = resp.get("content_type")
        file_bytes = resp.get("file_bytes")
        res = {"content_type": content_type, "file_bytes": file_bytes}
        return res

    def medias_download_to_local_file(self, file_token, local_path, param={}):
        file_res = self.medias_download_to_bytes(file_token, param={})
        file_bytes = file_res.get("file_bytes")
        with open(local_path, "wb") as fp:
            json.dump(file_bytes, fp)
        return local_path

    def get_feushu_file_url(self, file_token_block: dict) -> str:
        self._authorize_tenant_access_token()
        """
        :param file_token_block:  格式如  {"file_token":"xxxxx","type":"image/png"}
        :return:
        """
        res = self.medias_download(file_token_block.get("file_token"))
        # print(res)
        # 请补充异常校验
        return res

    def im_msg_send_text_with_open_id(self, open_id, content, **kwargs):
        self.__dict__.update(locals())
        self.im_msg_send("open_id", open_id, "text", content)

    def im_msg_send(self, receive_id_type, receive_id, msg_type, content, **kwargs):
        self.__dict__.update(locals())
        """

        :param receive_id_type:  消息接收者id类型
                                可选值有：
                                open_id：以open_id来识别用
                                user_id：以user_id来识别用户需要有获取用户 userID的权限
                                union_id：以union_id来识别用户
                                email：以email来识别用户。是用户的真实邮箱
                                chat_id：以chat_id来识别群聊。群ID说明请参考：群ID说明
        :param receive_id: 依据receive_id_type的值，填写对应的消息接收者id
        :param msg_type: 消息类型 包括：text、post、image、file、audio、media、sticker、interactive、share_chat、share_user等，
        :param content:
        :return:
        """
        self._authorize_tenant_access_token()
        url = "{}{}?receive_id_type={}".format(
            lark_host, MESSAGE_URI, receive_id_type
        )
        req_body = {
            "receive_id": receive_id,
            "content": content,
            "msg_type": msg_type,
        }
        resp = self.req_feishu_api("POST", url=url, req_body=req_body)
        return resp

    def messages_reply(self, message_id, msg_type, content, **kwargs):
        self.__dict__.update(locals())
        """

        :param message_id:  待回复的消息的ID
        :param msg_type: 消息类型，包括：text、post、image、file、audio、media、sticker、interactive、share_card、share_user
        :param content:  消息内容 json 格式，格式说明参考: 发送消息Content。示例值："{"text":"<at user_id="ou_155184d1e73cbfb8973e5a9e698e74f2">Tomtest content"}"
        :return:
        """
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, MESSAGES_REPLY
        ).replace(':message_id', message_id)
        req_body = {
            "content": content,
            "msg_type": msg_type,
            # "uuid": uuid.uuid4()
        }
        resp = self.req_feishu_api("POST", url=url, req_body=req_body)
        return resp

    # 获取用户或机器人所在的群列表
    def charts(self, param={}):
        self._authorize_tenant_access_token()
        url = "{}{}?page_size=".format(
            lark_host, CHATS, 100
        )
        if param:
            url = url + "&" + urlencode(param)
        action = "GET"
        resp = self.req_feishu_api(action, url=url)
        return resp.get("data") if resp else None

    # 批量获取用户ID
    def users_batch_get_id(self, req_body, param={}):
        """

        :param param:
            可选值有：
            open_id：用户的 open id
            union_id：用户的 union id
            user_id：用户的 user id
            默认值：open_id

        :req_body:
            {
                "emails": [
            "zhangsan@z.com","lisi@a.com"
                ],
                "mobiles": [
            "13812345678","13812345679"
                ]
            }
        :return:
        """
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, USERS_BATCH_GET_ID
        )
        if param:
            url = url + "?" + urlencode(param)
        action = "POST"
        resp = self.req_feishu_api(action, url=url, req_body=req_body)
        return resp.get("data") if resp else None

        # 批量获取用户ID

    # 上传文件到飞书
    def upload_file(self, parent_node, file_name, file_path_or_binary, parent_type, **kwargs):
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()

        url = "{}{}".format(
            lark_host, MEDIAS_UPLOAD_ALL
        )
        # print(type(file_path_or_binary))
        file_size = 0
        if type(file_path_or_binary) is bytes:
            file_binary = file_path_or_binary
            file_size = len(file_binary)
        elif type(file_path_or_binary) is str:
            if os.path.isfile(file_path_or_binary):
                file_size = os.path.getsize(file_path_or_binary)
                # file_binary = (open(file_path_or_binary, 'rb'))  #BufferedReader
                with open(file_path_or_binary, 'rb') as f:
                    file_binary = f.read()  # bytes
            else:
                raise LarkException(code=-1,
                                    msg="file_path_or_binary参数：{} 应该是文件路径".format(file_path_or_binary),
                                    url=url)
        else:
            raise LarkException(code=-1,
                                msg="file_path_or_binary参数：{} 应该是文件路径或bytes".format(file_path_or_binary),
                                url=url)

        form = {'file_name': file_name,
                'parent_type': parent_type,
                'parent_node': parent_node,
                'size': str(file_size),
                'file': file_binary
                }
        headers = {
            'Authorization': "Bearer " + self.tenant_access_token,
        }
        multi_form = MultipartEncoder(form)
        headers['Content-Type'] = multi_form.content_type
        response = requests.request("POST", url, headers=headers, data=multi_form)
        # print(response.status_code)

        if response.status_code != 200:
            if response.status_code in [403, 400]:
                response_dict = json.loads(response.content.decode('utf-8'))
                raise LarkException(code=response_dict.get("code", -1), msg=response.content.decode('utf-8'), url=url)
            else:
                raise LarkException(response.status_code, msg=response.content.decode('utf-8'), url=url)
        # response_dict = resp.json()
        response_dict = json.loads(response.content.decode('utf-8'))
        code = response_dict.get("code", -1)
        if code != 0:
            self.logger.error("url:{},response:{}".format(url, response_dict))
            raise LarkException(code=code, msg=response_dict.get("msg"), url=url)

        return response_dict.get("data")

    def documents_create(self, title, folder_token=None):
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, DOCUMENT_CREATE
        )
        # 标题只留前800个字符
        if len(title) > 800:
            title = title[:800]
        req_body = {
            "title": title,
            "folder_token": folder_token,
        }
        if not folder_token:
            req_body.pop("folder_token")

        resp = self.req_feishu_api("POST", url=url, req_body=req_body)
        return resp

    def documents_block_create(self, document_id, children=[], index=-1, block_id=None):
        """
        创建文档块
        见文档：https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/create

        :param document_id: 文档ID
        :param children: 块内容，长度范围：1 ～ 50。在一次请求中，你最多可以创建 5 个电子表格（Sheet）块
        :param index: 指定在某个块的子块列表中，新创建的子块的放置位置。索引的起始值为 0，表示子块列表的第一个位置；索引的最大值为某个块的子块数量，表示子块列表的最后一个位置。例如：一个块的子块列表中有 5 个子块，那么它们的索引分别为 0、1、2、3、4。如果要在该块的子块列表的中放置一个新创建的子块，并将其放置到第一个位置，那么索引值应为 0；如果要将新创建的子块放置到最后一个位置，那么索引值应为 -1
        :param block_id: 块ID,如果不传，表示文档树根节点创建子块
        :return:
        """
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        if not block_id:
            block_id = document_id
        url = "{}{}".format(
            lark_host, DOCUMENT_BLOCK_CREATE
        ).replace(":document_id", document_id).replace(":block_id", block_id)
        req_body = {
            "index": index,
            "children": children
        }
        resp = self.req_feishu_api("POST", url=url, req_body=req_body)
        return resp

    # 获取文档块
    def document_blocks(self, document_id, block_id="", param={}, **kwargs):
        """
        获取文档块
        :param document_id: 文档ID
        :param block_id: 块ID，如果不传，表示查询所有块，传入表示获取块内容
        :param param: 查询参数
        :return:
        """
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}?page_size=500".format(
            lark_host, DOCUMENT_BLOCKS
        ).replace(":document_id", document_id).replace(":block_id", block_id)

        action = "GET"
        if param:
            url = url + "&" + urlencode(param)
        resp = self.req_feishu_api(action, url=url)
        return resp.get("data") if resp else None

    # 获取或更新用户信息
    def get_contact_users(self, user_id, param='', user_info={}, **kwargs):
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, CONTACT_USERS
        ).replace(":user_id", user_id)

        action = "GET"
        if param:
            url = url + "?" + urlencode(param)
        resp = self.req_feishu_api(action, url=url)
        return resp.get("data") if resp else None

    def bot_permitted(self, token, type, perm='full_access', **kwargs):
        """
        判断机器人是否有某个文档的权限
        :param token: 文件的 token
        :param type:文档类型，可选 doc、docx、sheet、bitable、file
        :param perm: 权限，"view" or "edit" or "full_access"
        :return:
        """
        self.__dict__.update(locals())
        # res = self.drive_permissions_members(token, type)
        # items = res.get('items')
        # if not items:
        #     return False
        #
        # bot_info = self.bot_info()
        # for item in items:
        #     member_id = item.get('member_id')
        #     member_perm = item.get('perm')
        #     if member_id == bot_info.get('open_id') and member_perm == perm:
        #         return True
        # return False

        # 目前不支持获取机器人类别的协作者，只能用如下方法了
        return self.drive_permission_member_permitted(token, type)

    def drive_permission_member_permitted(self, token, type, perm='edit', **kwargs):
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, DRIVE_PERMISSION_MEMBER_PERMITTED
        )

        req_body = {
            "token": token,
            "type": type,
            "perm": perm
        }
        action = "POST"
        resp = self.req_feishu_api(action, url=url, req_body=req_body)

        return resp.get("data").get('is_permitted')

    def drive_permissions_members(self, token, type, **kwargs):
        """
        :param token: 文件的 token
        :param type:文档类型，可选 doc、docx、sheet、bitable、file
        :return:
        """
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}?type={}&fields=*".format(
            lark_host, DRIVE_PERMISSIONS_MEMBERS, type
        ).replace(':token', token)
        action = "GET"
        resp = self.req_feishu_api(action, url=url)

        return resp.get("data") if resp else None

    def notify_send(self, msg_type, msg, receive_id_type, receive_id, **kwargs):
        """

        :param receive_id_type:
        :param receive_id:
        :param msg_type:
        :param msg:  格式见 https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json
        :return:
        """
        self.__dict__.update(locals())
        content = json.dumps(msg, ensure_ascii=False)
        if not receive_id_type or not receive_id:
            # 如果没有配置默认通知的群,就给应用owner发信息
            applications_info = self.applications_info()
            receive_id_type = 'open_id'
            receive_id = applications_info.get('owner').get('owner_id')

        # if receive_id_type == 'open_id':
        #     msg_type = 'text'
        #     msg = {
        #         "text": "建议将建立一个预警群，将预警信息发送到群里面让先相关的人员都关注到，如果需要建立预警群，请将群信息配置到系统"
        #     }

        res = self.im_msg_send(receive_id_type=receive_id_type, receive_id=receive_id, msg_type=msg_type,
                               content=content)
        return res

    # 获取机器人信息
    def bot_info(self):
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, BOT_INFO
        )
        action = "GET"
        resp = self.req_feishu_api(action, url=url)
        return resp.get("bot") if resp else None

    # 获取机器人信息
    def applications_info(self, user_id_type='open_id'):
        self._authorize_tenant_access_token()
        app_id = self.feishu_conf.get('app_id')
        url = "{}{}?lang=zh_cn&user_id_type={}".format(
            lark_host, APPLICATIONS_INFO, user_id_type
        ).replace(':app_id', 'me')
        action = "GET"
        resp = self.req_feishu_api(action, url=url)
        if resp:
            return resp.get("data", {}).get('app')
        else:
            return None

    def files_subscribe(self, file_type, file_token, **kwargs):
        """
        订阅云文档事件
        :param file_type:  doc：文档、docx：新版文档、sheet：表格、bitable：多维表格
        :param file_token:
        :return:
        """
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}?file_type={}".format(
            lark_host, FILES_SUBSCRIBE, file_type
        ).replace(':file_token', file_token)
        action = "POST"
        resp = self.req_feishu_api(action, url=url, check_code=False, check_status=False)
        return resp

    # 列出字段、新增字段、更新字段、删除字段
    """
    GET是列出字段
    没有 req_body 和 field_id
    POST是新增字段
    有 req_body 和 没有 field_id
    PUT是更新字段
    有 req_body 和 field_id
    DELETE是删除字段
    没有 req_body 和 field_id
    """
    def tables_fields(self, app_token, table_id, query_params=None, field_id="", req_body=None):
        self.__dict__.update(locals())
        self._authorize_tenant_access_token()
        url = "{}{}".format(
            lark_host, TABLES_FIELDS
        ).replace(':app_token', app_token).replace(':table_id', table_id).replace(':field_id', field_id)

        # 如果url是以/结尾的，就去掉
        if url[-1] == '/':
            url = url[:-1]

        if query_params:
            url = url + "?" + urlencode(query_params)

        if not req_body and not field_id:
            action = "GET"
        elif req_body and not field_id:
            action = "POST"
        elif req_body and field_id:
            action = "PUT"
        elif not req_body and field_id:
            action = "DELETE"

        resp = self.req_feishu_api(action, url=url, req_body=req_body)
        return resp.get('data') if resp else None

    def create_table_field(self, app_token, table_id, req_body):
        """
        创建表格字段
        req_body = {
            "field_name": "文本",
            "type": 1
        }
        """
        return self.tables_fields(app_token=app_token, table_id=table_id, req_body=req_body)
        
    # 获取表格字段信息
    def tables_fields_info(self, field_names: list, app_token, table_id, query_params={}):
        """
        获取表格字段信息
        :param field_names: 字段名列表 ["字段名1","字段名2","字段名3"]
        :param app_token:
        :param table_id:
        :param query_params:留空即可

        返回值中：
        type可选值有：
            1：多行文本
            2：数字
            3：单选
            4：多选
            5：日期
            7：复选框
            11：人员
            13：电话号码
            15：超链接
            17：附件
            18：关联
            20：公式
            21：双向关联
            22：地理位置
            23：群组
            1001：创建时间
            1002：最后更新时间
            1003：创建人
            1004：修改人
            1005：自动编号
        """
        query_params['page_size'] = 100
        field_name_dicts = []
        for field_name in field_names:
            if type(field_name) is str:
                field_name_dicts.append({"field_name": field_name})
            else:
                field_name_dicts.append(field_name)

        tables_fields_res = self.tables_fields(app_token, table_id, query_params)
        has_more = tables_fields_res.get('has_more')
        if not has_more:
            field_items = tables_fields_res.get('items')
            for field_item in field_items:
                field_name = field_item.get('field_name')
                for field_name_dict in field_name_dicts:
                    if field_name_dict.get('field_name') == field_name:
                        field_name_dict.update(field_item)

            return field_name_dicts

        query_params['page_size'] = 100
        query_params['page_token'] = tables_fields_res.get('page_token')
        self.tables_fields_info(field_name_dicts, app_token, table_id, query_params)

    def send_webhook_msg(self, webhook, msg_type, content, **kwargs):
        """
        发送webhook消息
        :param webhook:
        :param msg_type:
        :param content:
        :return:
        """
        self.__dict__.update(locals())
        req_data = json.dumps({
            "msg_type": msg_type,
            "content": content
        }, ensure_ascii=False).encode('utf-8')

        # curl -X POST -H "Content-Type: application/json" \
        # 	-d '{"msg_type":"text","content":{"text":"request example"}}' \
        #   https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxxx
        headers = {'Content-Type': 'application/json'}
        resp = _http_pool.request(method='POST', url=webhook, body=req_data, headers=headers)

        # resp, check_code, check_status, url=None, req_body=None, headers=None
        self._check_error_response(resp=resp, check_code=True, check_status=True, url=webhook, req_body=req_data,
                                   headers=headers)
        resp_msg = resp.data.decode('utf-8')
        resp_dict = json.loads(resp_msg)
        return resp_dict.get('data')


class LarkException(Exception):
    def __init__(self, code=0, msg=None, url=None, req_body=None, headers=None):
        self.url = url
        self.req_body = req_body
        self.code = code
        self.msg = msg
        self.headers = headers

    def __str__(self) -> str:
        # if self.url:
        #     return "{} | {}  | {} | ".format(self.url, self.code, self.msg)
        # return "{}:{}".format(self.code, self.msg)
        return f"code:{self.code} | msg:{self.msg} | url:{self.url} | headers:{self.headers} | req_body:{self.req_body}"

    __repr__ = __str__


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)
