import requests
import os
import urllib3

import config

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置信息
BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
CHAT_ID = config.TELEGRAM_CHAT_ID

class TelegramNotifier:
    def __init__(self, token=BOT_TOKEN, chat_id=CHAT_ID):
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.chat_id = chat_id

    def send_message(self, text):
        """发送文本消息"""
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": text
        }
        try:
            # verify=False 防止 Mac 上 SSL 证书报错
            response = requests.post(url, json=data, verify=False)
            if response.status_code == 200:
                print("✅ Telegram 消息发送成功")
                return True
            else:
                print(f"❌ 发送失败: {response.text}")
                return False
        except Exception as e:
            print(f"💥 发送异常: {e}")
            return False

    def send_photo(self, photo_path, caption=None):
        """发送图片"""
        if not os.path.exists(photo_path):
            print(f"❌ 图片不存在: {photo_path}")
            return False
            
        url = f"{self.base_url}/sendPhoto"
        data = {"chat_id": self.chat_id}
        if caption:
            data["caption"] = caption
            
        try:
            with open(photo_path, "rb") as photo:
                files = {"photo": photo}
                # verify=False 防止 Mac 上 SSL 证书报错
                response = requests.post(url, data=data, files=files, verify=False)
                
            if response.status_code == 200:
                print("✅ Telegram 图片发送成功")
                return True
            else:
                print(f"❌ 图片发送失败: {response.text}")
                return False
        except Exception as e:
            print(f"💥 图片发送异常: {e}")
            return False

if __name__ == "__main__":
    # 测试代码
    bot = TelegramNotifier()
    bot.send_message("Solar Assistant Online")
    
    # 如果有图表，试着发一下
    chart_file = "solar_data_chart.png"
    if os.path.exists(chart_file):
        bot.send_photo(chart_file, caption="📊 最新的发电数据图表")
