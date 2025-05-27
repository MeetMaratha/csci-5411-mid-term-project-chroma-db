from pathlib import Path
from typing import Any, Dict

from chromadb import ClientAPI, PersistentClient, QueryResult
from flask import Flask, Response, json, make_response, request
from flask_cors import CORS

app: Flask = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
CHROMA_DB_PATH: Path = Path(".", "ChromaDB")
COLLECTION_NAME: str = "zig_documentation"
chroma_client: ClientAPI = PersistentClient(path=str(CHROMA_DB_PATH))


@app.route("/get_relevant_vectors", methods=["POST"])
def getRelevantVectors() -> Response:

    request_data = request.json

    query_sentence: str = request_data["query"]
    number_of_relevant_documents: int = int(
        request_data["number_of_relevant_documents"]
    )

    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    documents: QueryResult = collection.query(
        query_texts=[query_sentence], n_results=number_of_relevant_documents
    )

    result: Dict[Any, Any] = dict(documents=dict())
    for id, document, metadata in zip(
        documents["ids"][0], documents["documents"][0], documents["metadatas"][0]
    ):
        result["documents"][id] = {"document": document, "metadata": metadata}

    return make_response(json.dumps(result), 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
