import os
import traceback

import requests
# import urllib3
# from utils.logger import log as logger


def send_sys_error(content:str, to:list = ["feishu"], at:list = [],
                   spl_callback_url=os.getenv("SPL_CALLBACK_URL"),
                   feishu_webhook_url=os.getenv("FEISHU_WEBHOOK_URL"),
                   ):
    resp = None
    try:
        payload = [
            {
                "to": to,
                "msg": content,
                "at": at
            }
        ]

        try:
            response = requests.post(spl_callback_url, json=payload)
            resp = response.text
            response.raise_for_status()
        except Exception as e:
            tb = traceback.format_exc()
            # logger.error(f"send_wehbook error: {e} | {tb}")
            print(f"send_wehbook error: {e} | {tb}")
            # 飞书是最后一道防火墙，如果飞书也挂了，那就真的没办法了
            send_feishu_wehbook(feishu_webhook_url, f"🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘spl_new回调失败，请检查服务是否正常: {spl_callback_url} | {e} | {tb}")
            

    except Exception as e:
        tb = traceback.format_exc()
        # logger.error(f"send_sys_error error: {e} | {tb}")
        print(f"send_sys_error error: {e} | {tb}")
        # 飞书是最后一道防火墙，如果飞书也挂了，那就真的没办法了
        send_feishu_wehbook(feishu_webhook_url, f"🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘🆘spl_new系统错误 回调出错了，请检查代码传参: {spl_callback_url} | {e} | {tb}")

    # 返回响应
    return resp

# curl -X POST -H "Content-Type: application/json" \
#     -d '{"msg_type":"text","content":{"text":"request example"}}' \
#     https://open.feishu.cn/open-apis/bot/v2/hook/****

def send_feishu_wehbook(url: str, content, msg_type="text",
                        feishu_webhook_url=os.getenv("FEISHU_WEBHOOK_URL"),):
    # logger.info(f"send_wehbook url type: {type(url)} ")
    if not url:
        # logger.error(f"send_wehbook url is None")
        return None

    data = {
        "msg_type": msg_type,
        "content": content
    }
    if msg_type == "plain_text":
        data["msg_type"] = "text"
        data["content"] = {"text": content}

    # logger.info(f"send_wehbook url: {url}  data: {data}")
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except Exception as e:
        tb = traceback.format_exc()
        # logger.error(f"send_wehbook error: {e} | {tb}")
        return None
    # logger.info(f"send_wehbook response: {response.status}")

    
    # logger.info(f"send_wehbook resp: {resp_data}")

    return response.text

