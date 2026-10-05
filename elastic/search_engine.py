from elasticsearch import Elasticsearch
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "products"
PAGE_SIZE = 5
SEARCH_FIELDS = ["title", "product_name", "description"]


def search_documents(query, page=1, search_type="match", category_name=None, 
                     date_from=None, date_to=None, file_type=None, 
                     min_price=None, max_price=None):
    
    start = (page - 1) * PAGE_SIZE
    logger.info(f"Search Request: q='{query}' | category='{category_name}'")

    body = build_query(
        query=query,
        search_type=search_type,
        category_name=category_name,
        start=start,
        date_from=date_from,
        date_to=date_to,
        file_type=file_type,
        min_price=min_price,
        max_price=max_price
    )

    try:
        response = es.search(index=INDEX_NAME, body=body)
        return dict(response)
    except Exception as e:
        logger.error(f"Elasticsearch Search Error: {e}")
        raise


def build_query(query, search_type, category_name, start, 
                date_from=None, date_to=None, file_type=None, 
                min_price=None, max_price=None):
    
    if query and query.lower() != "none" and query.strip() != "":
        main_query = get_query_by_type(query, search_type)
    else:
        main_query = {"match_all": {}}

    query_body = {
        "from": start,
        "size": PAGE_SIZE,
        "query": {
            "bool": {
                "must": main_query,
                "filter": []
            }
        },
        "highlight": {
            "pre_tags": ["<mark>"],
            "post_tags": ["</mark>"],
            "fields": {
                "title": {},
                "product_name": {},
                "description": {}
            }
        }
    }

    if category_name and category_name != "All":
        query_body["query"]["bool"]["filter"].append({"term": {
            "category_name.keyword": category_name
        }})

    if file_type and file_type != "All":
        query_body["query"]["bool"]["filter"].append({"term": {"file_type": file_type.lower()}})

    if min_price or max_price:
        price_range = {}
        if min_price:
            price_range["gte"] = float(min_price)
        if max_price:
            price_range["lte"] = float(max_price)
        query_body["query"]["bool"]["filter"].append({"range": {"price": price_range}})

    return query_body


def get_query_by_type(query, search_type):
    if search_type == "phrase":
        return {"multi_match": {"query": query, "fields": SEARCH_FIELDS, "type": "phrase"}}

    elif search_type == "fuzzy":
        return {"multi_match": {"query": query, "fields": SEARCH_FIELDS, "fuzziness": "AUTO"}}

    elif search_type == "wildcard":
        return {"query_string": {"query": f"*{query}*", "fields": SEARCH_FIELDS}}

    elif search_type == "boolean":
        return {"query_string": {"query": query, "fields": SEARCH_FIELDS}}

    return {"multi_match": {"query": query, "fields": SEARCH_FIELDS}}


def get_suggestions(query):
    body = {
        "suggest": {
            "text": query,
            "simple_phrase": {
                "phrase": {
                    "field": "description",
                    "size": 1,
                    "direct_generator": [{
                        "field": "description",
                        "suggest_mode": "always"
                    }]
                }
            }
        }
    }
    try:
        response = es.search(index=INDEX_NAME, body=body)
        return dict(response)
    except Exception as e:
        logger.error(f"Suggestions Error: {e}")
        return {}


def get_total_documents():
    return es.count(index=INDEX_NAME)["count"]


def get_category_stats():
    body = {
        "size": 0,
        "aggs": {
            "file_formats": {
                "terms": {"field": "file_type"}
            }
        }
    }
    return es.search(index=INDEX_NAME, body=body)