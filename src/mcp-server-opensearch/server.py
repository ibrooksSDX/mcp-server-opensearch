import httpx
import click
import asyncio

#from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from mcp.server.fastmcp import FastMCP
from mcp.server import Server



from OpenSearchClient import OpenSearchClient

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
        'query': q,
        'fields': ['category']
        }
    }
}
### END OF TESTING VALUES

def serve(
    opensearch_host: str,
    opensearch_hostPort: str,
    index_name: str,
    http_compress: bool,
    use_ssl: bool,
    verify_certs: bool,
    ssl_assert_hostname: bool,
    ssl_show_warn: bool
) -> Server:
    """
    Instantiate the server and configure tools to store and find documents in OpenSearch.
    :param opensearch_host: The URL of the OpenSearch server.
    :param opensearch_hostPort: The port number of the OpenSearch server.
    :param index_name: The name of the index to use.
    """
    serverAPP = FastMCP("opensearch")

    opensearch = OpenSearchClient(
       opensearch_host = T_opensearch_host, opensearch_hostPort = T_opensearch_hostPort, index_name = T_index_name, bhttp_compress=T_http_compress, buse_ssl=T_use_ssl, bverify_certs=T_verify_certs, bssl_assert_hostname=T_ssl_assert_hostname, bssl_show_warn=T_ssl_show_warn
    )

    @serverAPP.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """
        Return the list of tools that the server provides. By default, there are two
        tools: one to store documents and another to find them. 
        """
        return [
            types.Tool(
                name="opensearch-find-documents",
                description=(
                    "Look up documents in OpenSearch. Use this tool when you need to: \n"
                    " - Find documents by their index or content"
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to search for in the documents",
                        },
                    },
                    "required": ["query"],
                },
            ),
        ]

    @serverAPP.call_tool()
    async def handle_tool_call(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name not in ["opensearch-find-documents"]:
            raise ValueError(f"Unknown tool: {name}")

        if name == "opensearch-find-documents":
            if not arguments or "query" not in arguments:
                raise ValueError("Missing required argument 'query'")
            query = arguments["query"]
            documents = await opensearch.search_documents(query)
            content = [
                types.TextContent(
                    type="text", text=f"Documents for the query '{query}'"
                ),
            ]
            for doc in documents:
                content.append(
                    types.TextContent(type="text", text=f"<document>{doc}</document>")
                )
            return content

    return serverAPP


@click.command()
@click.option(
    "--opensearch_host",
    envvar="OPENSEARCH_HOST",
    required=True,
    help="Open Search Host URL",
)
@click.option(
    "--opensearch_hostPort",
    envvar="OPENSEARCH_HOST_PORT",
    required=True,
    help="Open Search Port Number",
)
@click.option(
    "--index-name",
    envvar="INDEX_NAME",
    required=True,
    help="Index name",
)
def main(
    opensearch_host: str,
    opensearch_hostPort: str,
    index_name: str,
    http_compress: bool,
    use_ssl: bool,
    verify_certs: bool,
    ssl_assert_hostname: bool,
    ssl_show_warn: bool
):
    async def _run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            server = serve(
                opensearch_host,
                opensearch_hostPort,
                index_name,
                http_compress,
                use_ssl,
                verify_certs,
                ssl_assert_hostname,
                ssl_show_warn
            )
            await server.run(
                read_stream,
               write_stream,
               InitializationOptions(
                server_name="openSearch",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                       notification_options=NotificationOptions(),
                       experimental_capabilities={},
                   ),
                ),
            )
    asyncio.run(_run())