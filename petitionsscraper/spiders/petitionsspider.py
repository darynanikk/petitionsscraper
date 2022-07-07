import json
import time

from scrapy import Request, FormRequest, Spider, Selector
from petitionsscraper.items import PetitionsScraperItem


class PetitionSpider(Spider):
    name = 'petition_spider'
    start_urls = ['https://petition.president.gov.ua/petition/146960']

    def parse(self, response, **kwargs):
        last_page = int(response.css('.pag_child:nth-child(7) .pag_link::text').get())

        for i in range(last_page + 1):
            source = f'{response.url}/votes/{i}'
            self.log(f'Found source: {source}')
            yield Request(source, callback=self.parse_vote)

    def parse_vote(self, response):
        selector = Selector(text=response.body, type='html')
        vote_item = PetitionsScraperItem()
        for vote in selector.css('.table .table_row'):
            number = vote.css('.number::text').get()
            vote_item['order_number'] = number[:number.find('.')]
            vote_item['name'] = vote.css('.name::text').get()
            vote_item['date'] = vote.css('.date::text').get()
            self.logger.info(f'Parsed vote: {vote_item}')
            yield vote_item
