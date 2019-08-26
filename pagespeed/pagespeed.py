import requests
from pagespeed.responses import DesktopPageSpeed, MobilePageSpeed
import logging
import os

# make logger errors and save in to file
try:
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/info.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
except FileNotFoundError:
    print('Not found logs dir. Add...')
    os.makedirs('logs')

class PageSpeed(object):
    """Google PageSpeed analysis client

    Attributes:
        api_key (str): Optional API key for client account.
        endpoint (str): Endpoint for HTTP request
    """

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.endpoint = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'

    def analyse(self, url, filter_third_party_resources=False, screenshot=False,
                strategy='desktop'):
        """Run PageSpeed test

        Args:
            url (str): The URL to fetch and analyse.
            filter_third_party_resources (bool, optional): Indicates if third party
                resources should be filtered out before PageSpeed analysis. (Default: false)
            locale (str, optional): The locale used to localize formatted results.
            rule (list, optional): A PageSpeed rule to run; if none are given, all rules are run
            screenshot (bool, optional): Indicates if binary data containing a screenshot should
                be included (Default: false)
            strategy (str, optional): The analysis strategy to use. Acceptable values: 'desktop', 'mobile'

        """

        params = {
            'filter_third_party_resources': filter_third_party_resources,
            'screenshot': screenshot,
            'strategy': strategy,
            'url': url
        }

        strategy = strategy.lower()
        if strategy not in ('mobile', 'desktop'):
            raise ValueError('invalid strategy: {0}'.format(strategy))
        logging.info('Getting data from page speed...')
        raw = requests.get(self.endpoint, params=params)
        logging.info('Data while receive.')

        if strategy == 'mobile':
            response = MobilePageSpeed(raw)
        else:
            response = DesktopPageSpeed(raw)

        return response