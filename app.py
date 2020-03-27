# in-built
from flask import Flask, render_template, request, jsonify, Response, session
from flask_cors import CORS, cross_origin
from urllib import parse
import json
import requests
import logging

# my-app 
from services import validations, services
from services import exceptions
import config_app




# Initialize application
application = Flask(__name__)
application.secret_key = config_app.SECRET_KEY
CORS(application)

# Intialize logger
logger = logging.getLogger(__name__)
logger.info('Flask NCBI API started.')


@application.route('/')
def homepage():
    """
    Home page for server 
    """
    return render_template("index.html")


@application.before_request
def before_request_func():
    if "queryKey" not in session.keys():
        session["queryKey"] = None
    if "webEnv" not in session.keys():
        session["webEnv"] = None



@application.route('/search/db/<database>', methods=["GET"])
@cross_origin(supports_credentials=True)
def search(database):
    """
    Handle Search Query
    
    @param database: database name
    @return: summary of search result
    """
    try:
        queryDict = validations.searchRequest(database, request.url)

        # User search meta data
        search_meta = services.eSearch(database, queryDict)
        

        # Store query key and webenv in session. webEnv will have user's search query.
        session["queryKey"] = search_meta["esearchresult"]["querykey"]
        session["webEnv"] = search_meta["esearchresult"]["webenv"] 
        session["count"] = search_meta["esearchresult"]["count"]


        # store summary data
        summary_data = services.eSummary(database, 
                        queryKey=search_meta["esearchresult"]["querykey"], 
                        webEnv=search_meta["esearchresult"]["webenv"])
        
        summary_data["count"] = search_meta["esearchresult"]["count"]

        return summary_data

    except exceptions.InvalidURLError as err:
        return Response(err.value, status=400)
    except exceptions.NcbiAPIError as err:
        return Response(err.value, status=400)
    except Exception as ae:
        print("SearchException: ",ae)
        # TODO: write error logs
        logger.exception("SearchException", str(ae))
        return Response("Flask server error: " + str(ae), status=400)


@application.route('/search/db/<database>/pg/<page>', methods=["GET"])
@cross_origin(supports_credentials=True)
def searchPagination(database, page): 
    """
    Handle Pagination

    @param database: database name
    @param page: page number to start the search
    @return: summary of search result
    """
    try:
        # store summary data
        summary_data = services.eSummary(database, queryKey=session["queryKey"], 
                            webEnv=session["webEnv"], page=page)
        summary_data["count"] = session["count"]
        return summary_data

    except exceptions.NcbiAPIError as err:
        return Response(err.value, status=400)
    except Exception as ae:
        print("PaginationException: ", ae)
        # TODO: write error logs
        logger.exception("PaginationException", str(ae))
        return Response("Flask server error: " + str(ae), status=400)



    

"""
    Initial setup for the server.
"""
if __name__ == '__main__':
    # start server
    application.run(debug=True, port=8080, host='0.0.0.0')