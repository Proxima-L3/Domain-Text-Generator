"""Defined a class constructor that can retrieve and save text content from Gutendex via relevant APIs.

This module holds a class used by a code user to retrieve corpora text from Gutendex text using the gutendex APIs, 
returned text, and then save the corpora text for each book id in a dictionary class instance attribute. Takes in two arguments: one to define what search term to use for the article databases (Gutendex) used & the other to define how many articles to grab text from.

Classes:
    RetrieveCorporaFromGutendexAPI: Contains all code necessary for functionality defined above.
"""

import requests
from collections import defaultdict


class RetrieveCorporaFromGutendexAPI():
    """Contains all code necessary to make calls to relevant apis and save article corpora to corpora_dict attribute.
    
    Class constructor to make object that admin user can use to request book ids and their urls to text format from search results from a response from a fetch request for Gutendex api. Returns an object instance that has a corpora dictionary retrieved text from corresponding url only with keys as article ids and values as each book text itself.
    """

    def __init__(self, search_query: str, corpora_count: int):
        self.search_query = search_query
        self.corpora_count = corpora_count
        self.gutendex_books_api_url = f'https://gutendex.com/books?languages=en&author_year_start=1880&author_year_end=2026&copyright=false&mime_type=text%2Fplain'
        self.search_query_book_ids = []
        self.corpora_dict = defaultdict(lambda: '')

    def get_search_query_article_ids_list(self):
        """Uses gutendex api to retrieve a list of article ids regarding a no specific topic defined by the admin/code user.
        
        
        This method makes a get request to the gutendex api endpoint with relevant url params defined by class constructor argument input. If the request response is received (status code 200) then the response is converted to json format which is then iterated through to make a list of admin/code user defined number of corpora book ids and their associated urls to text docs into a list class instance attribute.
        """
        try:
            response = requests.get(str(self.gutendex_books_api_url))

            if response.status_code == 200:
                json_data = response.json()
                # use list comp to iterate through user defined corpora count to make list of id numbers
                self.search_query_book_ids = [(int(json_data['results'][i]['id']), str(json_data['results'][i]['formats']['text/plain; charset=utf-8'])) for i in range(self.corpora_count)]
                # count = 0
                # while count <= self.corpora_count - 1:
                #     self.search_query_article_ids.append(int(json_data['results'][count]['id']))
                #     count += 1
            else:
                self.search_query_book_ids = []
                # print('failed to retrieve article id data')
        except requests.exceptions.RequestException as err:
            self.search_query_book_ids = []
            return f'HTTP error occurred: {err}'
        
    def get_corpora_text(self):
        """Use gutendex api to retrieve and save article text to corpora dict.

        This method retrieves all previously defined gutendex api text_id and url to text file and saves it to corpora_dict.
        """

        try:
            for text_id_url_tuple in self.search_query_book_ids:
                # unpack current iterated tuple from list
                text_id, text_url = text_id_url_tuple
                # retrieve text from url
                text = requests.get(text_url).text
                # save text_id & text itself to corpora_dict
                self.corpora_dict[text_id] = text

        except requests.exceptions.RequestException:
            self.corpora_dict = defaultdict(lambda: '')

