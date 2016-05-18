#!/usr/bin/env python

# python 3.5 async web crawler.


import aiohttp
import asyncio
import sys
from urllib.parse import urljoin, urldefrag

root_url = sys.argv[1]
crawled_urls, url_hub = [], [root_url, "%s/sitemap.xml" % (root_url), "%s/robots.txt" % (root_url)]

async def get_body(url):
    response = await aiohttp.request('GET', url)
    return await response.read()

async def handle_task(task_id, work_queue):
    while not work_queue.empty():
        queue_url = await work_queue.get()
        crawled_urls.append(queue_url)
        body = await get_body(queue_url)
        for new_url in get_urls(body):
            if root_url in new_url and not new_url in crawled_urls:
                q.put_nowait(new_url)
        print(queue_url)
        #await asyncio.sleep(5)

def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url

def get_urls(html):
    new_urls = set([url.split('"')[0] for url in str(html).replace("'",'"').split('href="')[1:]])
    return [urljoin(root_url, remove_fragment(new_url)) for new_url in new_urls]

if __name__ == "__main__":
    q = asyncio.Queue()
    [q.put_nowait(url) for url in url_hub]    
    loop = asyncio.get_event_loop()
    tasks = [handle_task(task_id, q) for task_id in range(10)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()