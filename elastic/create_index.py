from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

INDEX_NAME = "products"
mapping = {
    "mappings": {
        "properties": {
            "asin": {
                "type": "keyword"
            },
            "title": {
                "type": "text"
            },
            "product_name": {
                "type": "text"
            },
            "category_name": {
                "type": "keyword"
            },
            "price": {
                "type": "float"
            },
            "description": {
                "type": "text"
            },
            "imgUrl": {
                "type": "keyword",
                "index": False
            },
            "productURL": {
                "type": "keyword"
            },
            "file_type": {
                "type": "keyword"
            }
        }
    }
}

if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body=mapping)
    print("Index created successfully")
else:
    print("Index already exists")