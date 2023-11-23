from elasticsearch import Elasticsearch
import json

es = Elasticsearch(["http://localhost:9200"])

#index = "image_features"
index = "features"
settings = {
  "settings": {
    "elastiknn": True,
    "number_of_shards": 1,
    "number_of_replicas": 0
  }
}

mapping = {
  "dynamic": False,
  "properties": {
      "imageId": { "type": "keyword" },
      "tags": { "type": "text" },
      "imgUrl":{"type":"text","index":False},
      "featurevector": {
          "type": "elastiknn_dense_float_vector",
          "elastiknn": {
            "dims": 795,
            "model": "lsh",
            "similarity": "l2",
            "L": 60,
            "k": 3,
            "w": 2
          }
    },
    
  }
}

# Use keyword arguments here
if not es.indices.exists(index=index):
    # The body should be an object, not a JSON string
    es.indices.create(index=index, body=settings)
    
    # Use keyword arguments and correct the body
    es.indices.put_mapping(index=index, body=mapping)

# Retrieve and print the inpdex mapping
mapping = es.indices.get_mapping(index=index)
print(mapping)
