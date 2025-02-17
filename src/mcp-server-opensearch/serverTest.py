import logging
from OpenSearchClient import OpenSearchClient
from fastmcp import FastMCP

#from .tools.index import IndexTools
#from .tools.document import DocumentTools
#rom .tools.cluster import ClusterTools

# TESTING VALUES 
opensearch_host="localhost"
opensearch_hostPort=9200
index_name="test_index"
http_compress=True
use_ssl=False
verify_certs=False
ssl_assert_hostname=False
ssl_show_warn=False

q = "Women's Clothing"
query = {
    'size': 5,
    'query': {
        'multi_match': {
        'query': q,
        'fields': ['category']
        }
    }
}
### END OF TESTING VALUES


class OpenSearchMCPServer:
    def __init__(self):
        self._name = "opensearch_mcp_server"
        self.mcp = FastMCP(self._name)
        
        #Configure and Establish Client to Open Search
        try:
            self._client = OpenSearchClient(opensearch_host, opensearch_hostPort, index_name, http_compress, use_ssl, verify_certs, ssl_assert_hostname, ssl_show_warn)
        except Exception as e:
            print(f"Error during search: {e}")
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self._name)
        
        # Initialize tools
        self._register_tools()

    def _testClient(self):
        self._client.search_documents(query)

    def _register_tools(self):
        """Register all MCP tools."""
        # Initialize tool classes
        #index_tools = IndexTools(self.logger)
        #document_tools = DocumentTools(self.logger)
        #cluster_tools = ClusterTools(self.logger)
        
        # Register tools from each module
        #index_tools.register_tools(self.mcp)
        #document_tools.register_tools(self.mcp)
        #cluster_tools.register_tools(self.mcp)

    def run(self):
        """Run the MCP server."""
        self.mcp.run()

def main():
    server = OpenSearchMCPServer()
    server.run()