# Search Engine Project

## Overview

This project is a mini search engine built with Flask and Elasticsearch. It allows indexing of various file formats (JSON, TXT, CSV, XLSX, PDF, DOCX) and provides search, suggestions, and statistics via a web interface.

## Project Structure

```
src/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker compose for Elasticsearch and Kibana
├── elastic/
│   ├── create_index.py         # Creates Elasticsearch index with mapping
│   ├── index_documents.py      # Handles rebuilding index and indexing files
│   └── search_engine.py        # Contains search, suggest, total docs, category stats functions
├── extractors/
│   ├── csv_extractor.py        # Extracts data from CSV files
│   ├── docx_extractor.py       # Extracts text from DOCX files
│   ├── excel_extractor.py      # Extracts data from Excel files
│   ├── json_extractor.py       # Extracts data from JSON files
│   ├── pdf_extractor.py        # Extracts text from PDF files
│   ├── txt_extractor.py        # Extracts text from TXT files
│   └── unified_extractor.py    # Unified interface to call appropriate extractor
└── templates/
    ├── index.html              # Main search interface
    └── results.html            # Results display template (if used separately)
```

## Features Implemented

### Core Functionality
- File extraction for multiple formats (JSON, TXT, CSV, XLSX, PDF, DOCX)
- Elasticsearch index creation with appropriate mapping
- Indexing and rebuilding index with selection of file formats
- Search functionality with support for different query types (match, phrase, fuzzy, wildcard, boolean)
- Filtering by category, file type, price range, and date range
- Autocomplete suggestions using Elasticsearch suggester
- Statistics: total number of documents and breakdown by file format
- Highlighting of search terms in results
- RESTful API endpoints for all functionalities
- Web interface built with HTML/CSS/JavaScript

### Architecture Components
- **Flask Application (app.py)**: Handles HTTP requests, routes, and integrates with Elasticsearch services.
- **Elasticsearch Modules**:
  - `create_index.py`: Defines index mapping and creates index if not exists.
  - `index_documents.py`: Manages index deletion/recreation and iterates over data folder to index files using appropriate extractors.
  - `search_engine.py`: Implements core search logic, query building, suggestions, total count, and category aggregations.
- **Extractor Modules**: Each file type has a dedicated extractor that returns a list of dictionaries suitable for indexing. A unified extractor dispatches to the correct one based on file extension.
- **Templates**: HTML files for the user interface.

## How to Run the Project

### Prerequisites
- Docker and Docker Compose (for Elasticsearch)
- Python 3.8 or higher
- Git (optional, for cloning)

### Step-by-Step Instructions

1. **Clone the repository** (if not already done):
   ```
   git clone https://github.com/RahmaYahiaa/Search-Engine.git
   cd Search-Engine
   ```

2. **Start Elasticsearch and Kibana using Docker Compose**:
   ```
   docker-compose up -d
   ```
   Wait a moment for Elasticsearch to be ready (you can check at `http://localhost:9200`).

3. **Install Python dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **(Optional) Index the sample data**:
   The project includes a `data` folder with sample files in various formats.
   You can index them by running:
   ```
   python elastic/index_documents.py
   ```
   When prompted, enter the file formats you want to index (e.g., `json,txt,csv,xlsx,pdf`). You can also leave it empty to index all.

   Alternatively, indexing can be triggered via the web interface (see below).

5. **Run the Flask application**:
   ```
   python app.py
   ```
   The server will start on `http://localhost:5000`.

6. **Access the web interface**:
   Open your browser and go to `http://localhost:5000`.
   You will see the search interface where you can:
   - Enter a search query
   - Select search type (match, phrase, fuzzy, wildcard, boolean)
   - Apply filters (category, file type, price range)
   - Get suggestions as you type
   - View results with highlighted terms
   - Access statistics (total documents, breakdown by file type)
   - Rebuild index with selected formats via the Index panel

### API Endpoints

All API endpoints are prefixed with `/api`.

- `GET /` : Returns the main HTML page.
- `POST /api/index/rebuild` : Rebuilds the index. Expects a JSON body with optional `formats` array (e.g., `["json","txt"]`). Returns success status and indexing summary.
- `GET /api/search` : Performs a search. Parameters:
  - `q` (string): search query
  - `page` (integer, default 1): page number for pagination
  - `type` (string, default match): search type (match, phrase, fuzzy, wildcard, boolean)
  - `category` (string): filter by category name
  - `file_type` (string): filter by file extension
  - `min_price` (number): minimum price filter
  - `max_price` (number): maximum price filter
- `GET /api/suggest` : Gets suggestions for a query. Parameter `q` (string).
- `GET /api/stats/total` : Returns total number of documents in the index.
- `GET /api/stats/categories` : Returns breakdown of documents by file type.

## Notes

- The Elasticsearch index name is `products`.
- The search highlights matching terms using the `<mark>` tag.
- The web interface uses vanilla HTML/CSS/JS with no external frameworks beyond CDN fonts.
- All file extractors return data in a format suitable for Elasticsearch indexing (list of dictionaries).
- The project does not include any authentication or security measures; it is intended for learning and demonstration purposes.
- To reset the state, you can delete the index via the rebuild endpoint or by running the index_documents script with a rebuild.

## File Format Support

| Format | Extractor | Description |
|--------|-----------|-------------|
| JSON   | json_extractor.py | Loads JSON data; each object becomes a document. |
| TXT    | txt_extractor.py | Treats entire file as one document with title as filename and description as content. |
| CSV    | csv_extractor.py | Each row becomes a document. |
| XLSX   | excel_extractor.py | Each row becomes a document (first sheet). |
| PDF    | pdf_extractor.py | Treats entire file as one document with title as filename and description as extracted text. |
| DOCX   | docx_extractor.py | Treats entire file as one document with title as filename and description as concatenated paragraph text. |

## Troubleshooting

- If Elasticsearch is not running, check Docker container status with `docker ps` and ensure ports 9200 and 5601 are free.
- If Python modules are missing, verify that `pip install -r requirements.txt` succeeded.
- If the index appears empty, ensure that data files exist in the `data` folder and that the correct file types were selected during indexing.
- For detailed logs, check the console output where Flask is running; logging is set to INFO level.

This completes the setup and usage instructions for the search engine project.