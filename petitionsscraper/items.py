from scrapy.item import Field
import scrapy


class PetitionsScraperItem(scrapy.Item):
    order_number = Field()
    name = Field()
    date = Field()