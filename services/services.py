from . import config

import requests
import json
import xmltodict

"""
    Complete documentation for NCBI API: 
    https://www.ncbi.nlm.nih.gov/books/NBK25498/#chapter3.ESearch__ESummaryEFetch
"""



def eSearch(database, queryDict):
    """
    Get meta-data for the search query. Use to fetch Count, WebEnv & ID list.

    @param database: name of database.
    @param queryDict: search query.
    @return: response, status code.
    """
   
    db = config.DB_MAPPING[database]
    kw = queryDict["keywords"]
    kw = kw.split(" ")
    kw = "[mesh]+AND+[mesh]".join(kw)
    url = config.BASE_URL + \
        "esearch.fcgi?db={}&term={}&retmax={}&usehistory=y&retmode=json".format(
            db, kw, config.RETMAX)
    print("URL: ", url)
    if "page" in queryDict["keywords"]:
        url += "&retstart={}".format(queryDict["page"])

    res = requests.get(url)

    return res.json(), res.status_code
    


def eSummary(database, queryKey, webEnv, page=1):
    """
    Get search result summary for a given query.
    
    @param database: name of database.
    @param queryDict: search query.
    @param webEnv: webEnv token for a given eSearch.
    @param page: page number to start search from. Default page 1.
    @return: response, status code.
    """

    db = config.DB_MAPPING[database]
    retstart = config.RETMAX * (int(page)-1)
    url = config.BASE_URL + \
        "esummary.fcgi?db={}&query_key={}&WebEnv={}&retstart={}&retmax={}&retmode=json".format(
        db, queryKey, webEnv, retstart, config.RETMAX);
    print("URL: ", url)
    res = requests.get(url)
    summary = res.json()

    # no results
    if "result" not in summary.keys():
        return summary, res.status_code

    # get abstract and add it to summary
    uids = summary["result"]["uids"]
    data, _ = eFetch(database, uids)
    summary = addAbstract(data, summary, database)
        
    return summary, res.status_code
    


# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=abstract&retmode=xml&id=32207519,32207584
def eFetch(database, ids):
    """
    Get complete information of documents.
    
    @param database: name of database.
    @param ids: list of ids.
    @return: response, status code.
    """
    
    db = config.DB_MAPPING[database]
    ids = ",".join(ids)
    url = config.BASE_URL + \
            "efetch.fcgi?db={}&rettype=abstract&retmode=xml&id={}".format(
                db, ids)
    print("URL eFetch: ", url)
    res = requests.get(url)
    content = json.loads(json.dumps(xmltodict.parse(res.content)))

    return content, res.status_code


def addAbstract(data, summary, database):
    """
        Get abstract only for PubMed database.
        TODO: Need to generalize this for all database

        @param data: response from eFetch.
        @param summary: resposne from eSummary.
        @param database: name of database.
        @return: summary with abstract.
    """
    # Return if db not PubMed.
    if database != "PubMed_DB":
        return summary
    
    # For PubmedArticles
    if "PubmedArticle" in data["PubmedArticleSet"].keys():
        publications = data["PubmedArticleSet"]["PubmedArticle"]
        for publication in publications:
            uid = publication["MedlineCitation"]["PMID"]["#text"]
            abstract = ""
            # check if publication has abstract or not
            if summary["result"][uid]["attributes"] == ["Has Abstract"]:
                abstract = publication["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
                if type(abstract) is list:
                    complete_abstract = ""
                    for abstract_type in abstract:
                        complete_abstract += abstract_type["#text"]
                    # print("Complete_abstract: ", complete_abstract)
                    abstract = complete_abstract
                if type(abstract) is dict:
                    abstract = abstract["#text"]
            # create new key "abstract" and add value
            summary["result"][uid]["abstract"] = abstract

    # For PubMedBookArticle
    if "PubmedBookArticle" in data["PubmedArticleSet"].keys():
        publications = data["PubmedArticleSet"]["PubmedBookArticle"]
        if type(publications) == dict:
            publications = [publications] 
        if not publication:
            return summary
        for publication in publications:
            try:
                uid = publication["BookDocument"]["PMID"]["#text"]
            except Exception as ae:
                print(ae, publication.keys())
            abstract = ""
            # check if publication has abstract or not
            if summary["result"][uid]["attributes"] == ["Has Abstract"]:
                abstract = publication["BookDocument"]["Abstract"]["AbstractText"]
                if type(abstract) is list:
                    complete_abstract = ""
                    for abstract_type in abstract:
                        complete_abstract += abstract_type["#text"]
                    # print("Complete_abstract: ", complete_abstract)
                    abstract = complete_abstract
                if type(abstract) is dict:
                    abstract = abstract["#text"]
            # create new key "abstract" and add value
            summary["result"][uid]["abstract"] = abstract
    
    return summary