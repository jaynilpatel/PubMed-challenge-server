from urllib import parse

# my-app
from . import config
from . import exceptions

def searchRequest(database, url):
    """
        Validate request @ ../search/db/<database>.
        
        @param database: name of database.
        @param url: url to be validated. ie. request.url
        @return: dict of query.
    """

    # https://stackoverflow.com/questions/21584545/url-query-parameters-to-dict-python
    queryDict = dict(parse.parse_qsl(parse.urlsplit(url).query))

    # check database name and
    # check keywords encoded in url or not
    if database in config.DB_MAPPING.keys() and "keywords" in queryDict.keys():
        return queryDict
    else:
        raise(exceptions.InvalidURLError("InvalidURLError: Please specify keywords in the URL"))
    