import click
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine

# TODO(developer): Uncomment these variables before running the sample.
# PROJECT_ID = "YOUR_PROJECT_ID"
# LOCATION = "YOUR_LOCATION" # Values: "global"
# data_store_id = "YOUR_DATA_STORE_ID"

# Examples:
# - Unstructured documents
#   - `gs://bucket/directory/file.pdf`
#   - `gs://bucket/directory/*.pdf`
# - Unstructured documents with JSONL Metadata
#   - `gs://bucket/directory/file.json`
# - Unstructured documents with CSV Metadata
#   - `gs://bucket/directory/file.csv`
# gcs_uri = "YOUR_GCS_PATH"

#  For more information, refer to:
# https://cloud.google.com/generative-ai-app-builder/docs/LOCATIONs#specify_a_multi-region_for_your_data_store



import config as c

VERTEX_AI_LOCATION = c.VERTEX_AI_LOCATION
PROJECT_ID = c.PROJECT_ID
DATASTORE_ID = c.DATASTORE_ID

@click.command()
@click.argument("gcs_uris", nargs=-1)
def refresh_datastore(gcs_uris: list[str]):


    print("gcs_uris:", list(gcs_uris))
    client_options = (
        ClientOptions(api_endpoint=f"{VERTEX_AI_LOCATION}-discoveryengine.googleapis.com")
        if VERTEX_AI_LOCATION != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/LOCATIONs/{LOCATION}/dataStores/{data_store_id}/branches/{branch}
    parent = client.branch_path(
        project=PROJECT_ID,
        location=VERTEX_AI_LOCATION,
        data_store=DATASTORE_ID,
        branch="default_branch",
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        gcs_source=discoveryengine.GcsSource(
            # Multiple URIs are supported
            input_uris=list(gcs_uris),
            # Options:
            # - `content` - Unstructured documents (PDF, HTML, DOC, TXT, PPTX)
            # - `custom` - Unstructured documents with JSONL metadata
            # - `csv` - Unstructured documents with CSV metadata
            data_schema="content",
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    print(response)
    print(metadata)


if __name__ == "__main__":
    refresh_datastore()
