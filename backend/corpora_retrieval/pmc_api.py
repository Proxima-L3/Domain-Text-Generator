"""Defined a class constructor that can retrieve and save article content from PMC via relevant APIs.

This module holds a class used by a code user to retrieve corpora text from PMC articles using the e-utilities esearch and efetch APIs, can clean up the returned xml response, and then save the corpora text for each article in a dictionary class instance attribute. Takes in two arguments: one to define what search term to use for the article databases (PMC) used & the other to define how many articles to grab text from.

Classes:
    RetrieveCorporaFromPMCAPI: Contains all code necessary for functionality defined above.
"""

import requests
import xml.etree.ElementTree
from io import StringIO
from collections import defaultdict


class RetrieveCorporaFromPMCAPI():
    """Contains all code necessary to make calls to relevant apis and save article corpora to corpora_dict attribute.
    
    Class constructor to make object that admin user can use to request article ids from search results from a response from a requests.get(url) for PubMedCentral (PMC) apis. Returns an object instance that has a corpora dictionary retrieved and parsed to text only with keys as article ids and values as each article text itself.
    """

    def __init__(self, search_query: str, corpora_count: int):
        self.search_query = search_query
        self.corpora_count = corpora_count
        self.e_utils_esearch_api_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={self.search_query}[Title/Abstract]&retmax={self.corpora_count}&retmode=json'
        self.e_utils_efetch_api_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc'
        self.search_query_article_ids = []
        self.corpora_dict = defaultdict(lambda: '')

    def get_search_query_article_ids_list(self):
        """Uses e-utilities esearch api to retrieve a list of article ids regarding a specific topic defined by the admin/code user.
        
        This method makes a get request to the e-utils esearch api endpoint with relevant url params defined by class constructor argument input. If the request response is received (status code 200) then the response is converted to json format which is then indexed to make a list of admin/code user defined number of articles into a list class instance attribute
        """
        try:
            response = requests.get(str(self.e_utils_esearch_api_url))

            if response.status_code == 200:
                json_data = response.json()
                self.search_query_article_ids = json_data['esearchresult']['idlist']
            else:
                self.search_query_article_ids = []
                # print('failed to retrieve article id data')
        except requests.exceptions.RequestException as err:
            self.search_query_article_ids = []
            return f'HTTP error occurred: {err}'
        
    def get_corpora_text(self):
        """Use e-utilities efetch api to retrieve, parse, and save article text to corpora dict.

        This method appends all efetch api specified url params to the url that will be used in a requests.get() to retrieve all articles with matching ids previously defined in get_search_article_ids_list. It then uses the ElementTree xml library to parse through the xml response and grab only relevant article text by separating the response into a temp dictionary with article ids as keys and article element node content (including their child elements) as values. The article nodes are then parsed through to grab only relevant tags that contain the text wanted and loops through to remove unwanted child tags before finally saving each article node text content to corpora_dict.
        """

        try:
            # if id list is >= 200 then append all ids from id list to efetch_endpoint_url_params string (must use http post request if over 200)
            efetch_endpoint_url_params = '&id='
            for article_id in self.search_query_article_ids:
                # print(article_id)
                efetch_endpoint_url_params += f'{article_id}'
                if article_id == self.search_query_article_ids[-1]:
                    pass
                else:
                    efetch_endpoint_url_params += ','
            
            efetch_endpoint_url_params += '&retmode=xml'

            # retrieve efetch api xml response
            xml_response = requests.get(str(f'{self.e_utils_efetch_api_url}{efetch_endpoint_url_params}'))

            # parse xml response with builtin python xml parsing api:
            # after saving xml response as parsed text use for loop that iterates through xml response root to find and separate all articles at their dom node level before finding all title, p, and td tags. Then saving them to a temp dictionary then loops through to remove unwanted tags and return a cleaned up article list with just the desired text content which is then conjoined into a string then saved to corpora_dict.

            xml_response_tree = xml.etree.ElementTree.parse(StringIO(xml_response.text))
            xml_response_root = xml_response_tree.getroot()

            temp_dict = defaultdict(lambda: '')
            temp_index = 0
            for article_node in xml_response_root.findall('article'):
                temp_dict[self.search_query_article_ids[temp_index]] = article_node
                temp_index += 1
            
            temp_index = 0
            for temp_dict_key in temp_dict:
                # find all content in title, p, and td tags and conjoin into a list
                temp_list_of_elements = temp_dict[temp_dict_key].findall('.//title') + temp_dict[temp_dict_key].findall('.//p') + temp_dict[temp_dict_key].findall('.//td')

                # exclude unwanted text from each title, p, and td tag content
                unwanted_tags = ['xref', 'sub', 'sup']
                for element in temp_list_of_elements:
                    for tag in unwanted_tags:
                        for unwanted in element.findall('.//' + tag):
                            # preserve tail end text before removing
                            if unwanted.tail:
                                parent = element
                                parent_text = parent.text or ''
                                parent.text = parent_text + (unwanted.tail or '')
                            if unwanted in element:
                                element.remove(unwanted)
                
                # cleaned up list then removes all tags so its just a list of text strings
                text_only_cleaned_list = [' '.join(element.itertext()) for element in temp_list_of_elements]
                # list of text strings is then joined to single string before being saved to corpora_dict
                article_text_cleaned = ' '.join(text_only_cleaned_list)
                self.corpora_dict[self.search_query_article_ids[temp_index]] = article_text_cleaned

                temp_index += 1
        except requests.exceptions.RequestException:
            self.corpora_dict = defaultdict(lambda: '')

