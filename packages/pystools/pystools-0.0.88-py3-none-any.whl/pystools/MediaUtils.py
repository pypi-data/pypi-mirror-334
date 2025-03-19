import requests
from io import BytesIO

from pydub import AudioSegment


def get_audio_duration(audio_file_url):
    # 使用requests获取在线音频文件内容
    response = requests.get(audio_file_url)

    # 将内容加载为BytesIO对象，方便pydub读取
    audio_file = BytesIO(response.content)

    return get_audio_duration_by_file(audio_file)


def get_audio_duration_by_file(audio_file):
    # 使用pydub的AudioSegment加载音频
    audio = AudioSegment.from_file(audio_file)

    # 获取音频时长（单位为毫秒），转换为秒
    duration_in_seconds = audio.duration_seconds

    # 打印音频时长
    # print(f"音频时长为: {duration_in_seconds} 秒")

    return duration_in_seconds


import re


def estimate_duration_from_text(text):
    language_speeds = {
        'en': 175,  # 英语速度（词/分钟）
        'zh': 150,  # 中文速度（字/分钟）
        # 其他语言可以在这里添加
    }

    # 按语言估算时长
    total_duration = 0
    words = re.findall(r'[\u4e00-\u9fa5]|[a-zA-Z]+', text)

    for word in words:
        if re.match(r'[\u4e00-\u9fa5]', word):  # 中文字符
            total_duration += 60 / language_speeds['zh']  # 中文按字计算
        else:
            total_duration += 60 / language_speeds['en']  # 英文按词计算

    return total_duration

# import pyttsx3
# import time
#
# def text_to_audio_duration(text, lang='zh'):
#     start_time = time.time()
#     tts = gTTS(text=text, lang=lang)
#     tts.save("temp_audio.mp3")
#     os.system("start temp_audio.mp3")  # 在 Windows 上播放音频
#     duration_seconds = time.time() - start_time
#     return duration_seconds
#
#
# # 示例文本
# mixed_text = ("Hello, 你好, how are you?我不敢苟同。"
#               "我个人认为这个意大利面就应该拌42号混凝土。"
#               "因为这个螺丝钉的长度，它很容易会直接影响到挖掘机的扭距，"
#               "你往里砸的时候，一瞬间它就会产生大量的高能蛋白，俗称UFO。"
#               "会严重影响经济的发展。"
#               "照你这么说，炸鸡块要用92#汽油，毕竟我们无法用光学透镜探测苏格拉底，"
#               "如果二氧化氢持续侵蚀这个机床组件，那么我们早晚要在斐波那契曲线上安装一个胶原蛋白，"
#               "否则我们将无法改变蜜雪冰城与阿尔别克的叠加状态，"
#               "因为众所周知爱吃鸡摩人在捕鲲的时候往往需要用氢的同位素当做诱饵，"
#               "但是原子弹的新鲜程度又会直接影响到我国东南部的季风和洋流，"
#               "所以说在西伯利亚地区开设农学院显然是不合理的。"
#               "我知道你一定会反驳我，告诉我农业的底层思维是什么，"
#               "就是不用化肥农药和种子，还包括生命之源氮气，"
#               "使甲烷分子直接转化成能够捕获放射性元素释放的β射线的单质，"
#               "并且使伽马射线在常温下就能用老虎钳折弯成78°，"
#               "否则在用望远镜观察细胞结构时，根本发现不了时空重叠时到底要叠几层才能使潼关肉夹馍更酥脆的原因。")
#
# text = "我个人认为这个意大利面就应该拌42号混凝土。" \
#        "因为这个螺丝钉的长度，它很容易会直接影响到挖掘机的扭距，" \
#        "你往里砸的时候，一瞬间它就会产生大量的高能蛋白，俗称UFO。" \
#        "会严重影响经济的发展。" \
#        "I'm afraid I can't agree. Personally, I believe this pasta should be mixed with No. 42 concrete. Due to the length of this screw, it can easily affect the torque of the excavator. When you hammer it in, it can instantaneously generate a large amount of high-energy protein, commonly referred to as UFOs, which would severely impact economic development. According to your logic, chicken nuggets should be cooked with 92# gasoline, since we can't detect Socrates with optical lenses. If hydrogen peroxide continues to erode this machine component, we'll eventually need to install collagen on the Fibonacci curve. Otherwise, we won't be able to change the superposition of Honey Snow Ice City and Albei Ke. As we know, those who love chicken often need isotopes of hydrogen as bait when catching giant fish, but the freshness of atomic bombs directly affects the monsoons and ocean currents in our southeastern region. Therefore, establishing an agricultural college in Siberia is clearly unreasonable. I know you'll likely counter my points, telling me that the foundational thinking of agriculture involves not using fertilizers, pesticides, or seeds, and also includes nitrogen, the source of life. It enables methane molecules to be directly transformed into elements that capture beta rays released by radioactive elements, allowing gamma rays to be bent at 78° with pliers at room temperature. Otherwise, when observing cell structures with a telescope, we wouldn't be able to determine how many layers need to overlap in spacetime for a Tongguan meat sandwich to become crispier."
# estimated_duration = estimate_duration_from_text(text)
#
# print(f"Estimated Duration: {estimated_duration:.2f} seconds")
#
# actual_duration = text_to_audio_duration(text)
# print(f"Actual Duration: {actual_duration:.2f} seconds")
