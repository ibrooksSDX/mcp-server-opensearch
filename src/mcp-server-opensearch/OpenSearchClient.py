import os
import asyncio
import json
from fastmcp import FastMCP

from opensearchpy import OpenSearch
host = 'localhost'
port = 9200

def get_string_list_from_json(json_data):
    """Extracts a list of strings from a JSON object."""

    if isinstance(json_data, list):
        return [item for item in json_data if isinstance(item, str)]
    elif isinstance(json_data, dict):
        return [value for value in json_data.values() if isinstance(value, str)]
    else:
        return []


class OpenSearchClient:
    def __init__(
        self,
        opensearch_host: str,
        opensearch_hostPort: str,
        index_name: str,
        bhttp_compress: bool,
        buse_ssl: bool,
        bverify_certs: bool,
        bssl_assert_hostname: bool,
        bssl_show_warn: bool
    ):
        self._index_name = index_name,
        self._host = [{'host':  opensearch_host, 'port': opensearch_hostPort}],
        self._auth =('admin', 'pizzaParty123'),
        self._client = OpenSearch(hosts = [{'host': host, 'port': port}], http_compress = bhttp_compress, http_auth = ('admin', 'pizzaParty123') , use_ssl = buse_ssl, verify_certs = bverify_certs, ssl_assert_hostname = bssl_assert_hostname, ssl_show_warn = bssl_show_warn)
    
    async def search_documents(self, query: str) -> list[str]:
        """
        Find documents in the OpenSearch index. If there are no documents found, an empty list is returned.
        :param query: The query to use for the search.
        :return: A list of documents found.
        """
        index_exists = self._client.indices.exists(index=self._index_name)
        if not index_exists:
           return []
        search_results = self._client.search(
            body=query,
           index = self._index_name
        )
        #search_results_json = json.loads(search_results, indent=4)
        #print(search_results_json)
        #return search_results
    
        return search_results

   
    def _return_client(self) -> OpenSearch:
        """Create and return an OpenSearch client using configuration from environment."""
        return self._client
