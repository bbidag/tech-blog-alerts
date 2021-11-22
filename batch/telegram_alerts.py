import os
from pathlib import Path

from crawl.rss_feed_crawler import RSSFeedCrawler
from repository.crawl_info_repository import CrawlInfoRepository
import telegram


MY_TOKEN = ''


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
    chat_id = bot.getUpdates()[-1].message.chat.id

    for content in contents:
        bot.sendMessage(chat_id=chat_id, text="%s\n%s" % (content['title'], content['content_url']))
