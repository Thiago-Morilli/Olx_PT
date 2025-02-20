
import scrapy


class OlxPtItem(scrapy.Item):
    Title = scrapy.Field()
    Model = scrapy.Field()
    Price = scrapy.Field()
    Brand = scrapy.Field()
    production_data = scrapy.Field()
    City = scrapy.Field()
    Description = scrapy.Field()
