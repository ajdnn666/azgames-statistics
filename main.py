"""
主程序
整合爬虫、数据管理和通知功能
"""

import sys
from datetime import datetime
from scraper import GameScraper
from data_manager import DataManager
from wechat_notifier import WeChatNotifier


def main():
    """主函数"""
    print("=" * 60)
    print(f"游戏点赞量监控系统")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 配置要监控的网页
    urls = [
        'https://azgames.io/new-games',
        # 后续可以添加更多网页
    ]
    
    # 初始化组件
    scraper = GameScraper(headless=True)
    data_manager = DataManager()
    notifier = WeChatNotifier()
    
    all_games = []
    
    try:
        # 1. 抓取所有网页的游戏数据
        print("\n步骤 1: 抓取游戏数据")
        print("-" * 60)
        
        for url in urls:
            print(f"\n正在抓取: {url}")
            games = scraper.scrape_games(url)
            all_games.extend(games)
            print(f"从 {url} 抓取到 {len(games)} 个游戏")
        
        print(f"\n总共抓取到 {len(all_games)} 个游戏")
        
        # 2. 保存当前数据
        print("\n步骤 2: 保存数据")
        print("-" * 60)
        data_manager.save_current_data(all_games)
        
        # 3. 计算增长量
        print("\n步骤 3: 计算增长量")
        print("-" * 60)
        
        daily_increases = data_manager.calculate_daily_increase(all_games)
        print(f"每日增长游戏数: {len(daily_increases)}")
        
        weekly_increases = data_manager.calculate_weekly_increase(all_games)
        print(f"每周增长游戏数: {len(weekly_increases)}")
        
        # 4. 发送通知
        print("\n步骤 4: 发送微信通知")
        print("-" * 60)
        
        # 获取TOP10
        daily_top10 = daily_increases[:10] if daily_increases else []
        weekly_top10 = weekly_increases[:10] if weekly_increases else []
        
        # 发送每日报告
        if daily_top10:
            print("\n发送每日报告...")
            success = notifier.send_daily_report(daily_top10)
            if success:
                print("✓ 每日报告发送成功")
            else:
                print("✗ 每日报告发送失败")
        else:
            print("没有每日增长数据，跳过每日报告")
        
        # 发送每周报告（仅在周一发送）
        if datetime.now().weekday() == 0:  # 0 = 周一
            if weekly_top10:
                print("\n发送每周报告...")
                success = notifier.send_weekly_report(weekly_top10)
                if success:
                    print("✓ 每周报告发送成功")
                else:
                    print("✗ 每周报告发送失败")
            else:
                print("没有每周增长数据，跳过每周报告")
        else:
            print("今天不是周一，跳过每周报告")
        
        print("\n" + "=" * 60)
        print("任务完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        # 清理资源
        scraper.close_driver()


if __name__ == '__main__':
    main()
