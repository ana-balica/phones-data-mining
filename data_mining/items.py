# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class AddItem(Item):
    '''
    Container that are stores all add fields
    '''
    url = Field()
    id = Field()
    title = Field()
    author = Field()
    author_url = Field()
    date = Field()
    region = Field()
    type = Field()
    views = Field()
    pics_number = Field()
    description = Field()
    contacts = Field()    
