"""
    Base url of the NCBI API.
"""
BASE_URL= "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

"""
    Number of results to retreive
"""
RETMAX=20

"""
    Contains mappings for database which is requested from client to the database on NCBI server.
"""
DB_MAPPING = {
    # from client: db_name at NCBI
    "PubMed_DB": "pubmed"
}
