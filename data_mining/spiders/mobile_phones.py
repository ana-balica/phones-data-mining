from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from data_mining.items import AddItem
from scrapy import log

from urlparse import urljoin
import re


class MobilePhonesSpider(BaseSpider):

    name = "mobile_phones"
    allowed_domains = ["999.md"]
    start_urls = [
        "http://999.md/#!/list/phone-and-communication/mobile-phones"
    ]

    def parse(self, response):
        '''
        Extract add links and proceed to the next page
        '''
        yield Request("http://999.md/#!/1487148", callback=self.parseItem, cookies={'simpalsid.lang': 'ro-Ro'})
        # hxs = HtmlXPathSelector(response)
        # add_links = hxs.select(".//div[@class='adsPage__list__title']/a/@href").extract()
        # for add_link in add_links:
        #     add_link = urljoin(response.url, add_link)
        #     log.msg("Found link %s" % add_link, level=log.INFO)
        #     yield Request(add_link, callback=self.parseItem, priority=2, cookies={'simpalsid.lang': 'ro-Ro'}, meta={'dont_merge_cookies': True})

        # next_page = hxs.select("//li[@class='current']/following-sibling::li[1]")
        # if next_page:
        #     next_page_number = next_page.select('text()').extract()
        #     if next_page_number == '11':
        #         raise CloseSpider('Stopping spider - scraped 1000 pages')
        #     next_page_link = next_page.select("a/@href").extract()
        #     next_page_link = urljoin(response.url, next_page_link[0])
        #     log.msg("Going to the next page %s" % next_page_link, level=log.INFO)
        #     yield Request(next_page_link, callback=self.parse, priority=1)


    def parseItem(self, response):
        '''
        Extract necessary data from a specific add
        '''
        hxs = HtmlXPathSelector(response)
        item = AddItem()
        item['url'] = response.url
        id = re.search(r'(\d{7})', response.url)
        try:
            item['id'] = id.group(1)
        except:
            item['id'] = ''


        title = hxs.select(".//header/h1/text()").extract()
        item['title'] = title[0] if title else ''

        author = hxs.select(".//section[@class='adPage__header__stats']/dl[1]/dd/a/text()").extract()
        item['author'] = author[0] if author else ''

        author_url = hxs.select(".//section[@class='adPage__header__stats']/dl[1]/dd/a/@href").extract()
        item['author_url'] = urljoin(response.url, author_url[0]) if author_url else ''

        date = hxs.select(".//section[@class='adPage__header__stats']/dl[2]/dd/text()").extract()
        item['date'] = self.parseDate(date[0]) if date else ''

        region = hxs.select(".//section[@class='adPage__header__stats']/dl[3]/dd/text()").extract()
        item['region'] = region[0] if date else ''

        type = hxs.select(".//section[@class='adPage__header__stats']/dl[4]/dd/text()").extract()
        item['type'] = type[0] if type else ''

        views = hxs.select(".//section[@class='adPage__header__stats']/dl[5]/dd/text()").extract()
        try:
            item['views'] = int(views[0])
        except:
            item['views'] = None

        pics = hxs.select(".//div[contains(@class,'adPage__content__photos')]/a/img/@src").extract()
        item['pics_number'] = len(pics)

        description = hxs.select(".//div[contains(@class,'adPage__content__description')]/text()").extract()
        item['description'] = description[0] if description else ''

        yield item



    def parseDate(self, date_string):
        return ''



