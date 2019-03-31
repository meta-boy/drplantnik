import datetime
from urllib.parse import parse_qs
import asyncio

import aiohttp

from lxml import etree


class Google:

    async def get_google_entries(self, query):
        params = {
            'q': query,
            'hl': 'en'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
        }
        entries = []
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.google.com/search', params=params, headers=headers) as resp:
                if resp.status != 200:
                    raise RuntimeError('Google somehow failed to respond.')

                root = etree.fromstring(await resp.text(), etree.HTMLParser())
                # card_node = root.find(".//div[@id='topstuff']")
                # card = self.parse_google_card(card_node)
                search_nodes = root.findall(".//div[@class='g']")
                for node in search_nodes:
                    url_node = node.find('.//h3/a')
                    if url_node is None:
                        continue
                    url = url_node.attrib['href']
                    if not url.startswith('/url?'):
                        continue
                    url = parse_qs(url[5:])['q'][0]
                    entries.append(url)
        return entries

    # Google Command, clumsy but works~
    async def g(self, query):
        """Google for whatever you like."""
        try:
            entries = await self.get_google_entries(query)
        except RuntimeError as e:
            print(content=str(e))
        else:
            next_two = entries[1:3]
            before = entries[:10]
            before = before[:-1] + '%29' if before[-1] == ')' else before

            if len(entries) == 0:
                return print("https://www.google.com/search?q=" + query.replace(" ", "+"))
                 
            elif next_two and not entries:
                formatted = '\n'.join(map(lambda x: '%s' % x, next_two))
                print(formatted)
            else:
                print("\n".join(before))