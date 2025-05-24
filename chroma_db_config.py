from pprint import pprint

import chromadb

if __name__ == "__main__":
    chroma_client = chromadb.Client()

    collection = chroma_client.get_or_create_collection(name="zig_documentations")

    collection.add(
        documents=[
            "This is a document about pineapple",
            "This is a document about oranges",
        ],
        ids=["id1", "id2"],
    )

    results = collection.query(
        query_texts=["This is a query document about hawaii."], n_results=1
    )

    pprint(results)
