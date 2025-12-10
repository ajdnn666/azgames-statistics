"""
数据管理模块
负责数据的存储、读取和对比分析
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path


class DataManager:
    def __init__(self, data_dir='data'):
        """初始化数据管理器"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.history_file = self.data_dir / 'history.json'
        self.daily_file = self.data_dir / 'daily_stats.json'
        self.weekly_file = self.data_dir / 'weekly_stats.json'
        
    def save_current_data(self, games_data):
        """
        保存当前抓取的数据
        
        Args:
            games_data: 游戏数据列表
        """
        timestamp = datetime.now().isoformat()
        
        # 读取历史数据
        history = self._load_history()
        
        # 添加新数据
        history.append({
            'timestamp': timestamp,
            'games': games_data
        })
        
        # 只保留最近30天的数据
        cutoff_date = datetime.now() - timedelta(days=30)
        history = [
            entry for entry in history
            if datetime.fromisoformat(entry['timestamp']) > cutoff_date
        ]
        
        # 保存
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
            
        print(f"数据已保存，历史记录数: {len(history)}")
        
    def _load_history(self):
        """加载历史数据"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def calculate_daily_increase(self, current_games):
        """
        计算每日增长量
        
        Args:
            current_games: 当前游戏数据
            
        Returns:
            list: 包含增长数据的游戏列表
        """
        history = self._load_history()
        
        if len(history) < 2:
            print("历史数据不足，无法计算每日增长")
            return []
        
        # 获取上一次的数据（倒数第二条）
        previous_data = history[-2]['games']
        
        # 创建游戏URL到点赞数的映射
        previous_likes = {game['url']: game['likes'] for game in previous_data}
        
        # 计算增长
        increases = []
        for game in current_games:
            url = game['url']
            current_likes = game['likes']
            previous = previous_likes.get(url, 0)
            
            increase = current_likes - previous
            if increase > 0:  # 只记录有增长的
                increases.append({
                    'name': game['name'],
                    'url': url,
                    'current_likes': current_likes,
                    'previous_likes': previous,
                    'increase': increase
                })
        
        # 按增长量排序
        increases.sort(key=lambda x: x['increase'], reverse=True)
        
        # 保存每日统计
        self._save_daily_stats(increases)
        
        return increases
    
    def calculate_weekly_increase(self, current_games):
        """
        计算每周增长量
        
        Args:
            current_games: 当前游戏数据
            
        Returns:
            list: 包含增长数据的游戏列表
        """
        history = self._load_history()
        
        if not history:
            print("历史数据不足，无法计算每周增长")
            return []
        
        # 获取7天前的数据
        week_ago = datetime.now() - timedelta(days=7)
        week_ago_data = None
        
        for entry in history:
            entry_time = datetime.fromisoformat(entry['timestamp'])
            if entry_time <= week_ago:
                week_ago_data = entry['games']
            else:
                break
        
        if not week_ago_data:
            print("没有找到7天前的数据")
            return []
        
        # 创建游戏URL到点赞数的映射
        week_ago_likes = {game['url']: game['likes'] for game in week_ago_data}
        
        # 计算增长
        increases = []
        for game in current_games:
            url = game['url']
            current_likes = game['likes']
            previous = week_ago_likes.get(url, 0)
            
            increase = current_likes - previous
            if increase > 0:
                increases.append({
                    'name': game['name'],
                    'url': url,
                    'current_likes': current_likes,
                    'previous_likes': previous,
                    'increase': increase
                })
        
        # 按增长量排序
        increases.sort(key=lambda x: x['increase'], reverse=True)
        
        # 保存每周统计
        self._save_weekly_stats(increases)
        
        return increases
    
    def _save_daily_stats(self, increases):
        """保存每日统计数据"""
        stats = {
            'timestamp': datetime.now().isoformat(),
            'top_10': increases[:10]
        }
        
        with open(self.daily_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    
    def _save_weekly_stats(self, increases):
        """保存每周统计数据"""
        stats = {
            'timestamp': datetime.now().isoformat(),
            'top_10': increases[:10]
        }
        
        with open(self.weekly_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    
    def get_top_games(self, period='daily', limit=10):
        """
        获取排名前N的游戏
        
        Args:
            period: 'daily' 或 'weekly'
            limit: 返回的数量
            
        Returns:
            list: 排名前N的游戏
        """
        file_path = self.daily_file if period == 'daily' else self.weekly_file
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            stats = json.load(f)
            
        return stats.get('top_10', [])[:limit]


if __name__ == '__main__':
    # 测试数据管理器
    manager = DataManager()
    
    # 测试数据
    test_games = [
        {'name': 'Game 1', 'url': 'https://example.com/game1', 'likes': 100},
        {'name': 'Game 2', 'url': 'https://example.com/game2', 'likes': 200},
    ]
    
    manager.save_current_data(test_games)
    print("测试数据已保存")
