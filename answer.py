import os
import re
from urllib.parse import quote

from pprint import pprint as pp
from google.cloud import discoveryengine_v1 as discoveryengine
from google.api_core.client_options import ClientOptions

import config as c

VERTEX_AI_LOCATION = c.VERTEX_AI_LOCATION
PROJECT_ID = c.PROJECT_ID
DATASTORE_ID = c.DATASTORE_ID

MODEL_VERSION = c.MODEL_VERSION

client_options = (
    ClientOptions(api_endpoint=f"{VERTEX_AI_LOCATION}-discoveryengine.googleapis.com")
    if VERTEX_AI_LOCATION != "global"
    else None
)
search_client = discoveryengine.ConversationalSearchServiceClient(
    client_options=client_options
)

PREAMBLE = c.PREAMBLE

doc_cache: dict = {}


def query(
    query_text: str,
    session_id: str = "-"
) -> discoveryengine.types.conversational_search_service.AnswerQueryResponse:
    query = discoveryengine.Query()
    query.text = query_text

    request = discoveryengine.AnswerQueryRequest(
        serving_config=f"projects/{PROJECT_ID}/locations/global/collections/default_collection/dataStores/{DATASTORE_ID}/servingConfigs/default_serving_config",
        query=query,
        asynchronous_mode=False,
        query_understanding_spec=discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec(
            query_rephraser_spec=discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec.QueryRephraserSpec(
                max_rephrase_steps=3,
                disable=False,
            ),
        ),
        search_spec=discoveryengine.AnswerQueryRequest.SearchSpec(
            search_params=discoveryengine.AnswerQueryRequest.SearchSpec.SearchParams(
                max_return_results=3,
            )
        ),
        answer_generation_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec(
            model_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.ModelSpec(
                model_version=MODEL_VERSION,
            ),
            prompt_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.PromptSpec(
                preamble=PREAMBLE,
            ),
            include_citations=True,
            ignore_low_relevant_content=True,
            ignore_non_answer_seeking_query=True,
        ),
        session=f"projects/{PROJECT_ID}/locations/global/collections/default_collection/dataStores/{DATASTORE_ID}/sessions/{session_id}",
    )

    response = search_client.answer_query(request=request)

    return response

def render_response(response):
    answer = response.answer.answer_text
    answer_with_citations = ""
    citations = []
    all_ids = []
    end_index_pre = 0
    try:
        for item in response.answer.citations:
            start_index = item.start_index
            end_index = item.end_index + 1
            # sources = item.sources
            ids = []
            for source in item.sources:
                ids.append(int(source.reference_id)+1)
                all_ids.append(int(source.reference_id)+1)
            answer_with_citations += "".join([
                answer[end_index_pre:start_index],
                answer[start_index:end_index],
                str(ids),
            ])
            end_index_pre = end_index
        answer_with_citations += answer[end_index_pre:]

        for c, item in enumerate(response.answer.references):
            if c+1 in all_ids:
                chunk = item.chunk_info.content
                title = item.chunk_info.document_metadata.title
                citation = {
                    "title": f"{title}",
                    "preview": f"{chunk[:50]}",
                    "url": get_doc_uri(item.chunk_info.document_metadata.document)
                }
                citations.append(citation)
    except Exception as e:
        print(e)

    return answer_with_citations, citations

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
            bucket_and_blob = f"match.group(1)/match.group(2)"
            encoded_bucket_and_blob = quote(bucket_and_blob)
            return f"https://storage.cloud.google.com/{encoded_bucket_and_blob}"
    else:
        print(f"{gcs_path} can NOT be converted")
        return ""
