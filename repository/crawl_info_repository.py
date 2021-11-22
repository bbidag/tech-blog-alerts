import sqlite3
import os
from pathlib import Path

CREATE_SITE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS site(
        site_url TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        is_disabled INTEGER DEFAULT 1,
        mod_dts TIMESTAMP DEFAULT (datetime('now','localtime'))
    )"""

CREATE_CONTENTS_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS site_contents(
        site_url TEXT NOT NULL,
        content_url TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        pub_date TIMESTAMP,
        PRIMARY KEY (site_url, content_url)
    )"""


class CrawlInfoRepository:
    def __init__(self):
        dest = 'resources'
        dest_path = os.path.join(Path(__file__).parent.absolute().as_posix(), '..', dest, 'crawl_info.db')
        self.conn = sqlite3.connect(dest_path, isolation_level=None)
        cur = self.conn.cursor()
        cur.execute(CREATE_SITE_TABLE_SQL)
        cur.execute(CREATE_CONTENTS_TABLE_SQL)
        cur.close()

    def insert_site_info(self, site_url, title, is_disabled = 0):
        c = self.conn.cursor()
        c.execute("INSERT INTO site (site_url, title, is_disabled) VALUES (?,?,?)", (site_url, title, is_disabled))
        c.close()

    def insert_site_contents(self, contents):
        c = self.conn.cursor()
        c.execute("INSERT INTO site_contents VALUES (?,?,?,?,?)", (contents['site_url'], contents['content_url'],
                contents['title'], contents['content'], contents['pub_date']))
        c.close()

    def is_exist_site(self, site_url):
        c = self.conn.cursor()
        exist = c.execute("SELECT EXISTS(SELECT 1 FROM site WHERE site_url = '%s')" % site_url).fetchone()
        c.close()
        return exist[0]

    def is_exist_site_contents(self, site_url, content_url):
        c = self.conn.cursor()
        exist = c.execute("SELECT EXISTS(SELECT 1 FROM site_contents WHERE site_url = '%s' AND content_url = '%s')" % (site_url, content_url)).fetchone()
        c.close()
        return exist[0]

    def update_site_info(self, site):
        c = self.conn.cursor()
        c.execute("UPDATE site SET mod_dts = DATETIME('now') WHERE site_url = '%s'" % site)
        c.close()
