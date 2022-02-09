import re
import uuid
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class DemoSpider(CrawlSpider):
    name = "scrap"
    allowed_domains = ["kennesaw.edu"]
    start_urls = [ "https://www.kennesaw.edu/","https://ccse.kennesaw.edu/","https://learnonline.kennesaw.edu/"]

    custom_settings={'USER_AGENT':'KSU CS4422-IRbot/0.1',
                     'DOWNLOAD_DELAY': 2,
                     'DEPTH_LIMIT': 1, #for BFS(FIFO)
                     'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
                     'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue',
                     'FEED_URI': "KrupexaIR_%(time)s.json",
                     'FEED_FORMAT': 'json'}

    #Duplicate URLs should not be revisited
    #Only the links with the domain name `kennesaw.edu' should be extracted for the next request.
    rules = (Rule(LinkExtractor(allow_domains =("kennesaw.edu"),
            restrict_xpaths = ("//div[@class = 'site_wrapper']",)),
            callback = "parse_item", follow = True),)

    #parse function which extracts information from the url response
    def parse_item(self, response):

        # str, A unique identifier for the page.
        # You may use a hash function (e.g., md5) to create a unique ID for a URL.
        page_id = uuid.uuid5(uuid.NAMESPACE_URL, response.text)
        page_id = str(page_id)

        #str, URL from which the page is fetched
        print("procesing:"+response.url)

        #str, Title of the page (if exists)
        titles = response.css("h1.page_title::text").extract()

        #str, Body text of the page.
        soup = BeautifulSoup(response.text, 'lxml')
        body = soup.get_text().replace("\n", " ").replace("\xa0", " ").replace("\t"," "), ("\r"," ")
        #body = (body.split())
        #body = body.strip("\n")

        #list, A list of email addresses found in the document.
        mails = [re.findall(r'[\w\.]+@[\w\.]+', response.text)]
        
        key = ('pageid', 'url', 'title', 'emails', 'body')
        entry = dict.fromkeys(key, "Null")
        entry['pageid'] = page_id
        entry['url'] = response.url
        entry['title'] = titles
        entry['emails'] = mails
        entry['body'] = body

        yield entry








