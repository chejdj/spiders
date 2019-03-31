# -*- coding: utf-8 -*-

# Scrapy settings for explore project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'android_bus'

SPIDER_MODULES = ['android_bus.spiders']
NEWSPIDER_MODULE = 'android_bus.spiders'
MONGO_URI = '127.0.0.1:27017'
MONGO_DATABASE = 'zhihu_user'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'explore (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie':'_uab_collina=155126903548946434885494; UM_distinctid=1692ed705964-083ccfa3e9d68b-36657105-13c680-1692ed705975e3; rajL_2132_saltkey=lhtdHeDl; rajL_2132_lastvisit=1554015123; rajL_2132_pc_size_c=0; rajL_2132_viewid=blog_79765; rajL_2132_nofocus_home=1; CNZZDATA1257119092=1544842857-1551266742-null%7C1554021747; Hm_lvt_017b20ea7175a0f1c1d2986e70969473=1551773649,1554018731,1554019431,1554022013; Hm_lvt_9a38139975e66f82168b87eb12ddf97d=1551773649,1554018731,1554019431,1554022013; Hm_lvt_29b902bb270d54143715474591145950=1551773649,1554018731,1554019431,1554022013; Hm_lvt_7ca494ee88867e1c48fc51ebb852cea9=1551773649,1554018731,1554019431,1554022013; rajL_2132_sid=x0kY9q; Hm_lpvt_017b20ea7175a0f1c1d2986e70969473=1554023119; Hm_lpvt_7ca494ee88867e1c48fc51ebb852cea9=1554023119; Hm_lpvt_29b902bb270d54143715474591145950=1554023119; rajL_2132_lastact=1554023114%09connect.php%09check; Hm_lpvt_9a38139975e66f82168b87eb12ddf97d=1554023120',
}
# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'explore.middlewares.ExploreSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'explore.middlewares.ExploreDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'android_bus.pipelines.ArticlePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
