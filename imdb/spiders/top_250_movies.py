# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Top250MoviesSpider(CrawlSpider):
    
    name = 'top_250_movies'
    allowed_domains = ['imdb.com']
    # since we overide start_requests, we don't need start_urls here anymore
    # start_urls = ['https://www.imdb.com/list/ls068082370/']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

    # we don't specify callback in the second Rule because everytime it visits the next page it will call the first rule
    # to execute with the callback and follow
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//a[contains(@class, 'next-page')]"), process_request='set_user_agent')
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/list/ls068082370/', headers={
            'User-Agent': self.user_agent
        })

    def parse_item(self, response):
        
        # normalize-space is used to remove the space pre and post the duration
        yield {
            'title': response.xpath("//div[@class='title_wrapper']/h1/text()").get(),
            'year': response.xpath("//span[@id='titleYear']/a/text()").get(),
            'duration': response.xpath("normalize-space(//div[@class='subtext']/time/text())").get(),
            'genre': response.xpath("//div[@class='subtext']/a[1]/text()").get(),
            'rating': response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            'movie_url': response.url
        }
