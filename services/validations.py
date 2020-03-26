from urllib import parse
from . import config

def searchRequest(database, url):
    """
        Validate request @ ../search/db/<database>.
        
        @param database: name of database.
        @param url: url to be validated. ie. request.url
        @return: dict of query.
    """

    try:
        queryDict = dict(parse.parse_qsl(parse.urlsplit(url).query))
        # check database name
        # check keywords encoded in url or not
        if database in config.DB_MAPPING.keys() and "keywords" in queryDict.keys():
            return queryDict
        else:
            return False
    except Exception as ae:
        print(ae)
        return False

