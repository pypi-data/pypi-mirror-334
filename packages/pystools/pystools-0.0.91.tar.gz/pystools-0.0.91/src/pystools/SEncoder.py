import hashlib
import random
import time
import uuid
from typing import Any

import shortuuid


class SEncoder:
    @staticmethod
    def md5_from_uuid(to_upper=False):
        # 生成唯一的uuid
        v = str(uuid.uuid1())
        m = hashlib.md5()
        # 将args中的所有值拼接起来
        m.update(f"{v}".encode("utf-8"))
        if to_upper:
            return m.hexdigest().upper()
        return m.hexdigest()

    @staticmethod
    def short_uuid(to_upper=False):
        unique_id = shortuuid.uuid()
        if to_upper:
            return unique_id.upper()
        return unique_id

    @staticmethod
    def gen_md5(*args, to_upper=False):
        m = hashlib.md5()
        # 将args中的所有值拼接起来
        for arg in args:
            m.update(f"{arg}".encode("utf-8"))
        if to_upper:
            return m.hexdigest().upper()
        return m.hexdigest()

    @staticmethod
    def gen_num_str_by_timestamp(length=8):
        sleep_time = random.random() * 0.8
        print("sleep time: ", sleep_time)
        time.sleep(sleep_time)
        t = time.time()
        tm = t * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000
        # 显示完整的数字，不用科学计数法
        tstr = "{:.0f}".format(tm)
        # print(tstr)
        nameStr = tstr[13:-1]

        def split_string(string, cnt=4):
            length = len(string)
            segment_length = length // cnt
            segments = []
            for i in range(cnt):
                start = i * segment_length
                end = (i + 1) * segment_length
                segment = string[start:end]
                segments.append(segment)
            return segments

        segments = split_string(nameStr, length)
        # print(segments)

        lid = ""
        for segment in segments:
            # 从 segment 中随机取一个字符
            char = random.choice(segment)
            # 把字符添加到 lid 中
            lid += char
        return lid

    @staticmethod
    def encode_sign(param_dict: Any, nonce: str):
        # 将param_dict中的key按照字母排序，如果只处理第一层的key，然后拼接成字符串 例如：a=1&b=2&c=3
        param_str = ""
        if isinstance(param_dict, dict):
            for key in sorted(param_dict.keys()):
                value = param_dict[key]
                value_str = value
                if not isinstance(value, str):
                    value_str = str(value)
                    if value_str == "None":
                        value_str = "null"
                param_str += f"{key}={value_str}&"
            param_str = param_str[:-1]
        # 然后将param_gen_sign.nonce拼接到字符串后面
        param_str += str(nonce)
        # 然后对字符串进行sha256加密
        import hashlib
        m = hashlib.sha256()
        m.update(param_str.encode("utf-8"))
        sign = m.hexdigest()
        return {"sign": sign, "param_str": param_str}
    
from hashlib import md5
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import os

def encrypt_json(json_data, key: str):
    key = md5(key.encode('utf-8')).digest()
    json_str = "{}"
    if isinstance(json_data, str):
        json_str = json_data
    elif isinstance(json_data, dict):
        json_str = json.dumps(json_data, ensure_ascii=False)
    else:
        raise ValueError("json_data 必须是字符串或字典")

    # 生成加密器（使用CBC模式）
    iv = b'1234567812345678'  # 初始化向量(长度需16字节)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 加密并填充数据
    encrypted_data = cipher.encrypt(pad(json_str.encode('utf-8'), AES.block_size))

    # 转换为Base64字符串
    return base64.b64encode(encrypted_data).decode('utf-8')


from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64


def decrypt_json(encrypted_str: str, key: str):
    key = md5(key.encode('utf-8')).digest()
    # Base64解码
    encrypted_data = base64.b64decode(encrypted_str)

    # 生成解密器
    iv = b'1234567812345678'  # 需与加密时的IV一致
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 解密并去除填充
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    return decrypted_data.decode('utf-8')


from datetime import datetime
from urllib.parse import urlparse
import os

def get_filename_from_url(url,sub_fix=None  ):
    # 解析URL获取路径部分
    parsed = urlparse(url)
    # 分割路径并获取最后一段
    path = parsed.path
    if not path:
        return ""
    
    res = os.path.basename(path)
    

    if sub_fix:
        return res.split(".")[0] + sub_fix + "." + res.split(".")[1]
    else:
        return res

# 获取当前时间
def get_current_time(format_str="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(format_str)