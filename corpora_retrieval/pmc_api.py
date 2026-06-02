import requests
from collections import defaultdict
import xml.dom.minidom
import xml.etree.ElementTree
from io import StringIO


# class constructor to make object that admin user can use to request meta data from search results from a response from a requests.get(url) for PubMedCentral (PMC) apis. returns an object instance that has a corpora dictionary retrieved and parsed 
class RetrieveCorporaFromPMCAPI():

    def __init__(self, search_query: str, corpora_count: int):
        self.search_query = search_query
        self.corpora_count = corpora_count
        self.e_utils_esearch_api_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={self.search_query}[Title/Abstract]&retmax=3&retmode=json'
        self.e_utils_efetch_api_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc'
        self.oa_web_services_api_url = 'https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi'
        self.bioc_api_url = 'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json'
        self.search_query_article_ids = []
        self.corpora_dict = defaultdict(lambda: '')
        # self.corpus_1 = ''
        # self.corpus_2 = ''
        # self.corpus_3 = ''

    def get_search_query_article_ids_list(self):
        response = requests.get(str(self.e_utils_esearch_api_url))

        if response.status_code == 200:
            json_data = response.json()
            # print(json_data)
            # print('\n\n\n')
            # print(response.text)
            # last_refreshed = data['Meta Data'][f'{self.corpora_count}. Last Refreshed']
            # article_ids = data['?'][last_refreshed]['?']
            # self.search_query_article_ids = article_ids
            self.search_query_article_ids = json_data['esearchresult']['idlist']
            # print(self.search_query_article_ids)
        else:
            self.search_query_article_ids = None
            print('failed to retrieve article id data')
        
    def get_corpora_text(self):
        # use e-utilities efetch api to retrieve, parse, and download text files
        
        # create string to append to base eutils efetch api endponit url
        # idlist in param form

        # if id list is >= 200 then append all ids from id list to efetch_endpoint_url_params string (must use http post request if over 200)
        efetch_endpoint_url_params = '&id='
        for article_id in self.search_query_article_ids:
            print(article_id)
            efetch_endpoint_url_params += f'{article_id}'
            if article_id == self.search_query_article_ids[-1]:
                pass
            else:
                efetch_endpoint_url_params += ','
        
        efetch_endpoint_url_params += '&retmode=xml'

        # retrieve efetch api xml response
        xml_response = requests.get(str(f'{self.e_utils_efetch_api_url}{efetch_endpoint_url_params}'))

        # parse xml response with builtin python xml parsing api
        # print(xml.dom.minidom.parseString(xml_response.text).toprettyxml())
        # with open('sample_corporaxml.xml', 'w', encoding='utf-8') as f:
        #     f.write(xml.dom.minidom.parseString(xml_response.text).toprettyxml())

        # for tag_item in xml_response

        # for loop that iterates through element tree to 
            # find/separate articles at their dom node level
            # before finding all title, p, and td tags
            # grab just their text
            # and append/conjoin it all to a string
            # add string to corpora_dict as value with keys being each article id
        xml_response_tree = xml.etree.ElementTree.parse(StringIO(xml_response.text))
        xml_response_root = xml_response_tree.getroot()
        # article_xml_list = []
        # article_xml_list = [article_node for article_node in xml_response_root.findall('article')]

        temp_dict = defaultdict(lambda: '')
        temp_index = 0
        for article_node in xml_response_root.findall('article'):

            temp_dict[self.search_query_article_ids[temp_index]] = article_node
            temp_index += 1
        
        temp_index = 0
        for temp_dict_key in temp_dict:
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
            # unwanted_element_cleaned_list = temp_list_of_elements
            text_only_cleaned_list = [' '.join(element.itertext()) for element in temp_list_of_elements]
            article_text_cleaned = ' '.join(text_only_cleaned_list)
            self.corpora_dict[self.search_query_article_ids[temp_index]] = article_text_cleaned

            temp_index += 1
        
        print(self.corpora_dict)
        print(len(self.corpora_dict))

        






    def get_corpora_text_files_bioc(self):
        # use BioC api to download text files
        for article_id in self.search_query_article_ids:
            
            response = requests.get(f'{self.bioc_api_url}/PMC{article_id}/unicode')

            if response.status_code == 200:

                try:
                    article_passages = response.json()[0]['documents'][0]['passages']
                    joined_passage_text_strs = ''

                    # print('\n\n\n')
                    # print(article_passages)


                    # for section in article_passages:
                    #     for subitem in section:
                    #         print('\n\n\n')
                    #         print(subitem)
                    #         nested_text = subitem['text']
                    #         joined_passage_text_strs.append(f' {nested_text}')

                    for sub_passage in article_passages:
                        print('\n\n\n')
                        print(sub_passage)
                        nested_text = sub_passage['text']
                        joined_passage_text_strs += f' {nested_text}'
                    
                    deeply_nested_article_text = joined_passage_text_strs
                    self.corpora_dict[article_id] = deeply_nested_article_text
                    # print('\n\n\n')
                    # print(response.json())
                    # print('\n\n\n')
                    # print(deeply_nested_article_text)
                except requests.exceptions.JSONDecodeError:
                    print(f'Article PMC{article_id} not available as JSON — skipping')
                    continue
            else:
                print('failed to retrieve article text data')

        for text in self.corpora_dict:
            print(len(self.corpora_dict))
            print('\n\n\n')


pmc_api_object = RetrieveCorporaFromPMCAPI('psychedelics', 3)
pmc_api_object.get_search_query_article_ids_list()
pmc_api_object.get_corpora_text()








""" 
This is what response.json() returns:

{
    'header': {
        'type': 'esearch',
        'version': '0.3'
        },
    'esearchresult': {
        'count': '1282',
        'retmax': '3',
        'retstart': '0',
        'idlist': ['13202413', '12169207', '12169204'],
        'translationset': [],
        'querytranslation': '"psychedelics"[Title/Abstract]'
        }
    }

    



This is what response.text returns:

{"header":{"type":"esearch","version":"0.3"},"esearchresult":{"count":"1282","retmax":"3","retstart":"0","idlist":["13202413","12169207","12169204"],"translationset":[],"querytranslation":"\"psychedelics\"[Title/Abstract]"}}

"""