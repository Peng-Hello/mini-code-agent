"""
Web interaction tools for mini-code-agent.
"""

import asyncio
from typing import List


async def fetch_website_html(url: str, wait: int = 3) -> str:
    """
    使用 Playwright 抓取指定url动态渲染后的网页内容

    :param url: 目标 URL
    :param wait: 页面加载后等待的秒数（等待 JS 渲染）
    :return: 渲染完成后的 HTML
    """
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # True=无头模式
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")  # 等待页面加载完成
        await asyncio.sleep(wait)  # 额外等几秒给JS渲染
        html = await page.content()
        await browser.close()
        return html


async def use_search_engine(question: str, engine: str = "bing") -> List[dict]:
    """
    使用 Playwright 打开搜索引擎并解析搜索结果
    当前支持: Bing (https://cn.bing.com)

    :param question: 搜索关键词
    :param engine: 搜索引擎 ('bing')
    :return: [{'title': str, 'url': str, 'desc': str}, ...]
    """
    from playwright.async_api import async_playwright
    from bs4 import BeautifulSoup

    if engine != "bing":
        raise ValueError("目前仅支持 Bing 搜索")

    search_url = f"https://cn.bing.com/search?q={question}"
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        page.set_default_timeout(30000)

        await page.goto(search_url, wait_until="networkidle")
        await page.wait_for_timeout(1500)  # 等待渲染完成

        html = await page.content()
        await browser.close()

        # 用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, "html.parser")
        for li in soup.select("li.b_algo"):
            # 标题
            title_tag = li.select_one("h2 a")
            title = title_tag.get_text(strip=True) if title_tag else ""
            # URL
            url = (
                title_tag.get("href")
                if title_tag and title_tag.has_attr("href")
                else ""
            )
            # 描述
            desc_tag = li.select_one("p")
            desc = desc_tag.get_text(strip=True) if desc_tag else ""
            if title and url:
                results.append({"title": title, "url": url, "desc": desc})
    return results
