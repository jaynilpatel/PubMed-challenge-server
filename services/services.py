from . import config
from . import ncbi_dbs 
import requests
import json

def eSearch(database, queryDict):
    try:
        db = ncbi_dbs.db_Mappings[database]
        kw = queryDict["keywords"]
        kw = kw.split(" ")
        kw = "[mesh]+AND+[mesh]".join(kw)
        url = config.BASE_URL + \
            "esearch.fcgi?db={}&term={}&retmax={}&usehistory=y&retmode=json".format(
                db, kw, config.RETMAX)
        
        if "page" in queryDict["keywords"]:
            url += "&retstart={}".format(queryDict["page"])

        res = requests.get(url)
        print(res.content)
        return res
    except Exception as ae:
        print(ae)
        return False

def eSummary(database, queryKey, webEnv, page=1):
    try:
        db=ncbi_dbs.db_Mappings[database]
        retstart = config.RETMAX * (int(page)-1)
        url = config.BASE_URL + \
            "esummary.fcgi?db={}&query_key={}&WebEnv={}&retstart={}&retmax={}&retmode=json".format(
            db, queryKey, webEnv, retstart, config.RETMAX);
        print("URL: ", url)
        res = requests.get(url)
        return res
    except Exception as ae:
        print("Services Exception: ", ae)
        return False