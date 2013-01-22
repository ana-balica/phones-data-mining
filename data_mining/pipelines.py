from scrapy.exceptions import DropItem


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


class DetermineTypePipeline(object):
    '''
    Determine the type of add: buy or sell
    ''' 
    def process_item(self, item, spider):

        if item['type'] == 'V\u00eend':
            item['type'] = 'sell'
        elif item['type'] == 'Cump\u0103r':
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
        self.nr_of_phones = 0

    def process_item(self, item, spider):
        
        contents = item['title'].lower() + item['description'].lower()
        for phone in self.phones:
            if phone in contents:
                self.nr_of_phones += 1

        if self.nr_of_phones > 5:
            raise DropItem("This is presumably spam. %s has more than 5 phones listed in the description" % item)
        else:
            return item


