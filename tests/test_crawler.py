#!/usr/bin/env python3
"""
爬虫测试文件 - 测试解析功能
"""

import asyncio
import os
import sys

# 修正路径导入
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from main import PageParser, AsyncCrawler
except ImportError as e:
    print(f"导入错误: {e}")
    # 在Jupyter中运行时可能需要重新定义类
    print("在Jupyter环境中运行测试...")

def test_parse_quotes():
    """测试名言页面解析"""
    print("测试名言页面解析...")
    
    # 使用绝对路径确保能找到文件（现在fixtures在项目根目录）
    fixture_path = os.path.join(parent_dir, 'fixtures', 'quotes_page1.html')
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    parser = PageParser()
    quotes, next_url = parser.parse_quotes(html, 'http://test.com')
    
    # 验证解析结果
    assert len(quotes) == 1, f"应该解析出1条名言，实际得到: {len(quotes)}"
    assert quotes[0]['author'] == 'Alan Kay', f"作者应该是Alan Kay，实际是: {quotes[0]['author']}"
    assert 'future' in quotes[0]['tags'], f"应该包含future标签，实际标签: {quotes[0]['tags']}"
    assert 'invention' in quotes[0]['tags'], f"应该包含invention标签，实际标签: {quotes[0]['tags']}"
    assert next_url == 'http://test.com/page/2/', f"下一页URL应该是http://test.com/page/2/，实际是: {next_url}"
    
    # 验证名言文本
    expected_text = '"The best way to predict the future is to invent it."'
    assert quotes[0]['text'] == expected_text, f"名言文本不匹配，期望: {expected_text}，实际: {quotes[0]['text']}"
    
    print("✓ 名言解析测试通过")
    return quotes

def test_parse_books():
    """测试图书页面解析"""
    print("测试图书页面解析...")
    
    # 使用绝对路径确保能找到文件（现在fixtures在项目根目录）
    fixture_path = os.path.join(parent_dir, 'fixtures', 'books_page1.html')
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    parser = PageParser()
    books, next_url = parser.parse_books(html, 'http://test.com')
    
    # 验证解析结果
    assert len(books) == 1, f"应该解析出1本图书，实际得到: {len(books)}"
    assert books[0]['title'] == 'A Light in the Attic', f"书名应该是A Light in the Attic，实际是: {books[0]['title']}"
    assert books[0]['price'] == '£51.77', f"价格应该是£51.77，实际是: {books[0]['price']}"
    assert books[0]['stock'] == 'In stock', f"库存状态应该是In stock，实际是: {books[0]['stock']}"
    assert books[0]['rating'] == 'Three', f"评分应该是Three，实际是: {books[0]['rating']}"
    assert next_url == 'http://test.com/page-2.html', f"下一页URL应该是http://test.com/page-2.html，实际是: {next_url}"
    
    print("✓ 图书解析测试通过")
    return books

def test_parse_empty_html():
    """测试空HTML解析"""
    print("测试空HTML解析...")
    
    parser = PageParser()
    
    # 测试空HTML
    quotes, next_url = parser.parse_quotes('', 'http://test.com')
    assert len(quotes) == 0, "空HTML应该返回0条名言"
    assert next_url is None, "空HTML应该返回None下一页URL"
    
    books, next_url = parser.parse_books('', 'http://test.com')
    assert len(books) == 0, "空HTML应该返回0本图书"
    assert next_url is None, "空HTML应该返回None下一页URL"
    
    print("✓ 空HTML解析测试通过")

def test_parse_invalid_html():
    """测试无效HTML解析"""
    print("测试无效HTML解析...")
    
    parser = PageParser()
    
    # 测试无效HTML
    invalid_html = '<div>Invalid HTML content</div>'
    quotes, next_url = parser.parse_quotes(invalid_html, 'http://test.com')
    assert len(quotes) == 0, "无效HTML应该返回0条名言"
    assert next_url is None, "无效HTML应该返回None下一页URL"
    
    books, next_url = parser.parse_books(invalid_html, 'http://test.com')
    assert len(books) == 0, "无效HTML应该返回0本图书"
    assert next_url is None, "无效HTML应该返回None下一页URL"
    
    print("✓ 无效HTML解析测试通过")

def test_parse_html_with_missing_elements():
    """测试缺失元素的HTML解析"""
    print("测试缺失元素的HTML解析...")
    
    parser = PageParser()
    
    # 测试缺失重要元素的HTML
    partial_html = ('<div class="quote">'
                   '<span class="text">"Test quote"</span>'
                   '<!-- 故意缺少author元素 -->'
                   '</div>')
    
    quotes, next_url = parser.parse_quotes(partial_html, 'http://test.com')
    assert len(quotes) == 0, "缺失author元素应该返回0条名言"
    
    print("✓ 缺失元素解析测试通过")

async def test_crawler_initialization():
    """测试爬虫初始化"""
    print("测试爬虫初始化...")
    
    # 测试quotes爬虫初始化
    quotes_crawler = AsyncCrawler('quotes', concurrency=2, max_pages=5, delay=1.0)
    assert quotes_crawler.site == 'quotes'
    assert quotes_crawler.base_url == 'https://quotes.toscrape.com'
    assert quotes_crawler.concurrency == 2
    assert quotes_crawler.max_pages == 5
    assert quotes_crawler.delay == 1.0
    
    # 测试books爬虫初始化
    books_crawler = AsyncCrawler('books', concurrency=3, max_pages=10, delay=2.0)
    assert books_crawler.site == 'books'
    assert books_crawler.base_url == 'https://books.toscrape.com'
    assert books_crawler.concurrency == 3
    assert books_crawler.max_pages == 10
    assert books_crawler.delay == 2.0
    
    print("✓ 爬虫初始化测试通过")

def simple_test():
    """简化测试 - 用于在Notebook中直接运行"""
    print("运行简化测试...")
    try:
        test_parse_quotes()
        test_parse_books()
        print(" 基本解析测试通过")
        return True
    except Exception as e:
        print(f" 测试失败: {e}")
        return False

if __name__ == '__main__':
    print("开始运行爬虫测试...\n")
    
    try:
        test_parse_quotes()
        test_parse_books()
        test_parse_empty_html()
        test_parse_invalid_html()
        test_parse_html_with_missing_elements()
        asyncio.run(test_crawler_initialization())
        
        print("\n 所有测试通过!")
        
    except Exception as e:
        print(f"\n 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
