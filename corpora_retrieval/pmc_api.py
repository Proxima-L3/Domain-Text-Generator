import requests
from collections import defaultdict


# class constructor to make object that admin user can use to request meta data from search results from a response from a requests.get(url)
class RetrieveCorporaFromPMCAPI():

    # e_utils_api_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=your_search_term'
    def __init__(self, search_query: str, corpora_count: int):
        self.search_query = search_query
        self.corpora_count = corpora_count
        self.e_utils_api_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={self.search_query}[Title/Abstract]&retmax=3&retmode=json'
        self.oa_web_services_api_url = 'https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi'
        self.bioc_api_url = 'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json'
        self.search_query_article_ids = []
        self.corpora_dict = defaultdict(lambda: '')
        self.corpus_1 = ''
        self.corpus_2 = ''
        self.corpus_3 = ''

    def get_search_query_article_ids_list(self):
        response = requests.get(str(self.e_utils_api_url))

        if response.status_code == 200:
            json_data = response.json()
            # print(json_data)
            # print('\n\n\n')
            # print(response.text)
            # last_refreshed = data['Meta Data'][f'{self.corpora_count}. Last Refreshed']
            # article_ids = data['?'][last_refreshed]['?']
            # self.search_query_article_ids = article_ids
            self.search_query_article_ids = json_data['esearchresult']['idlist']
        else:
            self.search_query_article_ids = None
            print('failed to retrieve article id data')
        
    def get_corpora_text_files(self):
        # use oa web service api to download text files
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


pmc_api_object = RetrieveCorporaFromPMCAPI('psychedelics', 40)
pmc_api_object.get_search_query_article_ids_list()
pmc_api_object.get_corpora_text_files()








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