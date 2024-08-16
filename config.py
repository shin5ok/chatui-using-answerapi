import os
  
VERTEX_AI_LOCATION = "global"
PROJECT_ID = os.environ.get("PROJECT_ID")
DATA_STORE_ID = os.environ.get("DATA_STORE_ID")

BUCKET_NAME = os.environ.get("BUCKET_NAME", PROJECT_ID)
LOCATION = os.environ.get("LOCATION", "europe-west1")

MODEL_VERSION = "gemini-1.5-flash-001/answer_gen/v1"
