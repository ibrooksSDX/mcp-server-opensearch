import asyncio
from OpenSearchClient import OpenSearchClient
import json


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

async def test_opensearch():
    # Initialize connector
    connector = OpenSearchClient(
        opensearch_host="localhost",
        opensearch_hostPort=9200,
        index_name="opensearch_dashboards_sample_data_ecommerce",
        bhttp_compress=True,
        buse_ssl=True,
        bverify_certs=False,
        bssl_assert_hostname=False,
        bssl_show_warn=False
    )

    # Test search
    try:
        search_results = await connector.search_documents(query)
        print("Search results:", search_results)
    except Exception as e:
        print(f"Error during search: {e}")

if __name__ == "__main__":
    asyncio.run(test_opensearch()) 