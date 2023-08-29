import os
import pandas as pd
import random
import re
from unidecode import unidecode

from scrapy.spiders import Spider

from ..items import FreshItem



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
    
    shorten_url = lambda self, url: url[url.find('oferta/')+7:]


    def __init__(self, search_url, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.search_url = search_url
        self.start_urls = [search_url]
    

    def validate_oferta(self, response, content_div=None) -> bool:
        if content_div is None:
            content_div = response
        content_raw = unidecode(content_div.get().lower())

        # load curses
        c_regexii = self.cursed_regexy.copy()
        c_miejsca = pd.DataFrame({'miejsce': pd.concat([self.cursed_miejsca.miejsce, self.cursed_miejsca.fraza])})

        c_miejsca['hits'] = c_miejsca.miejsce.apply(lambda x: x in content_raw)
        hits = c_miejsca[c_miejsca.hits]
        if len(hits) > 0:
            self.logger.info(f"Dropping {self.shorten_url(response.url)} due to cursed miejsca in content: {', '.join(hits.miejsce.to_list())}")
            return False

        c_regexii['hits'] = c_regexii.regex.apply(lambda x: re.search(x, content_raw))
        hits = c_regexii.hits[~c_regexii.hits.isna()]
        if len(hits) > 0:
            self.logger.info(f"Dropping {self.shorten_url(response.url)} due to cursed regexi in content: {', '.join(hits.apply(lambda x: x.group(0)).to_list())}")
            return False

        return True


    def parse_otooferta(self, response):
        assert "www.otodom.pl/pl/oferta" in response.url

        content_div = response.xpath('/html/body/div/main/div/div[2]')
        if self.validate_oferta(response, content_div.xpath('section[@role]')):
            item = FreshItem()
            item['smieszna_nazwa'] = voynich_generator()
            item['oryg_nazwa'] = content_div.xpath('header/h1/text()').get()
            item['czynsz_bazowy'] = int(re.search(r"[0-9]+", content_div.xpath('header/strong/text()').get().replace(' ',''))[0])
            czynsz_div = content_div.xpath('div[1]/div/div[2]/div[2]/div/text()').get()
            if czynsz_div is not None:
                item['czynsz_dodatkowo'] = int(re.search(r"[0-9]+", czynsz_div.replace(' ',''))[0])
            item['url'] = response.url
            # TODO: more
            yield item


    def parse_olxoferta(self, response):
        assert "www.olx.pl/d/oferta" in response.url

        content_div = response.css('div.css-1wws9er')
        if content_div is None:
            content_div = response.css('main section[role="region"]')
        if self.validate_oferta(response, content_div.css('div.css-bgzo2k.er34gjf0')):
            item = FreshItem()
            item['smieszna_nazwa'] = voynich_generator()
            item['oryg_nazwa'] = content_div.xpath('div[2]/h1/text()').get()
            item['czynsz_bazowy'] = int(content_div.xpath('div[3]/h3/text()').get().replace('zł','').replace(' ',''))
            item['czynsz_dodatkowo'] = int(re.search(r"[0-9]+",content_div.xpath('ul/li[last()]/p[@class="css-b5m1rv er34gjf0"]/text()').get().replace(' ',''))[0])
            item['url'] = response.url
            # TODO: more
            yield item


    def parse_oferta(self, response):
        if "olx.pl/d/oferta" in response.url:
            yield from self.parse_olxoferta(response)

        elif "otodom.pl/pl/oferta/" in response.url:
            yield from self.parse_otooferta(response)


    def parse(self, response):
        # load curses and old links
        self.cursed_regexy = pd.read_csv(self.settings.get('CURSED_REGEXII_PATH'))
        self.cursed_regexy.regex = self.cursed_regexy.regex.apply(lambda x: re.compile(unidecode(x).lower()))
        self.cursed_miejsca = pd.read_csv(self.settings.get('CURSED_MIEJSCA_PATH')).apply(lambda x: x.str.lower().apply(unidecode))
        try:
            old_links = pd.concat([pd.read_csv(uri) for uri in self.settings.get('FEEDS').keys() if uri.endswith('csv')]).url
        except pd.errors.EmptyDataError: 
            old_links = pd.Series()

        if "oferta" in response.url:
            self.logger.info("The provided search_url is an oferta. Parsing the oferta.")
            yield from self.parse_oferta(response)
        
        elif "olx.pl" in response.url:
            good_links = []
            ofertas = response.css('div.css-1sw7q4x[data-cy="l-card"]')

            for o in ofertas:
                link = o.xpath('a/@href').get()
                if any(old_links.str.endswith(link)):
                    continue
                o_title = unidecode(o.css('h6').get().lower())
                hits = pd.DataFrame(
                    {'miejsca': self.cursed_miejsca.miejsce.apply(lambda x: x in o_title),
                       'frazy':   self.cursed_miejsca.fraza.apply(lambda x: x in o_title)}
                )
                if any(hits.miejsca) or any(hits.frazy):
                    # TODO: explain which miejsca or frazy?
                    self.logger.info(f"Dropping {self.shorten_url(link)} due to cursed miejsce in title.")
                    continue
                good_links.append(link)
            
            yield from response.follow_all(good_links, self.parse_oferta)

