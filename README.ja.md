# Vertex AI SearchのAnswer APIを用いたChatUI（別名: Vertex AI Agent Builder）
## アーキテクチャ
![サンプルアーキテクチャ](/images/sample-architecture.png)

## 前提条件
- 有効な課金アカウントを持つGoogle Cloudプロジェクト
- Google Cloud SDK (gcloudコマンドとPython SDK)
- 検索ソースとなるPDFファイル複数個
- 権限を持つカスタムドメイン
- [オプション]: ローカルでのテストを行う場合、Python 3.12以上
- [オプション]: [Google Cloud Storageオブジェクトサービング](https://github.com/shin5ok/gcs-object-serving)


## 準備
### 1. リポジトリのクローン作成
ローカル環境で、このリポジトリをクローンし、ディレクトリを変更します。
```bash
git clone https://github.com/kawanos/chatui-using-answerapi; cd chatui-using-answerapi/
```

### 2. Google Cloudプロジェクトへのサインイン
※ すでに完了している場合は、スキップしてください  

認証を取得するには、以下を実行します。
```bash
gcloud auth login
```

ローカルでテストしたい場合は、
```bash
gcloud auth application-default login
```

### 3. 必要なサービスの有効化
```bash
gcloud services enable compute.googleapis.com run.googleapis.com cloudbuild.googleapis.com
```
数分かかります。

## 設定

### 1. Agent Builder用のデータストアの設定
データストアは簡単に構築できます。以下のリンクを参照してください。  
[https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search](https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search)

> [!NOTE]
> 他のデータソースで動作するかどうか確認していないため、Cloud Storageをデータソースとして使用することをお勧めします。


### 2. データストアIDの取得
データストアIDを書き留めてください。
![](./images/id_of_datastore.png)
この例では、IDは "kaijuu-storage_1723815035090" です。

### 3. Cloud Run 等に必要な環境変数を設定
環境変数を準備します。Database IDは先に書き留めたものを使用します。
```bash
export PROJECT_ID=<あなたのプロジェクトID>
export DATASTORE_ID=<あなたのデータストアID>
export RUN_NAME=chatapp
```
そして、アプリケーションに合わせて起動時のコメントを設定します。例えば、
```bash
export SUBJECT="社内規定について質問してください"
```
### オプション:
PDFやドキュメントなどのオブジェクトを配信する際の署名付きURLのセキュリティを考慮する場合は、[gcs-object-serving](https://github.com/shin5ok/gcs-object-serving)を使用できます。
```bash
export RETRIEVAL_FILE_URL=https://<ロードバランサ上のあなたのgcs-object-serving URL>
```
このオプションを使用すると、これらのオブジェクトはIAPによって保護されます。

### 4. Cloud Runサービス用のサービスアカウントの作成
トップディレクトリにいることを確認し、以下を入力します。
```bash
make sa iam
```
> [!NOTE]
> この例では、テストのため、Cloud Buildのデフォルトサービスアカウントのみを使用しています。本番環境またはステージング環境では、環境を保護するために、Cloud Build用のカスタムサービスアカウントを用意することをお勧めします。


### 5. Cloud Runサービスをデプロイ
デプロイします。
```bash
make deploy
```
デプロイが完了するまで数分待ちます。
