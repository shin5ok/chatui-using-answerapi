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
                max_return_results=3,
            )
        ),
        answer_generation_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec(
            model_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.ModelSpec(
                model_version=MODEL_VERSION,
            ),
            prompt_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.PromptSpec(
                preamble="""
                    Given the conversation between a user and a helpful assistant and some search results, create a final answer for the assistant.
                    The answer should use all relevant information from the search results, not introduce any additional information, and use exactly the same words as the search results when possible.
                    The assistant's answer should be no more than 20 sentences.
                    The assistant's answer should be formatted as a bulleted list.
                    Each list item should start with the "-" symbol.
                """
            ),
            include_citations=True,
            ignore_low_relevant_content=True,
            ignore_non_answer_seeking_query=True,
        ),
        session=f"projects/{PROJECT_ID}/locations/global/collections/default_collection/dataStores/{DATASTORE_ID}/sessions/{session_id}",
    )

    response = search_client.answer_query(request=request)

    return response
