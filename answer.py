import re
from urllib.parse import quote

from pprint import pprint as pp
from google.cloud import discoveryengine_v1 as discoveryengine
from google.api_core.client_options import ClientOptions

import config as c
import utils as u

VERTEX_AI_LOCATION = c.VERTEX_AI_LOCATION
PROJECT_ID = c.PROJECT_ID
DATASTORE_ID = c.DATASTORE_ID

MODEL_VERSION = c.MODEL_VERSION

PREAMBLE = c.PREAMBLE

doc_cache: dict = {}

class AnswerClient:

    def __init__(self, credentials=None):
    
        client_options = (
            ClientOptions(api_endpoint=f"{VERTEX_AI_LOCATION}-discoveryengine.googleapis.com")
            if VERTEX_AI_LOCATION != "global"
            else None
        )
        search_client = discoveryengine.ConversationalSearchServiceClient(
            client_options=client_options,
            credentials=credentials,
        )
    
        pp(search_client)
        self.client = search_client
    
    
    def query(
        self,
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
                    max_rephrase_steps=5,
                    disable=False,
                ),
            ),
            search_spec=discoveryengine.AnswerQueryRequest.SearchSpec(
                search_params=discoveryengine.AnswerQueryRequest.SearchSpec.SearchParams(
                    max_return_results=3,
                )
            ),
            related_questions_spec=discoveryengine.AnswerQueryRequest.RelatedQuestionsSpec(
                enable=True,
            ),
            answer_generation_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec(
                model_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.ModelSpec(
                    model_version=MODEL_VERSION,
                ),
                prompt_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.PromptSpec(
                    preamble=PREAMBLE,
                ),
                include_citations=True,
                ignore_adversarial_query=True,
                ignore_low_relevant_content=False,
                ignore_non_answer_seeking_query=False,
            ),
            session=f"projects/{PROJECT_ID}/locations/global/collections/default_collection/dataStores/{DATASTORE_ID}/sessions/{session_id}",
        )
    
        response = self.client.answer_query(request=request)
    
        return response
    
    def render_response(self, response):
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
                        "url": u.get_doc_uri(item.chunk_info.document_metadata.document)
                    }
                    citations.append(citation)
        except Exception as e:
            print(e)
    
        return answer_with_citations, citations


if __name__ == "__main__":

    import sys
    from pprint import pprint as pp
    a = AnswerClient()
    r = a.query(sys.argv[1])
    pp(a.render_response(r))
