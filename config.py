import os
  
VERTEX_AI_LOCATION = "global"
MODEL_VERSION = "gemini-1.5-flash-002/answer_gen/v1"

PROJECT_ID = os.environ.get("PROJECT_ID")
DATASTORE_ID = os.environ.get("DATASTORE_ID")
SUBJECT = os.environ.get("SUBJECT")


REF_PAGES = os.environ.get("REF_PAGES")
REF_ONLY = os.environ.get("REF_ONLY")

SEARCH_PAGE_SIZE = int(os.environ.get("SEARCH_PAGE_SIZE", 5))
SEARCH_CONTENT_LIMIT = int(os.environ.get("SEARCH_CONTENT_LIMIT", 100))
RETRIEVAL_FILE_URL = os.environ.get("RETRIEVAL_FILE_URL")


PREAMBLE = "200文字以内で簡潔にまとめるように"
# PREAMBLE = """
# ユーザーと親切なアシスタントとの会話といくつかの検索結果に基づいて、アシスタントへの最終的な回答を作成します。
# 回答では、検索結果の関連情報をすべて使用し、追加情報を導入せず、可能な場合は検索結果とまったく同じ単語を使用する必要があります。
# アシスタントの回答は 20 文以内にする必要があります。
# アシスタントの回答は、箇条書きリストとしてフォーマットする必要があります。
# 各リスト項目は「-」記号で始まる必要があります。
# """
