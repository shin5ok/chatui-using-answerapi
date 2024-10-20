import re
from urllib.parse import quote

from pprint import pprint as pp
from google.cloud import discoveryengine_v1 as discoveryengine
from google.cloud.discoveryengine_v1.types import SearchRequest
from google.api_core.client_options import ClientOptions

import config as c
import utils as u

VERTEX_AI_LOCATION = c.VERTEX_AI_LOCATION
PROJECT_ID = c.PROJECT_ID
DATASTORE_ID = c.DATASTORE_ID

client_options = (
    ClientOptions(api_endpoint=f"{VERTEX_AI_LOCATION}-discoveryengine.googleapis.com")
    if VERTEX_AI_LOCATION != "global"
    else None
)
search_client = discoveryengine.ConversationalSearchServiceClient(
    client_options=client_options
)

PREAMBLE = c.PREAMBLE

def query(search_query):
    client = discoveryengine.SearchServiceClient()

    request = SearchRequest(
        serving_config=client.serving_config_path(
            project=PROJECT_ID,
            location=VERTEX_AI_LOCATION,
            data_store=DATASTORE_ID,
            serving_config="default_config"
        ),
        query=search_query,
        page_size=c.SEARCH_PAGE_SIZE,
    )

    response = client.search(request)
    results = []

    for page in response.pages:
        for result in page.results:
            data = {}
            for k,v in (result.document.derived_struct_data.items()):
                if k == "extractive_answers":
                    content = v[0].get("content")
                    data["extractive_answers"] = content[0:c.SEARCH_CONTENT_LIMIT]
                    continue
                if k == "link":
                    data["url"] = u.gcs_path_to_url(v)
                    continue
                data[k] = v
            results.append(data)
    pp(results)
    return results


if __name__ == "__main__":
    import sys
    search_query: str = sys.argv[1]
    query(search_query)
    