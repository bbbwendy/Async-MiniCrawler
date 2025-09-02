#!/usr/bin/env python3
"""
Async MiniCrawler 命令行接口
"""

import asyncio
import argparse
from main import run_crawler

async def main():
    parser = argparse.ArgumentParser(description='Async MiniCrawler - 异步网页爬虫')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # run 命令
    run_parser = subparsers.add_parser('run', help='运行爬虫')
    run_parser.add_argument('--site', type=str, choices=['quotes', 'books'], 
                          default='quotes', help='要爬取的站点 (quotes 或 books)')
    run_parser.add_argument('--concurrency', type=int, default=5, 
                          help='并发数 (默认: 5)')
    run_parser.add_argument('--max-pages', type=int, default=50, 
                          help='最大页面数 (默认: 50)')
    run_parser.add_argument('--delay', type=float, default=1.0, 
                          help='请求延迟 (默认: 1.0秒)')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        print(f"开始爬取 {args.site} 站点")
        print(f"配置: 并发数={args.concurrency}, 最大页面={args.max_pages}, 延迟={args.delay}s")
        
        data, stats = await run_crawler(
            site=args.site,
            concurrency=args.concurrency,
            max_pages=args.max_pages,
            delay=args.delay
        )
        
        print(f"爬虫完成! 共收集 {len(data)} 条数据")
        print(f"统计信息: {stats['successful_pages']} 成功, {stats['failed_pages']} 失败")
        
    else:
        parser.print_help()

if __name__ == '__main__':
    asyncio.run(main())
