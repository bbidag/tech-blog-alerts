from crawl.base_crawler import BaseCrawler
import feedparser
from datetime import datetime
from datetime import timedelta
from time import mktime


GENERAL_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class RSSFeedCrawler(BaseCrawler):
    def __init__(self, sites, crawl_info_repository):
        self.sites = sites
        self.crawlInfoRepository = crawl_info_repository

    def parse_date(self, feed_item):
        if 'updated_parsed' in feed_item:
            time = mktime(feed_item['updated_parsed'])
        if 'published_parsed' in feed_item:
            time = mktime(feed_item['published_parsed'])

        assert time is not None

        parsed_date = datetime.fromtimestamp(time)
        return parsed_date.strftime(GENERAL_DATE_FORMAT)

    def parse_content_format(self, site, entries):
        docs = []
        for entry in entries:
            doc = {'site_url': site, 'content_url': entry['link'], 'title': entry['title'], 'pub_date': self.parse_date(entry), 'content': entry['summary']}
            docs.append(doc)
        return docs

    def get_site_contents(self):
        contents = []
        for site in self.sites:
            feed = feedparser.parse(site)
            entries = feed['entries']
            docs = self.parse_content_format(site, entries)
            dedups = self.save_if_not_duplicate(docs, site)
            self.update_site_mod_dts(site, feed['feed']['title'])
            contents.extend(dedups)
        return contents

    def is_exist_site(self, site):
        return self.crawlInfoRepository.is_exist_site(site)

    def is_exist_site_contents(self, site_url, content_url):
        return self.crawlInfoRepository.is_exist_site_contents(site_url, content_url)

    def is_not_out_of_date(self, published_at):
        return datetime.strptime(published_at, GENERAL_DATE_FORMAT) > datetime.now() - timedelta(days=30)

    def save_if_not_duplicate(self, docs, site):
        dedups = []
        for doc in docs:
            if self.is_exist_site_contents(site, doc['content_url']):
                continue
            if self.is_not_out_of_date(doc['pub_date']):
                self.crawlInfoRepository.insert_site_contents(doc)
                dedups.append(doc)
        return dedups

    def update_site_mod_dts(self, site, title):
        if self.is_exist_site(site):
            self.crawlInfoRepository.update_site_info(site)
        else:
            self.crawlInfoRepository.insert_site_info(site, title)

