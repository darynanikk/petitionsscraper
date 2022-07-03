from scrapy.item import Item, Field
import scrapy


class PetitionsscraperItem(scrapy.Item):
    number = Field()
    name = Field()
    date = Field()