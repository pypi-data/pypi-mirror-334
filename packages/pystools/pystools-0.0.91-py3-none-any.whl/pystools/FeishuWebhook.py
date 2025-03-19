import os
import traceback

import requests
import urllib3
from pystools.Logger import Loggings

# HTTP_POOL = urllib3.PoolManager(num_pools=1000, cert_reqs='CERT_NONE')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# curl -X POST -H "Content-Type: application/json" \
#     -d '{"msg_type":"text","content":{"text":"request example"}}' \
#     https://open.feishu.cn/open-apis/bot/v2/hook/****

def send_webhook(content, msg_type="plain_text", url: str = os.getenv("APP_ERR_WEBHOOK"), logger=Loggings()):
    logger.info(f"send_wehbook url type: {type(url)} ")
    if not url:
        logger.error(f"send_wehbook url is None")
        return None

    data = {
        "msg_type": msg_type,
        "content": content
    }
    if msg_type == "plain_text":
        data["msg_type"] = "text"
        data["content"] = {"text": content}

    logger.info(f"send_wehbook url: {url}  data: {data}")
    try:
        response = requests.request('POST', url, json=data)
        if response.status_code != 200:
            logger.error(f"send_wehbook error: {response.status_code} | {response.text}")
            return False, response
        return True, response
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"send_wehbook error: {e} | {tb}")
        return False, e

