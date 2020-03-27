# in-built
import requests
import json
import xmltodict
import logging
import sys

# my-app
from . import config
from . import exceptions


# sys.path.insert(0, '../logs/loggers')
# from logs.loggers import url_logger
import logging
logger = logging.getLogger(__name__)

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
    kw = list(map(lambda x: x + "[mesh]", kw))
    kw = "+AND+".join(kw)
    url = config.BASE_URL + \
        "esearch.fcgi?db={}&term={}&retmax={}&usehistory=y&retmode=json".format(
            db, kw, config.RETMAX)

    url = makeUrl(url, queryDict)

    # store logs
    logger.info(url)

    res = requests.get(url)
    if res.status_code != 200:
        raise exceptions.NcbiAPIError("NCBI API: Error [eSearch]")

    return res.json()
    


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

    # store logs
    logger.info(url)

    res = requests.get(url)
    if res.status_code != 200:
        raise exceptions.NcbiAPIError("NCBI API: Error [eSummary]")

    summary = res.json()

    # no results
    if "result" not in summary.keys():
        return summary

    # get abstract and add it to summary
    uids = summary["result"]["uids"]
    # initialize abstract
    for uid in uids:
        summary["result"][uid]["abstract"] = ""
    data = eFetch(database, uids)
    summary = addAbstract(data, summary, database)
        
    return summary
    



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

    # store logs
    logger.info(url)
    
    res = requests.get(url)
    if res.status_code != 200:
        raise exceptions.NcbiAPIError("NCBI API: Error [eFetch]")

    content = json.loads(json.dumps(xmltodict.parse(res.content)))

    return content


def makeUrl(url, queryDict):
    """
        Get URL after parsing queryDict.
        TODO: Need to generalize this for all database

        @param url: Base url string.
        @param queryDict: search query.
        @return: url.
    """

    # results in date range 
    if "min-date" in queryDict.keys() and "max-date" in queryDict.keys() and "datetype" in queryDict.keys():
        mindate = queryDict["min-date"].split("-")
        mindate = "/".join(mindate)
        maxdate = queryDict["max-date"].split("-")
        maxdate = "/".join(maxdate)
        if queryDict["datetype"] == "pub":
            url += "&mindate={}[pdat]&maxdate={}[pdat]".format(mindate, maxdate)
        else:
            url += "&mindate={}&maxdate={}".format(mindate, maxdate)

    # results in last nn days
    if "quick-filter" in queryDict.keys():
        url += "&reldate={}".format(queryDict["quick-filter"])
    
    # results in sort type
    if "sortBy" in queryDict.keys():
        url += "&sort={}".format(queryDict["sortBy"])

    # results for a page number 
    if "page" in queryDict["keywords"]:
        url += "&retstart={}".format(queryDict["page"])

    return url


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
    
    try:
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
                            complete_abstract += abstract_type["#text"] + " "
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
                uid = publication["BookDocument"]["PMID"]["#text"]
                
                abstract = ""
                # check if publication has abstract or not
                if summary["result"][uid]["attributes"] == ["Has Abstract"]:
                    abstract = publication["BookDocument"]["Abstract"]["AbstractText"]
                    if type(abstract) is list:
                        complete_abstract = ""
                        for abstract_type in abstract:
                            complete_abstract += abstract_type["#text"] + " "
                        abstract = complete_abstract
                    if type(abstract) is dict:
                        abstract = abstract["#text"]
                # create new key "abstract" and add value
                summary["result"][uid]["abstract"] = abstract
    
    except Exception as ae:
        print("addAbstractException: ", str(ae))
        logger.error(ae)
    return summary