import os
  
VERTEX_AI_LOCATION = "global"
PROJECT_ID = os.environ.get("PROJECT_ID")
DATASTORE_ID = os.environ.get("DATASTORE_ID")

BUCKET_NAME = os.environ.get("BUCKET_NAME", PROJECT_ID)
LOCATION = os.environ.get("LOCATION", "europe-west1")

REF_PAGES = "REF_PAGES" in os.environ

SUBJECT = os.environ.get("SUBJECT", "Ask me anything")

MODEL_VERSION = "gemini-1.5-flash-001/answer_gen/v1"
