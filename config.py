import os
  
VERTEX_AI_LOCATION = "global"
MODEL_VERSION = "gemini-1.5-flash-002/answer_gen/v1"

PROJECT_ID = os.environ.get("PROJECT_ID")
DATASTORE_ID = os.environ.get("DATASTORE_ID")

REF_PAGES = os.environ.get("REF_PAGES")
REF_ONLY = os.environ.get("REF_ONLY")

SUBJECT = os.environ.get("SUBJECT")

SEARCH_PAGE_SIZE = os.environ.get("SEARCH_PAGE_SIZE", 5)
SEARCH_CONTENT_LIMIT = int(os.environ.get("SEARCH_CONTENT_LIMIT", 100))
RETRIEVAL_FILE_URL = os.environ.get("RETRIEVAL_FILE_URL")

PREAMBLE = ""
# PREAMBLE = """
# Given the conversation between a user and a helpful assistant and some search results, create a final answer for the assistant.
# The answer should use all relevant information from the search results, not introduce any additional information, and use exactly the same words as the search results when possible.
# The assistant's answer should be no more than 20 sentences.
# The assistant's answer should be formatted as a bulleted list.
# Each list item should start with the "-" symbol.
# """
