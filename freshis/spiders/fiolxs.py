import re
import random
import pandas as pd
from unidecode import unidecode

from scrapy.spiders import Spider

from ..items import FreshItem

import os

# blame https://stackoverflow.com/questions/67854396/how-to-bypass-cloudflare-restrictions-with-scrapy
# from scrapy_selenium import SeleniumRequest

#     def start_requests(self):
#         # Driver Path and Options for Selenium is done in settings file
#         yield SeleniumRequest(
#             url='http://example.com',
#             wait_time=3,
#             callback=self.parse,
#         )

#     def parse(self, response):
#         # Get selenium web driver from response object
#         driver = response.meta['driver']
     

#         # Grab Modified response from webdriver
#         page_html = driver.page_source
#         pageResponseObj = Selector(text=page_html)


def voynich_generator() -> str:
    """
    always good to have one.
    :return: a slovo
    """
    prefixy = ["xi", "be", "su", "ta", "ro", "pu", "lo", "fero", "pi", "ju", "je", "ja"]
    intefixy = ["de", "ra", "ko", "su", "ke", "for", "kus", "rami", "n", "non", "suko"]
    sufixy = ["za", "fi", "no", "tix", "ter", "mer", "pir", "sena", "soto", "zur", "dos", "dex", "dek", "le", "ra"]
    bub = random.random()
    if bub <= 0.3333333333333:
        slowo = random.choice(prefixy) + random.choice(intefixy) + random.choice(sufixy)
    elif bub <= 0.6666666666666:
        slowo = random.choice(prefixy) + random.choice(sufixy)
    else:
        slowo = random.choice(prefixy) + random.choice(intefixy) + random.choice(intefixy)
    return slowo

# previous scraper did not bother with pagination, only read the first page
# this is something to consider, but for now we shall only parse the first page too

class FiolxSpider(Spider):
    # scrapes olx but also otodom
    name = "fiolxs"
    allowed_domains = ["www.olx.pl", "www.otodom.pl"]
    # handle_httpstatus_list = [403]
    
    custom_settings = {     # to attempt retry middleware
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'freshis.middlewares.FiolxRetryMiddleware': 399,
            # 'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            # 'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
        }
    }

    shorten_url = lambda self, url: url[url.find('oferta/')+7:]


    def __init__(self, search_url, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [search_url]
    

    def parse_oferta(self, response):
        assert "olx.pl/d/oferta" in response.url
        # load curses
        curses = self.cursed_regexii.copy()

        content_div = response.css('div.css-1wws9er')
        opis_raw = unidecode(content_div.css('div.css-bgzo2k.er34gjf0').get().lower())

        curses['hits'] = curses.regex.apply(lambda x: re.search(x, opis_raw))
        hits = curses.hits[~curses.hits.isna()]

        if len(hits) > 0:
            self.logger.info(f"Dropping {self.shorten_url(response.url)} due to cursed regexi in opis: {', '.join(hits.apply(lambda x: x.group(0)).to_list())}")

        item = FreshItem()
        item['smieszna_nazwa'] = voynich_generator()
        item['oryg_nazwa'] = content_div.xpath('div[2]/h1/text()').get()
        item['czynsz_bazowy'] = int(content_div.xpath('div[3]/h3/text()').get().replace('zł','').replace(' ',''))
        item['czynsz_dodatkowo'] = int(re.search(r"[0-9]+",content_div.xpath('ul/li[last()]/p[@class="css-b5m1rv er34gjf0"]/text()').get())[0])
        item['url'] = response.url
        # TODO: more

        yield item


    def parse(self, response):
        # load curses
        self.cursed_regexii = pd.read_csv(self.settings.get('CURSED_REGEXII_PATH'))
        self.cursed_regexii.regex = self.cursed_regexii.regex.apply(lambda x: re.compile(unidecode(x).lower()))
        cursed_miejsca = pd.read_csv(self.settings.get('CURSED_MIEJSCA_PATH')).apply(lambda x: x.str.lower().apply(unidecode))

        # parse otodom elsewhere
        if "olx.pl/d/oferta" in response.url:
            self.logger.info("The provided search_url is an oferta. Parsing the oferta.")
            yield from self.parse_oferta(response)
        elif "olx.pl" in response.url:
            ofertas = response.css('div.css-1sw7q4x[data-cy="l-card"]')
            good_links = []

            for o in ofertas:
                o_title = unidecode(o.css('h6').get().lower())
                link = o.xpath('a/@href').get()
                hits = pd.DataFrame(
                    {'miejsca': cursed_miejsca.miejsce.apply(lambda x: x in o_title),
                       'frazy':   cursed_miejsca.fraza.apply(lambda x: x in o_title)}
                )
                if any(hits.miejsca) or any(hits.frazy):
                    # TODO: explain which miejsca or frazy?
                    self.logger.info(f"Dropping {self.shorten_url(link)} due to cursed miejsce in title.")
                    continue
                good_links.append(link)
            
            # TODO: here filter out 
            # good_links = filter(lambda x: x not in old_links, good_links)
            yield from response.follow_all(good_links, self.parse_oferta)

        else:
            self.logger.error("Unexpected url: " + response.url)

