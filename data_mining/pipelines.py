from scrapy.exceptions import DropItem
from scrapy import log
from urlparse import urlparse
import datetime


class StripPipeline(object):
    '''
    This class implements the striping of strings
    '''
    def process_item(self, item, spider):

        item['url'] = item['url'].strip()
        item['title'] = item['title'].strip()
        item['author'] = item['author'].strip()
        item['region'] = item['region'].strip()
        item['type'] = item['type'].strip()
        item['description'] = item['description'].strip()
        item['contacts'] = item['contacts'].strip()

        return item

class ValidationPipeline(object):
    '''
    Validates types and values of item attributes
    '''

    def process_item(self, item, spider):

        if not urlparse(item['url']).scheme or not urlparse(item['url']):
            log.msg('Malformed URL for item with id %s' % item['id'], level=log.INFO)
            item['url'] = None

        if item['id'] == 0:
            log.msg('The item %s has no id' % item['url'], level=log.INFO)

        if type(item['date']) is not datetime.datetime:
            log.msg('Invalid datetime object for item %s' % item['url'], level=log.INFO)
            item['date'] = None

        if type(item['views']) is not int:
            log.msg('Invalid type for views for item %s. Should be integer.' % item['url'], level=log.INFO)
            item['views'] = 0

        if type(item['pics_number']) is not int:
            log.msg('Invalid type for number of pictures for item %s. Should be integer.' % item['url'], level=log.INFO)
            item['pics_number'] = 0

        return item


class DetermineTypePipeline(object):
    '''
    Determine the type of add: buy or sell
    ''' 
    def process_item(self, item, spider):

        if item['type'] == u'V\u00eend':
            item['type'] = 'sell'
        elif item['type'] == u'Cump\u0103r':
            item['type'] = 'buy'

        return item


class DropSpamPipeline(object):
    '''
    Consider dropping ads that have more than 
    5 phones listed in their advertisement.
    This is a simple spam detection.
    '''
    def __init__(self):
        self.file = open('phones.txt', 'r')
        self.phones = self.file.read().lower().split('\n')

    def process_item(self, item, spider):
        
        nr_of_phones = 0
        contents = item['title'].lower() + item['description'].lower()
        for phone in self.phones:
            if phone in contents:
                nr_of_phones += 1

        if nr_of_phones > 5:
            raise DropItem("This is presumably spam. %s has more than 5 phones listed in the description" %item['url'])
        else:
            return item


