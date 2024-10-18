import re
from urllib.parse import quote

from google.cloud import storage
from google.cloud import discoveryengine_v1 as discoveryengine
import config as c


doc_cache = {}
def get_doc_uri(doc_id: str) -> str:
    if doc_id in doc_cache:
        print("take doc id from cache")
        return doc_cache[doc_id]

    client = discoveryengine.DocumentServiceClient()
    request = discoveryengine.GetDocumentRequest(
        name=doc_id,
    )
    response = client.get_document(request=request)
    uri = gcs_path_to_url(response.content.uri)
    doc_cache[doc_id] = uri
    return uri

def gcs_path_to_url(gcs_path: str) -> str:
    match = re.match(r"^gs://([^/]+)/(.*)$", gcs_path)
    if match:
        if c.RETRIEVAL_FILE_URL:
            blob = match.group(2)
            encoded_blob = quote(blob)
            return f"{c.RETRIEVAL_FILE_URL}/{encoded_blob}"
        else:
            bucket_and_blob = f"{match.group(1)}/{match.group(2)}"
            encoded_bucket_and_blob = quote(bucket_and_blob)
            return f"https://storage.cloud.google.com/{encoded_bucket_and_blob}"
    else:
        print(f"{gcs_path} can NOT be converted")
        return ""

if __name__ == "__main__":
    import sys
    gcs_path = sys.argv[1]
    url = gcs_path_to_url(gcs_path)
    print(url)
