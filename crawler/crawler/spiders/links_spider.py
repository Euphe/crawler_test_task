import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
from scrapy.item import Item, Field
class NodeItem(scrapy.Item):
    current_url = scrapy.Field()
    referring_url = scrapy.Field()

class LinksSpider(CrawlSpider):
    def __init__(self, *args, **kwargs): 
      super(LinksSpider, self).__init__(*args, **kwargs) 
      self.start_urls = kwargs.get('start_urls')

    name = 'links_spider'
    rules = ( Rule (LinkExtractor(allow=("", ),),
            callback="parse_items",  follow= True),
    )

    def parse_items(self, response):
        items = []
        item = NodeItem()
        item["current_url"] = str(response.url)
        referring_url = response.request.headers.get('Referer', None)
        item["referring_url"] = referring_url.decode('utf-8')
        items.append(item)
        return items
