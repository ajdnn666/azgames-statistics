"""
游戏点赞量爬虫模块
负责从网页抓取游戏数据和点赞量
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class GameScraper:
    def __init__(self, headless=True):
        """初始化爬虫"""
        self.headless = headless
        self.driver = None
        
    def setup_driver(self):
        """配置Chrome浏览器"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            # 尝试使用webdriver-manager自动管理驱动
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.core.os_manager import ChromeType
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()),
                options=chrome_options
            )
        except Exception as e:
            print(f"使用webdriver-manager失败: {e}")
            print("尝试使用系统Chrome...")
            # 如果失败，尝试直接使用系统Chrome
            self.driver = webdriver.Chrome(options=chrome_options)
        
    def close_driver(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            
    def scrape_games(self, url):
        """
        抓取指定URL的游戏数据
        
        Args:
            url: 游戏列表页面URL
            
        Returns:
            list: 游戏数据列表，每个游戏包含名称、链接、点赞量等信息
        """
        if not self.driver:
            self.setup_driver()
            
        print(f"正在访问: {url}")
        self.driver.get(url)
        
        # 等待页面加载
        print("等待页面初始加载...")
        time.sleep(5)  # 增加初始等待时间
        
        # 滚动页面以加载所有内容
        self._scroll_page()
        
        games = []
        
        try:
            # 尝试多种选择器来查找游戏链接
            selectors = [
                'a[href*="azgames.io/"]',  # 包含azgames.io的链接
                'a.game-link',  # 游戏链接类
                'a.game-card',  # 游戏卡片类
                'div.game a',  # 游戏div内的链接
            ]
            
            game_elements = []
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        game_elements.extend(elements)
                except:
                    continue
            
            # 如果上面的选择器都没找到，使用通用选择器
            if not game_elements:
                game_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a[href]')
            
            print(f"找到 {len(game_elements)} 个链接元素")
            
            for element in game_elements:
                try:
                    href = element.get_attribute('href')
                    
                    # 过滤出游戏页面链接
                    if not href or 'azgames.io' not in href:
                        continue
                    
                    # 排除非游戏页面
                    exclude_patterns = [
                        '/category/', '/about-us', '/contact', '/privacy', 
                        '/term-of-use', '/copyright', '/new-games',
                        'javascript:', '#', '/tag/'
                    ]
                    if any(pattern in href for pattern in exclude_patterns):
                        continue
                    
                    # 确保是游戏页面（通常格式是 azgames.io/game-name）
                    parts = href.replace('https://', '').replace('http://', '').split('/')
                    if len(parts) < 2 or not parts[1]:
                        continue
                    
                    # 从URL中提取游戏名作为后备
                    url_game_name = parts[1].replace('-', ' ').title()
                        
                    game_name = element.text.strip()
                    
                    # 移除标签
                    for tag in ['New', 'Trending', 'Hot', 'Popular']:
                        game_name = game_name.replace(tag, '').strip()
                    
                    # 如果移除标签后名字为空，使用URL中的名字
                    if not game_name or len(game_name) < 2:
                        game_name = url_game_name
                    
                    # 最终检查
                    if not game_name or len(game_name) < 2:
                        continue
                    
                    if href not in [g['url'] for g in games]:
                        game_data = {
                            'name': game_name,
                            'url': href,
                            'likes': 0,  # 默认值，后续会更新
                            'scraped_at': datetime.now().isoformat()
                        }
                        games.append(game_data)
                        
                except Exception as e:
                    continue
            
            # 去重
            unique_games = []
            seen_urls = set()
            for game in games:
                if game['url'] not in seen_urls:
                    seen_urls.add(game['url'])
                    unique_games.append(game)
            
            print(f"找到 {len(unique_games)} 个游戏")
            
            # 获取每个游戏的点赞量
            for i, game in enumerate(unique_games):
                print(f"正在获取游戏 {i+1}/{len(unique_games)}: {game['name']}")
                likes = self._get_game_likes(game['url'])
                game['likes'] = likes
                time.sleep(1)  # 避免请求过快
                
        except Exception as e:
            print(f"抓取游戏列表时出错: {e}")
            
        return unique_games
    
    def _get_game_likes(self, game_url):
        """
        获取单个游戏的点赞量
        
        Args:
            game_url: 游戏页面URL
            
        Returns:
            int: 点赞数量
        """
        try:
            self.driver.get(game_url)
            time.sleep(2)
            
            # 尝试多种可能的选择器来查找点赞数
            selectors = [
                'button[class*="like"]',
                'button[class*="thumb"]',
                'div[class*="like"]',
                'span[class*="like"]',
                '.likes-count',
                '.like-count',
                '[data-likes]',
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        # 尝试从文本中提取数字
                        if text and any(char.isdigit() for char in text):
                            # 提取数字
                            import re
                            numbers = re.findall(r'\d+', text)
                            if numbers:
                                return int(numbers[0])
                except:
                    continue
            
            # 如果找不到点赞数，返回0
            return 0
            
        except Exception as e:
            print(f"获取点赞量失败 ({game_url}): {e}")
            return 0
    
    def _scroll_page(self):
        """滚动页面以加载所有内容"""
        print("开始滚动页面加载所有游戏...")
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_count = 0
        max_scrolls = 10  # 最多滚动10次
        
        for i in range(max_scrolls):
            # 滚动到底部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            scroll_count += 1
            print(f"第 {scroll_count} 次滚动...")
            time.sleep(3)  # 增加等待时间
            
            # 检查页面高度是否变化
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(f"页面高度不再变化，停止滚动")
                break
            last_height = new_height
        
        print(f"滚动完成，共滚动 {scroll_count} 次")
        time.sleep(2)  # 最后再等待一下


if __name__ == '__main__':
    # 测试爬虫
    scraper = GameScraper(headless=False)
    try:
        games = scraper.scrape_games('https://azgames.io/new-games')
        print(f"\n总共抓取到 {len(games)} 个游戏")
        
        # 保存到文件
        with open('test_games.json', 'w', encoding='utf-8') as f:
            json.dump(games, f, ensure_ascii=False, indent=2)
        print("数据已保存到 test_games.json")
        
    finally:
        scraper.close_driver()
