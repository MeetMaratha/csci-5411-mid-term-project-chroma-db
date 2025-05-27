import os
from typing import Dict, List
from uuid import uuid4

from boto3 import client
from chromadb import ClientAPI, Collection, PersistentClient

CHROMA_DB_PATH: str = os.path.join(".", "ChromaDB")
COLLECTION_NAME: str = "zig_documentation"
QUERY_URL: str = "https://sqs.us-east-1.amazonaws.com/123456789012/your-queue"


def processMessage(collection: Collection, message: Dict) -> None:
    chunks: List[str] = message["Body"]["chunks"]
    ids: List[str] = [str(uuid4()) for _ in range(len(chunks))]
    collection.add(documents=chunks, ids=ids)
    return None


if __name__ == "__main__":
    chroma_client: ClientAPI = PersistentClient(path=CHROMA_DB_PATH)
    collection: Collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )
    sqs_client = client(service_name="sqs", region_name="us-east-1")

    while True:
        try:
            response = sqs_client.receive_message(
                QueueUrl=QUERY_URL, MaxNumberOfMessages=10, WaitTimeSeconds=20
            )

            if "Messages" in response:
                for message in response["Messages"]:
                    processMessage(message)
        except Exception as e:
            print(f"ERROR: Error occured!!")
            print(e)
