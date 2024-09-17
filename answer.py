import os
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
                disable=False,
                max_rephrase_steps=5,
            ),
        ),
        search_spec=discoveryengine.AnswerQueryRequest.SearchSpec(
            search_params=discoveryengine.AnswerQueryRequest.SearchSpec.SearchParams(
                max_return_results=5,
            )
        ),
        answer_generation_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec(
            model_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.ModelSpec(
                model_version=MODEL_VERSION,
            ),
            prompt_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.PromptSpec(
                preamble="箇条書きで回答してください。"
            ),
            include_citations=True,
            ignore_low_relevant_content=True,
            ignore_non_answer_seeking_query=True,
        ),
        session=f"projects/{PROJECT_ID}/locations/global/collections/default_collection/dataStores/{DATASTORE_ID}/sessions/{session_id}",
    )

    response = search_client.answer_query(request=request)

    return response
