from flask import Flask, render_template, request, jsonify, Response, session
from flask_cors import CORS, cross_origin
from urllib import parse
from services import validations, services

import json
import requests
import config_app



"""
    Initialize application
"""
application = Flask(__name__)
application.secret_key = config_app.SECRET_KEY
CORS(application)



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
    """

    queryDict = validations.searchRequest(database, request.url)
    if not queryDict:
        return Response("NCBI: Invalid URL encodings", status=400)

    else:

        # User search meta data
        search_meta, status_code = services.eSearch(database, queryDict)
        if status_code != 200:
            return Response("NCBI: API error [eSearch]", status=status_code)
        

        # Store query key and webenv in session. webEnv will have user's search query.
        session["queryKey"] = search_meta["esearchresult"]["querykey"]
        session["webEnv"] = search_meta["esearchresult"]["webenv"] 
        session["count"] = search_meta["esearchresult"]["count"]


        # store summary data
        summary_data, status_code = services.eSummary(database, 
                        queryKey=search_meta["esearchresult"]["querykey"], 
                        webEnv=search_meta["esearchresult"]["webenv"])
        if status_code != 200:
            return Response("NCBI: API error [eSummary]", status=status_code)
        summary_data["count"] = search_meta["esearchresult"]["count"]


    return summary_data




@application.route('/search/db/<database>/pg/<page>', methods=["GET"])
@cross_origin(supports_credentials=True)
def searchPagination(database, page): 
    """
    Handle Pagination
    """
    
    # store summary data
    summary_data, status_code = services.eSummary(database, queryKey=session["queryKey"], 
                        webEnv=session["webEnv"], page=page)
    if status_code != 200:
            return Response("NCBI: API error [eSummary]", status=status_code)
     
    summary_data["count"] = session["count"]
    return summary_data



"""
    Initial setup for the server.
"""
if __name__ == '__main__':

    # start server
    application.run(debug=True, port=8080, host='0.0.0.0')