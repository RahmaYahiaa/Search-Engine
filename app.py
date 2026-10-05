from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging

from elastic.search_engine import (
    search_documents,
    get_suggestions,
    get_total_documents,
    get_category_stats
)

from elastic.index_documents import (
    rebuild_index,
    index_all_files
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

logger.info("Flask app initialized!")

@app.route("/")
def home():
    logger.info("Home page requested")
    return render_template("index.html")


@app.route("/api/index/rebuild", methods=["POST"])
def rebuild_search_index():
    try:
        data = request.get_json() or {}
        formats = data.get(
            "formats",
            ["json", "txt", "csv", "xlsx", "pdf"]
        )

        logger.info(f"Rebuilding index with formats: {formats}")

        rebuild_index()
        summary = index_all_files(formats)

        logger.info("Index rebuild completed successfully")

        return jsonify({
            "success": True,
            "summary": summary
        })

    except Exception as e:
        logger.error(f"Rebuild index error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("q")
    page = int(request.args.get("page", 1))
    search_type = request.args.get("type", "match")
    category = request.args.get("category")
    file_type = request.args.get("file_type")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    logger.info(
        f"Search request - "
        f"query: '{query}' | "
        f"file_type: {file_type} | "
        f"price: {min_price}, To: {max_price}"
    )

    try:
        results = search_documents(
            query=query,
            page=page,
            search_type=search_type,
            category_name=category,
            file_type=file_type,
            min_price=min_price,
            max_price=max_price
        )

        total = results.get(
            "hits",
            {}
        ).get(
            "total",
            {}
        ).get(
            "value",
            0
        )

        logger.info(f"Search done - found {total} results")
        return jsonify(results)

    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/api/suggest", methods=["GET"])
def suggest():
    query = request.args.get("q")
    logger.info(f"Suggest request - query: '{query}'")

    try:
        raw_response = get_suggestions(query)
        options = raw_response.get(
            "suggest",
            {}
        ).get(
            "simple_phrase",
            []
        )

        if options and len(options[0].get("options", [])) > 0:
            suggestion = options[0]["options"][0]["text"]
            return jsonify({
                "has_suggestion": True,
                "suggestion": suggestion,
                "message": f"Did you mean: {suggestion}?"
            })
        else:
            return jsonify({
                "has_suggestion": False
            })

    except Exception as e:
        logger.error(f"Suggest error: {e}")
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/api/stats/total", methods=["GET"])
def total_docs():
    try:
        count = get_total_documents()
        return jsonify({
            "total": count
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/api/stats/categories", methods=["GET"])
def category_stats():
    try:
        result = get_category_stats()
        buckets = result.get(
            "aggregations",
            {}
        ).get(
            "file_formats",
            {}
        ).get(
            "buckets",
            []
        )
        return jsonify(buckets)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )