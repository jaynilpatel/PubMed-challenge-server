from urllib import parse
from . import ncbi_dbs


def searchRequest(database, url):
    try:
        queryDict = dict(parse.parse_qsl(parse.urlsplit(url).query))
        # check database name
        # check keywords encoded in url or not
        if database in ncbi_dbs.db_Mappings.keys() and "keywords" in queryDict.keys():
            return queryDict
        else:
            return False
    except Exception as ae:
        print(ae)
        return False

