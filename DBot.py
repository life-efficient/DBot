import sys
sys.path.append('..')
from bots.bot import Bot


class DBot(Bot):
    def __init__(self):
        super().__init__()
        self.driver.get('https://www.depop.com')
        self._scrape()

    def _scrape(self):
        self.search()

    def search(self):
        searches = ['jackets', 'jeans']
        for search in searches:
            self.driver.get()


if __name__ == '__main__':
    # EXAMPLE USAGE
    bot = DBot()