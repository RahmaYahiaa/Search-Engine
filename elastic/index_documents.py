import sys
import os
import json
from collections import defaultdict
from datetime import datetime
from elasticsearch import Elasticsearch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractors.json_extractor import extract_json
from extractors.txt_extractor import extract_txt
from extractors.csv_extractor import extract_csv
from extractors.excel_extractor import extract_excel
from extractors.pdf_extractor import extract_pdf

es = Elasticsearch("http://localhost:9200")

DATA_FOLDER = "data"
INDEX_NAME = "products"


def rebuild_index():
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print(f"Deleted old index: {INDEX_NAME}")

    es.indices.create(index=INDEX_NAME)
    print(f"Created new index: {INDEX_NAME}")


def index_all_files(allowed_formats):
    total_docs = 0
    stats_by_type = defaultdict(int)

    for file_name in os.listdir(DATA_FOLDER):
        ext = file_name.split('.')[-1].lower()

        if ext not in allowed_formats:
            print(f"Skipping: {file_name}")
            continue

        path = os.path.join(DATA_FOLDER, file_name)
        mod_time = os.path.getmtime(path)
        mod_date_iso = datetime.fromtimestamp(mod_time).isoformat()
        documents = []

        if ext == "json":
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            documents = data if isinstance(data, list) else [data]

        elif ext == "csv":
            documents = extract_csv(path)

        elif ext == "xlsx":
            documents = extract_excel(path)

        elif ext == "txt":
            text_content = extract_txt(path)
            documents = [{
                "title": file_name,
                "description": text_content,
                "product_name": "Plain Text File"
            }]

        elif ext == "pdf":
            text_content = extract_pdf(path)
            documents = [{
                "title": file_name,
                "description": text_content
            }]

        for doc in documents:
            doc["file_name"] = file_name
            doc["file_type"] = ext
            doc["mod_date"] = mod_date_iso
            doc["indexed_at"] = datetime.now().isoformat()

            es.index(index=INDEX_NAME, document=doc)

        docs_count = len(documents)
        total_docs += docs_count
        stats_by_type[ext] += docs_count

        print(f"Indexed {docs_count} documents from {file_name}")

    print("\n==============================")
    print("INDEX BUILD SUMMARY")
    print("==============================")
    print(f"Total Indexed Documents: {total_docs}")
    print("\nBreakdown By File Type:")

    for file_type, count in stats_by_type.items():
        print(f"{file_type}: {count}")

    print("==============================\n")

    return {
        "total_documents": total_docs,
        "breakdown": dict(stats_by_type)
    }


if __name__ == "__main__":
    print("Choose file formats to index:")
    print("Available: json, txt, csv, xlsx, pdf")

    user_input = input("Enter formats separated by commas: ").lower()
    formats_to_index = [f.strip() for f in user_input.split(',')]

    rebuild_index()
    index_all_files(formats_to_index)

    print("All files indexed successfully!")