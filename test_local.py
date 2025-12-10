"""
本地测试脚本
测试爬虫功能，不发送微信通知
"""

import json
from datetime import datetime
from scraper import GameScraper


def test_scraper():
    """测试爬虫功能"""
    print("=" * 60)
    print("游戏点赞量监控系统 - 本地测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 初始化爬虫（非无头模式，可以看到浏览器）
    print("\n初始化爬虫...")
    scraper = GameScraper(headless=False)
    
    try:
        # 测试URL
        test_url = 'https://azgames.io/new-games'
        
        print(f"\n开始抓取: {test_url}")
        print("提示: 浏览器窗口会自动打开，请稍等...")
        print("-" * 60)
        
        # 抓取游戏数据
        games = scraper.scrape_games(test_url)
        
        print("\n" + "=" * 60)
        print(f"✓ 抓取完成！共获取 {len(games)} 个游戏")
        print("=" * 60)
        
        # 显示前10个游戏
        if games:
            print("\n前10个游戏预览:")
            print("-" * 60)
            for i, game in enumerate(games[:10], 1):
                print(f"{i}. {game['name']}")
                print(f"   URL: {game['url']}")
                print(f"   点赞数: {game['likes']}")
                print()
        
        # 保存到测试文件
        output_file = 'test_games_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(games, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 完整数据已保存到: {output_file}")
        
        # 统计信息
        total_likes = sum(game['likes'] for game in games)
        avg_likes = total_likes / len(games) if games else 0
        
        print("\n统计信息:")
        print("-" * 60)
        print(f"游戏总数: {len(games)}")
        print(f"总点赞数: {total_likes}")
        print(f"平均点赞数: {avg_likes:.2f}")
        
        # 找出点赞最多的游戏
        if games:
            top_game = max(games, key=lambda x: x['likes'])
            print(f"\n点赞最多的游戏:")
            print(f"  名称: {top_game['name']}")
            print(f"  点赞数: {top_game['likes']}")
        
        print("\n" + "=" * 60)
        print("测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n关闭浏览器...")
        scraper.close_driver()
        print("✓ 浏览器已关闭")


if __name__ == '__main__':
    test_scraper()
