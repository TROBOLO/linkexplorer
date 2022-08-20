import argparse
import datetime
import json

from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings

from bs4 import BeautifulSoup

from urllib.parse import urlparse


class LinkCrawler(CrawlSpider):
    name = 'linkcrawler'
    rules = [Rule(LinkExtractor(), callback="parse_url", follow=True)]

    def __init__(self, *args, **kwargs):
        super(LinkCrawler, self).__init__(*args, **kwargs)
        self.allowed_domains = [kwargs.get('allowed_domains')]
        self.start_urls = [kwargs.get('start_urls')]
        self.links = {
            "links": []
        }

    def parse_url(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            item = {
                "link_source": response.url,
                "link_target": link.get("href"),
                "link_text": link.text.strip(),
            }

            # check if there is an dict in the self.links list with the same link_target and link_text
            # if not, add the item to the list
            if not any(d['link_target'] == item['link_target'] and d['link_text'] == item['link_text'] and d['link_source'] == item['link_source'] for d in self.links['links']):
                 self.links['links'].append(item)

        return

    def closed(self, reason):
        print("[*] Finished. Reason: {}".format(reason))
        print("[*] Found {} links".format(len(self.links['links'])))
        
        # write links to file as json 
        with open('links.json', 'w') as f:
            f.write(json.dumps(self.links))


def main(args):
    parsed = urlparse(args.url)
    root_domain = parsed.netloc
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_LEVEL': 'INFO'
    })
    process.crawl(LinkCrawler, allowed_domains=root_domain,
                  start_urls=args.url)
    process.start()


def parser():
    p = argparse.ArgumentParser(description='LinkCrawler')
    p.add_argument(
        '-u', '--url', help="Define the URL to scrape", required=True)

    return p.parse_args()


if __name__ == '__main__':
    args = parser()
    main(args)
