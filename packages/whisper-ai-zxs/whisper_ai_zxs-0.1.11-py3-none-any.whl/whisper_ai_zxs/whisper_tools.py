from .whisper_db import WhisperDB
from datetime import datetime
import requests
from PIL import ImageGrab
import base64
import hashlib
#from xbot import print

class WhisperTools_ChatList:
    def __init__(self, name, before_time):
        """ 初始化一个空字典用于存储函数 """
        self._chat_list = []
        self._chat_name = name
        self._before_chat_time = before_time

    def add(self, chat_list):
        for item in chat_list:
            if (self._chat_name != item["name"]):
                if (self._before_chat_time == ""):
                    return False
                else:
                    return True
            if (item["time"] == self._before_chat_time):
                return False
            self._chat_list.append(item)
        return True

    def get(self):
        return self._chat_list
    

class WhisperTools_ChatRecord:
    @staticmethod
    def record_user_chat(kf_name, user_name, content):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_query = """
            INSERT INTO openai_chat_list (chat_time, shop_name, chat_name, sender, act, content)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        with WhisperDB() as myDB:
            myDB.query(insert_query, (current_time, kf_name, user_name, user_name, "ask", content))
            myDB.commit()
    @staticmethod
    def record_chatGPT_action(kf_name, user_name, act, content):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_query = """
            INSERT INTO openai_chat_list (chat_time, shop_name, chat_name, sender, act, content)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        with WhisperDB() as myDB:
            myDB.query(insert_query, (current_time, kf_name, user_name, "chatGPT", act, content))
            myDB.commit()

class WhisperTools_Qywx:
    @staticmethod
    def send_to_error_robot(msg):
        # 截取整个屏幕
        screenshot = ImageGrab.grab()
        screenshot_path = r"D:\WhisperAgent\异常截图\screenshot.png"  # 确保路径存在
        screenshot.save(screenshot_path)

        # 读取图片内容
        with open(screenshot_path, "rb") as f:
            image_data = f.read()

        # 计算 Base64 编码和 MD5 值
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        image_md5 = hashlib.md5(image_data).hexdigest()

        # 企业微信 Webhook URL
        webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f2113e16-d190-42b8-a386-6032ae7def7f'

        # 发送文本消息
        text_data = {
            "msgtype": "text",
            "text": {"content": msg}
        }
        text_response = requests.post(webhook_url, json=text_data)

        # 发送图片消息
        image_data = {
            "msgtype": "image",
            "image": {
                "base64": image_base64,
                "md5": image_md5
            }
        }
        image_response = requests.post(webhook_url, json=image_data)

        return {
            "text_response": text_response.json(),
            "image_response": image_response.json()
        }
    @staticmethod
    def send_to_kf_robot(agent, msg):
        webhook_url = WhisperTools_Qywx.get_robot_hook(agent)
        #print("robot hook:",webhook_url)
        if (webhook_url != ""):
            data = {
                'msgtype': 'text',
                'text': {'content': msg}
            }
            response = requests.post(webhook_url, json=data)
            return response.text
        else:
            return "webhook_url is blank!"
    @staticmethod
    def get_robot_hook(agent):
        # 使用 with 语句管理数据库连接
        with WhisperDB() as db:  # 自动管理连接
            # 使用参数化查询来防止 SQL 注入
            query = """
                SELECT robot_hook
                FROM openai_kf_manage
                JOIN openai_company ON openai_kf_manage.company = openai_company.name
                WHERE shop_name = %s;
            """
            # 获取查询结果
            result = db.query(query, (agent.get_kf_name(),))

        # 如果查询结果存在，则返回第一行
        return result[0][0] if result else ""
