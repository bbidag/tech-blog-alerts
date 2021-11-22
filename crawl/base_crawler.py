from abc import *


class BaseCrawler(metaclass=ABCMeta):

    @abstractmethod
    def get_site_contents(self, url):
        pass

    @abstractmethod
    def is_exist_site(self, site):
        pass

    @abstractmethod
    def is_exist_site_contents(self, site_url, content_url):
        pass

    @abstractmethod
    def is_not_out_of_date(self, contents):
        pass
