from elasticsearch import Elasticsearch

# Create a connection to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# # Index name you want to delete
index_name = "features"

# # Delete the index
# response = es.indices.delete(index=index_name, ignore=[400, 404])

# print(response)





# Get list of all indexes
# indices = es.cat.indices(index='*', h='index', s='index')
# print(indices)

count = es.count(index=index_name)

# The count is in the 'count' field of the response
print(f"The index '{index_name}' contains {count['count']} documents.")
