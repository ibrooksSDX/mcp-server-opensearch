# demo.py

from fastmcp import FastMCP
from OpenSearchClient import OpenSearchClient
import mcp.types as types
import asyncio
import json

mcp = FastMCP("Demo")

SLEEP_DELAY = 2

# TESTING VALUES 
T_opensearch_host="localhost"
T_opensearch_hostPort=9200
T_index_name="opensearch_dashboards_sample_data_ecommerce"
T_http_compress=True
T_use_ssl=False
T_verify_certs=False
T_ssl_assert_hostname=False
T_ssl_show_warn=False

q = "Women's Clothing"
query = {
    'size': 5,
    'query': {
        'multi_match': {
        'query': "Women's Clothing",
        'fields': ['category']
        }
    }
}
### END OF TESTING VALUES

@mcp.tool()
async def search_openSearch(query) -> list[types.TextContent] :
    client = OpenSearchClient(opensearch_host= T_opensearch_host, opensearch_hostPort=T_opensearch_hostPort, index_name=T_index_name, bhttp_compress = T_http_compress, buse_ssl = T_use_ssl, bverify_certs = T_verify_certs, bssl_assert_hostname = T_ssl_assert_hostname, bssl_show_warn = T_ssl_show_warn)
    queryresult = await client.search_documents(query)

    content = [
            types.TextContent(
                type="text", text=f"Documents for the query '{query}'"
            ),
        ]
    #for doc in queryresult:
    ##       content.append(
    #          types.TextContent(type="text", text=f"<document>{doc}</document>")
    #      )

    content.append(types.TextContent(type="text", text=f"<document>{str(queryresult)}</document>"))
    return content


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


def main():
    async def _run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            server = serve(search_openSearch)   
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="demo",
                    server_version="0.0.1",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
            await server.serve_forever()

    #asyncio.run(_run())

if __name__ == "__main__":
    asyncio.run(main()._run())