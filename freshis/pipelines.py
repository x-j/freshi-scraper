import os


from itemadapter import ItemAdapter


class FreshisPipeline:

    def open_spider(self, spider):
        feeds = spider.settings.getdict('FEEDS')
        num_csv_feeds = sum([uri.endswith('.csv') for uri in feeds.keys()])
        if num_csv_feeds > 1 and os.path.exists("out/fresh-info.csv"):
            outsize = len(os.listdir('out'))
            newname = f"old-fresh-info-{str(outsize)}.csv"
            spider.logger.info(f"Alternate csv output feed detected. I am renaming the previous fresh-info.csv to {newname}")
            os.rename('out/fresh-info.csv', 'out/'+newname)


    def process_item(self, item, spider):
        return item
