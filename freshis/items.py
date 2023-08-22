# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FreshItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    smieszna_nazwa = scrapy.Field()
    oryg_nazwa = scrapy.Field()
    czynsz_bazowy = scrapy.Field()
    czynsz_dodatkowo = scrapy.Field()
    url = scrapy.Field()
    # TODO: more