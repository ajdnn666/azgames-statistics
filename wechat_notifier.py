"""
微信通知模块
通过企业微信机器人发送消息
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv


class WeChatNotifier:
    def __init__(self):
        """初始化微信通知器"""
        load_dotenv()
        self.webhook_url = os.getenv('WECHAT_WEBHOOK_URL')
        
        if not self.webhook_url:
            print("警告: 未配置WECHAT_WEBHOOK_URL环境变量")
    
    def send_message(self, content):
        """
        发送文本消息
        
        Args:
            content: 消息内容
            
        Returns:
            bool: 是否发送成功
        """
        if not self.webhook_url:
            print("无法发送消息: 未配置Webhook URL")
            return False
        
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        
        try:
            response = requests.post(self.webhook_url, json=data)
            result = response.json()
            
            if result.get('errcode') == 0:
                print("消息发送成功")
                return True
            else:
                print(f"消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"发送消息时出错: {e}")
            return False
    
    def send_markdown(self, content):
        """
        发送Markdown格式消息
        
        Args:
            content: Markdown内容
            
        Returns:
            bool: 是否发送成功
        """
        if not self.webhook_url:
            print("无法发送消息: 未配置Webhook URL")
            return False
        
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        
        try:
            response = requests.post(self.webhook_url, json=data)
            result = response.json()
            
            if result.get('errcode') == 0:
                print("消息发送成功")
                return True
            else:
                print(f"消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"发送消息时出错: {e}")
            return False
    
    def format_daily_report(self, top_games):
        """
        格式化每日报告
        
        Args:
            top_games: 排名前10的游戏列表
            
        Returns:
            str: 格式化的报告内容
        """
        if not top_games:
            return "📊 今日游戏点赞增长报告\n\n暂无数据"
        
        report = f"📊 **游戏点赞增长日报**\n"
        report += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        report += "### 🏆 每日增长TOP10\n\n"
        
        for i, game in enumerate(top_games, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            report += f"{medal} **{game['name']}**\n"
            report += f"   ├ 当前点赞: {game['current_likes']}\n"
            report += f"   ├ 昨日点赞: {game['previous_likes']}\n"
            report += f"   └ 增长: <font color=\"info\">+{game['increase']}</font>\n\n"
        
        return report
    
    def format_weekly_report(self, top_games):
        """
        格式化每周报告
        
        Args:
            top_games: 排名前10的游戏列表
            
        Returns:
            str: 格式化的报告内容
        """
        if not top_games:
            return "📊 本周游戏点赞增长报告\n\n暂无数据"
        
        report = f"📊 **游戏点赞增长周报**\n"
        report += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        report += "### 🏆 每周增长TOP10\n\n"
        
        for i, game in enumerate(top_games, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            report += f"{medal} **{game['name']}**\n"
            report += f"   ├ 当前点赞: {game['current_likes']}\n"
            report += f"   ├ 7天前点赞: {game['previous_likes']}\n"
            report += f"   └ 增长: <font color=\"warning\">+{game['increase']}</font>\n\n"
        
        return report
    
    def send_daily_report(self, top_games):
        """发送每日报告"""
        content = self.format_daily_report(top_games)
        return self.send_markdown(content)
    
    def send_weekly_report(self, top_games):
        """发送每周报告"""
        content = self.format_weekly_report(top_games)
        return self.send_markdown(content)


if __name__ == '__main__':
    # 测试通知器
    notifier = WeChatNotifier()
    
    # 测试数据
    test_games = [
        {
            'name': '测试游戏1',
            'url': 'https://example.com/game1',
            'current_likes': 150,
            'previous_likes': 100,
            'increase': 50
        },
        {
            'name': '测试游戏2',
            'url': 'https://example.com/game2',
            'current_likes': 250,
            'previous_likes': 200,
            'increase': 50
        }
    ]
    
    print("测试每日报告:")
    print(notifier.format_daily_report(test_games))
