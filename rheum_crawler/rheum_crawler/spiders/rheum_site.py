# -*- coding: utf-8 -*-
from urllib.request import urlopen
import scrapy
from scrapy.http import Request


class RheumSpiderpdf(scrapy.Spider):
    name = "rheum_site"
    start_urls = [
    #'https://academic.oup.com/rheumatology',
    #'https://academic.oup.com/rheumatology/issue',
    #'https://academic.oup.com/rheumatology/advance-articles',
    #'https://academic.oup.com/rheumatology/search-results?page=1&f_OUPSeries=Editor%27s+Choice',
    #'https://academic.oup.com/rheumatology/pages/supplements',
    #'https://academic.oup.com/rheumatology/list-of-years?years=2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1997,1996,1995,1994,1993,1992,1991,1990,1989,1988,1987,1986,1985,1984,1983,1982,1981,1980,1979,1978,1977,1976,1975,1974,1973,1972,1971,1970,1969,1968,1967,1966,1965,1964,1963,1962,1961,1960,1959,1958,1957,1956,1955,1954,1953,1952&jn=Rheumatology'
    'https://academic.oup.com/rheumatology/issue/39/1'
    ]

    allowed_domains = ['academic.oup.com/rheumatology']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            yield Request(
                url=response.urljoin(href),
                callback=self.parse_article,
                dont_filter=True
            )


    def parse_article(self, response):
        # if there is a pdf link
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
        path = '../rheum_pdfs/' + path[0:end]
        # save to pdf
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)


### SPIDER FOR SCRAPING ABSTRACTS IF PDFS AREN'T AVAILABLE


class RheumSpiderAbstract(scrapy.Spider):
    name = "rheum_site_abstract"
    start_urls = [
    #'https://academic.oup.com/rheumatology',
    #'https://academic.oup.com/rheumatology/issue',
    #'https://academic.oup.com/rheumatology/advance-articles',
    #'https://academic.oup.com/rheumatology/search-results?page=1&f_OUPSeries=Editor%27s+Choice',
    #'https://academic.oup.com/rheumatology/pages/supplements',
    #'https://academic.oup.com/rheumatology/list-of-years?years=2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1997,1996,1995,1994,1993,1992,1991,1990,1989,1988,1987,1986,1985,1984,1983,1982,1981,1980,1979,1978,1977,1976,1975,1974,1973,1972,1971,1970,1969,1968,1967,1966,1965,1964,1963,1962,1961,1960,1959,1958,1957,1956,1955,1954,1953,1952&jn=Rheumatology'
    'https://academic.oup.com/rheumatology/issue/39/1'
    ]

    allowed_domains = ['academic.oup.com/rheumatology']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            yield Request(
                url=response.urljoin(href),
                callback=self.parse_article,
                dont_filter=True
            )


    def parse_article(self, response):
        # if there is a pdf link
        for href in response.css('a[href$=".pdf"]::attr(href)').extract():
            yield href
