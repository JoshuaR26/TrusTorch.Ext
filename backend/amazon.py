import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136'}

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [f"https://www.amazon.in/Apple-iPhone-Pro-Max-256/product-reviews/B0CHX1K2ZC/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber={i}" for i in range(1, 11)]
    l1 = []
    l2 = []
    new_data = {}

    async with aiohttp.ClientSession(headers=headers) as session:
        htmls = await asyncio.gather(*[fetch(session, url) for url in urls])
        for html in htmls:
            site = BeautifulSoup(html, features="lxml")

            # Parsing code
            review = site.findAll("div", {"class" : "a-row a-spacing-small review-data"})

            for i in range(len(review)):
                rev = str(review[i]).split("span>")[1].split("<")[0]
                l2.append(str(rev))
    print(l2)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())