from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from data_mining.items import AddItem
from scrapy import log

from urlparse import urljoin
import datetime
import json
import re


class MobilePhonesSpider(BaseSpider):

    name = "mobile_phones"
    allowed_domains = ["999.md"]
    start_urls = [
        "http://999.md/#!/list/phone-and-communication/mobile-phones"
    ]
    page_number = 1
    base_url = 'http://999.md/'

    def parse(self, response):
        '''
        Extract add links and proceed to the next page
        '''
        hxs = HtmlXPathSelector(response)
        add_links = hxs.select(".//div[@class='adsPage__list__title']/a/@href").extract()
        for add_link in add_links:
            print add_link
            json_url = self.buildURL(add_link)
            if json_url:
                log.msg("Found link %s" % json_url, level=log.INFO)
                yield Request(json_url, callback=self.parseItem, priority=2, meta={'link': add_link})

        self.page_number += 1
        if self.page_number == 6:
            raise CloseSpider('Stopping spider - scraped 1000 pages')
        next_page_link = self.start_urls[0] + '/' + str(self.page_number)
        log.msg("Going to the next page %s" % next_page_link, level=log.INFO)
        yield Request(next_page_link, callback=self.parse, priority=1)
        # yield Request("http://999.md/backend/view/ad?id=1283071&language=ro", callback=self.parseItem, meta={'link': '/#!/1283071/'})


    def buildURL(self, link):

        try:
            id = re.search(r'(\d+)', link).group(1)
        except:
            return

        url = "http://999.md/backend/view/ad?id=%s&language=ro" % id
        return url


    def parseItem(self, response):
        '''
        Extract necessary data from a specific add
        '''

        item = AddItem()
        try:
            json_item = json.loads(response.body)
        except:
            log.msg("An error occured while trying to load the json file", level=log.ERROR)
            return

        try:
            json_item_short = json_item['result']['ad']
        except KeyError:
            return

        item['url'] = urljoin(self.base_url, response.meta['link'])
        try:
            item['id'] = json_item_short['id']
        except KeyError:
            item['id'] = 0
        try:
            item['title'] = json_item_short['title']
        except KeyError:
            item['title'] = ''
        try:
            item['author'] = json_item_short['user']['login']
        except KeyError:
            item['author'] = ''

        try:
            date = json_item_short['date']
            item['date'] = datetime.datetime.fromtimestamp(date) - datetime.timedelta(hours=1)
        except:
            item['date'] = None

        try:
            item['region'] = json_item_short['features']['7']['value']
        except KeyError:
            item['region'] = ''
        try:
            item['type'] = json_item_short['features']['1']['value']
        except KeyError:
            item['type'] = ''
        try:
            item['views'] = int(json_item['result']['views'])
        except:
            item['views'] = None
        try:
            item['pics_number'] = len(json_item_short['features']['14']['value'])
        except:
            item['pics_number'] = None
        try: 
            item['description'] = json_item_short['features']['13']['value']
        except KeyError:
            item['description'] = ''

        try:
            contacts = json_item_short['features']['16']['value'][0]
            item['contacts'] = str(contacts['prefix']['country']) + str(contacts['prefix']['local']) + str(contacts['number'])
        except:
            item['contacts'] = ''

        yield item



