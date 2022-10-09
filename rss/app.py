import time
import aiohttp
import json
import asyncio
from config import URLS
from mongo_db import work_with_rss
import traceback
from rabbit import RABBIT

f = open('rbk.csv', 'w',encoding= "utf-8")
r = RABBIT()
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_rss(url):

    async with aiohttp.ClientSession() as session:
        try:
            resp = await fetch(session, url)
            new_news = work_with_rss(resp, url)
            if new_news:
                for message in new_news:
                    try:
                        r.push_uploaded_tag(json.dumps(message), key="parser")
                    except:
                        r = RABBIT()
                        r.push_uploaded_tag(json.dumps(message), key="parser")
        except AttributeError as ae:
            print(ae, url)
        except aiohttp.ClientConnectorError as ce:
            print(ce, url)
        except KeyError as ke:
            print(ke, url)
        except Exception:
            print(traceback.format_exc(),"\n" ,url)

if __name__ == '__main__':
    i = 0
    while True:
        print(i)
        ioloop = asyncio.get_event_loop()
        tasks = [ioloop.create_task(get_rss(link)) for link in URLS]
        ioloop.run_until_complete(asyncio.wait(tasks))

        i +=1
        time.sleep(36000)