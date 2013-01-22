# Scrapy settings for data_mining project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'data_mining'

SPIDER_MODULES = ['data_mining.spiders']
NEWSPIDER_MODULE = 'data_mining.spiders'
DOWNLOAD_DELAY = 0.5

ITEM_PIPELINES = [
    'data_mining.pipelines.StripPipeline',
    'data_mining.pipelines.ValidationPipeline',
    'data_mining.pipelines.DetermineTypePipeline',
    'data_mining.pipelines.DropSpamPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'data_mining (+http://www.yourdomain.com)'
