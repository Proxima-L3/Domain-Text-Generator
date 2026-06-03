"""Cleans up raw corpora text.

Uses ..[insert method/library/tools].. to clean up corpora of all bloated/unwanted pieces of text from corpora such as: escape characters like \n, urls, citations, author names, etc. And maybe punctuation and converting non ascii characters and symbols not typically able to be typed on the standard keyboard.
"""

from corpora_retrieval.pmc_api import RetrieveCorporaFromPMCAPI


# the turning of the resulting corpora retrieval object instance's corpora_dict will be put in preprocess (it will make a call to pmc_api to make an object instance then join all the values of corpora_dict attribute into a single string.. the cleaning up of the text functions/classes will come later for now)

