# %%
import sys
sys.path.append('..')
from bots.bot import Bot
from time import sleep
import os
import boto3


class DBot(Bot):
    def __init__(self, headless=False):
        super().__init__(headless=headless)
        self.driver.get('https://www.depop.com')
        # self._scrape()

    def _scrape(self):
        searches = ['jackets', 'jeans']
        for search in searches:
            self.driver.get(f'https://www.depop.com/search/?q={search}')
            for _ in range(10):
                self.scroll(y=600)
            results = self._get_search_results()
            for idx, result in enumerate(results):
                print(idx)
                print(result)
                if result['img'] is None:
                    continue
                self._save_product(result)
                print()

    def _get_search_results(self):
        sleep(3) # wait for imgs to load
        results = self.driver.find_elements_by_xpath('//*[@id="main"]/div[2]/div/ul/li')
        return [
            {
                'link': r.find_element_by_xpath('a').get_attribute('href'),
                'product_id': r.find_element_by_xpath('a').get_attribute('href').split('/')[-2],
                'price': r.find_element_by_xpath('div/span').text,
                'img': r.find_element_by_xpath('a/div/img').get_attribute('src')
            }
            for r in results
        ]
        
    def _save_product(self, product):

        # SAVE IMG LOCALLY
        img_ext = product['img'].split('.')[-1]
        product_folder = f'products/{product["product_id"]}'
        local_fp = f'{product_folder}/img.{img_ext}'
        if not os.path.exists('products'):
            os.mkdir('products')
        if not os.path.exists(product_folder):
            os.mkdir(product_folder)
        self.download_file(product['img'], local_fp)
        
        # SAVE IMG ON S3
        s3 = boto3.client('s3')
        s3.upload_file(local_fp, 'demo-scraper-ai-core', local_fp)

        # SAVE IMG IN DYNAMODB
        product['img'] = local_fp
        ddb = boto3.resource('dynamodb', region_name='eu-west-1')
        table = ddb.Table('demo-scraper-products')
        table.put_item(Item=product)

if __name__ == '__main__':
    # EXAMPLE USAGE
    bot = DBot(
        headless=True
    )
    # %%
    bot._scrape()
# %%
