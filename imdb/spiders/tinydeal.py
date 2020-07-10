# -*- coding: utf-8 -*-
import scrapy


class TinydealSpider(scrapy.Spider):
    name = 'tinydeal'
    allowed_domains = ['www.tinydeal.com']
    start_urls = ['https://tinydeal.com/specials.html']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

    def start_request(self):
        yield scrapy.Request(url='https://tinydeal.com/specials.html', headers={
            'User-Agent': self.user_agent
        })

    def parse(self, response):
        for product in response.xpath("//li[@class='productListing-even']"):
            yield {
                'title': product.xpath(".//a[@class='p_box_title']/text()").get(),
                'url': response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
                'discounted_price': product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                'original_price': product.xpath(".//div[@class='p_box_price']/span[2]/text()").get(),
                'User-Agent': response.request.headers['User-Agent']
            }

        next_page = response.xpath("//a[@class='nextPage']").get()
        if next_page:
            next_url = response.xpath("//a[@class='nextPage']/@href").get()
            # we can use follow or scrapy.Request to continue to next page

            # yield scrapy.Request(url=next_url, callback=self.parse)
            yield response.follow(url=next_url, callback=self.parse, headers={
                'User-Agent': self.user_agent
            })
