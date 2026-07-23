import couchdb
from corpora_retrieval import gutendex_api, pmc_api, mediawiki_api


# define server_url and db name on server
server_url = couchdb.Server('http://localhost:5984/')
db = server_url['markov_chain_models']

# data entry, event management, executive assistance, financial analysis, rf cable design technician, vet tech,  needs better corpora
specialization_map = {
    'generic': [gutendex_api.RetrieveCorporaFromGutendexAPI, 100, '', ''], 
    'accounting': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Accounting'], ''], 
    'architecture': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Architecture', 'Architectural_design'], ''], 
    'auto mechanics': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Automobile_maintenance', 'Auto_mechanics'], ''], 
    'business law': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Business_law'], ''], 
    'carpentry': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Carpentry', 'Woodworking', 'Wood-related terminology'], ''], 
    'computer science': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Computer_science'], ''], 
    'data entry': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Data_management'], ''], 
    'ems': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Emergency_medical_services', 'First_aid'], ''], 
    'event planning': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Event_management'], ''], 
    'executive assistance': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Office_administration'], ''], 
    'financial analysis': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Corporate_finance', 'Financial_data_analysis', 'Financial_analysts'], ''], 
    'graphic design': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Graphic_design'], ''], 
    'marketing': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Marketing', 'Promotional_and_marketing_communications'], ''], 
    'medical transcription': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Medical_terminology'], ''], 
    'phlebotomy': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Phlebotomy', 'Blood_tests'], ''], 
    'psychology': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Psychology'], ''], 
    'rf cable design technician': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Radio_spectrum', 'Radio_technology', 'Cables', 'Signal_cables'], ''], 
    'social work': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Social_work'], ''], 
    'vet tech': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Veterinary_medicine', 'Paraveterinary_workers'], ''], 
    'web design': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Web_design'], '']
#  'medical - experimental autogen text': [pmc_api.RetrieveCorporaFromPMCAPI, 100, 'cryonics', 'Cryogenic preservation']
    }

