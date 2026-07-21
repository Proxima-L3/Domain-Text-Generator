"""Defined a class constructor that can retrieve and save text content from MediaWiki via relevant APIs.

This module holds a class used by a code user to retrieve corpora text from MediaWiki text using the MediaWiki APIs, 
returned text, and then save the corpora text for each article id in a dictionary class instance attribute. Takes in two arguments: one to define what search term to use for the article databases (MediaWiki) used & the other to define how many articles to grab text from.

Classes:
    RetrieveCorporaFromMediaWikiAPI: Contains all code necessary for functionality defined above.
"""

import requests
from collections import defaultdict


class RetrieveCorporaFromMediaWikiAPI():
    """Contains all code necessary to make calls to relevant apis and save article corpora to corpora_dict attribute.
    
    Class constructor to make object that admin user can use to request article ids and then request article in text format from search results from a response from a fetch request for MediaWiki api. Returns an object instance that has a corpora dictionary retrieved text from corresponding url only with keys as article ids and values as each article text itself.
    """

    def __init__(self, search_query_categories: list, corpora_count: int):
        self.search_query_categories = search_query_categories
        self.corpora_count = corpora_count
        self.mediawiki_get_article_ids_by_categories_url = f'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtype=page&cmlimit={corpora_count}&format=json'
        self.mediawiki_get_article_text_api_url = f'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=true&format=json'
        self.request_headers = {'User-Agent': 'DomainTextGenerator/1.0 (proximal3dev@gmail.com)'}
        self.search_query_article_ids = []
        self.corpora_dict = defaultdict(lambda: '')

    def get_search_query_article_ids_list(self):
        """Uses MediaWiki api to retrieve a list of article ids or titles regarding a no specific topic defined by the admin/code user.
        
        
        This method makes a get request to the MediaWiki api endpoint with relevant url params defined by class constructor argument input. If the request response is received (status code 200) then the response is converted to json format which is then iterated through to make a list of admin/code user defined number of corpora article ids and their associated urls to text docs into a list class instance attribute.
        """
        try:
            # use for loop to iterate through categories list to return results of all pages within each category then grab each of their titles and add them to search_query_article_titles
            for category in self.search_query_categories:
                response = requests.get(f'{self.mediawiki_get_article_ids_by_categories_url}&cmtitle=Category:{category}', headers=self.request_headers)
                print(response.status_code)

                if response.status_code == 200:
                # maybe have conditional that checks for each category if object after categorymembers is a list (more than 100 page results) or an int (100 or less results) ...(do this conditional because if its over 100 page results the returned json is different and has another layer so to index it it would be a nested for loop like: for page_list in json_data['query']['categorymembers']: (then a for loop for each page in page_list like: for page in page_list: (then append page id to search_query_article_ids list) ). if its 100 or less then the for loop is simpler like: (for page in json_data['query']['categorymembers'][i]['pageid']) then append pageid value to search_query_article_ids. )...   ....(or not because my browser tricked me and apparently the list vs int being returned at that json's index is always just one list row/key with values of dictionaries)....

                    json_data = response.json()

                    # if isinstance(json_data['query']['categorymembers'], list):
                    #     for pageid_list in json_data['query']['categorymembers']:
                    #         for result in pageid_list:
                    #             self.search_query_article_ids.append(result['pageid'])
                    # elif isinstance(json_data['query']['categorymembers'], int):
                    #     # use list comp to iterate through returned json to make list of id numbers
                    #     self.search_query_article_ids.extend([str(json_data['query']['categorymembers'][i]['pageid']) for i in range(len(json_data['query']['categorymembers']))])

                    self.search_query_article_ids.extend([item['pageid'] for item in json_data['query']['categorymembers']])
                else:
                    # self.search_query_article_titles.append()
                    print('failed to retrieve article category data')
        except requests.exceptions.RequestException as err:
            self.search_query_article_ids = []
            return f'HTTP error occurred: {err}'
        
    def get_corpora_text(self):
        """Use MediaWiki api to retrieve and save article text to corpora dict.

        This method retrieves all previously defined MediaWiki api article's text by id and saves it to corpora_dict.
        """

        try:
            # get article text for every article title in article list attribute
            for article_id in self.search_query_article_ids:

                # get returned json data for specified article id
                response = requests.get(f'{self.mediawiki_get_article_text_api_url}&pageids={article_id}', headers=self.request_headers)
                if response.status_code == 200:
                    json_data = response.json()
                    # retrieve text from response json
                    text = json_data['query']['pages'][str(article_id)]['extract']
                    # save text_id & text itself to corpora_dict
                    self.corpora_dict[article_id] = text

        except requests.exceptions.RequestException:
            self.corpora_dict = defaultdict(lambda: '')



