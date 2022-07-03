import re
import json
from scrapy import Request, Spider, Selector
from petitionsscraper.items import PetitionsscraperItem


class PetiionSpider(Spider):
    name = 'petition_spider'
    start_urls = ['https://petition.president.gov.ua/petition/146960']
    
    def parse(self, response, **kwargs):
        last_page = int(response.css('.pag_child:nth-child(7) .pag_link::text').get())
            
        for i in range(last_page+1):
            source = f'{response.url}/votes/{i}/json'
            self.log(f'Found source: {source}')
            yield Request(source, callback=self.parse_vote)
        
    def parse_vote(self, response):
        table_html = json.loads(response.body)['table_html']
        selector = Selector(text=table_html, type='html')
        vote_item = PetitionsscraperItem()
        for vote in selector.css('.table .table_row'):
            number = re.sub(r"\D", "", vote.css('.number::text').get())
            vote_item['number'] = int(number)
            vote_item['name'] = vote.css('.name::text').get()
            vote_item['date'] = vote.css('.date::text').get()
            self.logger.info(f'Parsed vote: {vote_item}')
            yield vote_item