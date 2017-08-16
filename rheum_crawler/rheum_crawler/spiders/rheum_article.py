# -*- coding: utf-8 -*-
from urllib.request import urlopen
import scrapy
from scrapy.http import Request


class RheumSpiderpdf(scrapy.Spider):
    name = "rheumpdf"
    start_urls = ['https://academic.oup.com/rheumatology/article/doi/10.1093/rheumatology/keh199/1788304/Benefit-of-very-early-referral-and-very-early']
    allowed_domains = ['academic.oup.com/rheumatology']

    def parse(self, response):
        for href in response.css('li.toolbar-item a[href$=".pdf"]::attr(href)').extract():
            yield Request(
                url=response.urljoin(href),
                callback=self.save_pdf,
                dont_filter=True
            )
    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        # remove temporary link key
        file_id = '.pdf'
        end = path.find(file_id,0) + len(file_id)
        path = path[0:end]
        # save to pdf
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
