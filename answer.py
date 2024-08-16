import os
from google.cloud import discoveryengine_v1alpha as discoveryengine
from google.api_core.client_options import ClientOptions

import config as c

VERTEX_AI_LOCATION = c.VERTEX_AI_LOCATION
PROJECT_ID = c.PROJECT_ID
DATA_STORE_ID = c.DATA_STORE_ID

MODEL_VERSION = c.MODEL_VERSION

client_options = (
    ClientOptions(api_endpoint=f"{VERTEX_AI_LOCATION}-discoveryengine.googleapis.com")
    if VERTEX_AI_LOCATION != "global"
    else None
)
search_client = discoveryengine.ConversationalSearchServiceClient(
    client_options=client_options
)


def answer_query(
    query_text: str, session_id: str = "-"
) -> discoveryengine.types.conversational_search_service.AnswerQueryResponse:
    # Init Query object
    query = discoveryengine.Query()
    query.text = query_text

    request = discoveryengine.AnswerQueryRequest(
        serving_config=f"projects/{PROJECT_ID}/locations/global/collections/default_collection/dataStores/{DATA_STORE_ID}/servingConfigs/default_serving_config",
        query=query,
        # （Option）クエリフェーズ
        query_understanding_spec=discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec(
            # クエリ言い換え
            query_rephraser_spec=discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec.QueryRephraserSpec(
                disable=False,  # True に設定するとクエリ言い換えを無効化
                max_rephrase_steps=5,  # 言い換えステップ数を設定（1〜5の範囲）
            ),
        ),
        # （Option）検索フェーズ
        search_spec=discoveryengine.AnswerQueryRequest.SearchSpec(
            search_params=discoveryengine.AnswerQueryRequest.SearchSpec.SearchParams(
                max_return_results=3
            )
        ),
        # （Option）回答フェーズ
        answer_generation_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec(
            # モデル指定
            model_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.ModelSpec(
                model_version=MODEL_VERSION,
            ),
            # プリアンブル設定
            prompt_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.PromptSpec(
                preamble="箇条書きで回答してください。"
            ),
            # 引用を含めるかどうか
            include_citations=True,
            # 関連性の低いクエリを除外するかどうか
            ignore_low_relevant_content=True,
            # 分類されたクエリを無視するかどうか
            ignore_non_answer_seeking_query=True,
        ),
        # （Option）フォローアップ検索利用時のセッション
        session=f"projects/{PROJECT_ID}/locations/global/collections/default_collection/dataStores/{DATA_STORE_ID}/sessions/{session_id}",
    )

    # Answer API 実行
    response = search_client.answer_query(request=request)

    return response
