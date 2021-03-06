import os, sys
from pathlib import Path

module_path = os.path.join(Path(__file__).parent.absolute().as_posix(), '..')

if module_path not in sys.path:
    sys.path.append(module_path)

from crawl.rss_feed_crawler import RSSFeedCrawler
from repository.crawl_info_repository import CrawlInfoRepository
import telegram


MY_TOKEN = ''
CHAT_ID = ''


def read_site_list():
    site_list = []
    dest = 'resources/'

    with open(os.path.join(Path(__file__).parent.absolute().as_posix(), '..', dest, 'sites.txt'), 'r') as lines:
        while True:
            line = lines.readline()

            if not line: break

            if line.startswith("#"):
                continue
            site_list.append(line.strip())

    return site_list


if __name__ == "__main__":
    print(read_site_list())
    repository = CrawlInfoRepository()
    sites = read_site_list()
    crawler = RSSFeedCrawler(sites, repository)
    contents = crawler.get_site_contents()

    bot = telegram.Bot(token=MY_TOKEN)

    for content in contents:
        bot.sendMessage(chat_id=CHAT_ID, text="%s\n%s" % (content['title'], content['content_url']))
