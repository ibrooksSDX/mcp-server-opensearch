from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'pizzaParty123') # For testing only. Don't store credentials in code.

# Create the client with SSL/TLS and hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

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

response = client.search(
    body = query,
    index = 'opensearch_dashboards_sample_data_ecommerce'
)

print('\nSearch results:')
print(response)
