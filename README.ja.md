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
git clone https://github.com/shin5ok/chatui-using-answerapi; cd chatui-using-answerapi/
```

### 2. Google Cloudプロジェクトへのサインイン
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

### 3. Cloud Runサービス用のサービスアカウントの作成
トップディレクトリにいることを確認し、以下を入力します。
```bash
make sa iam
```
> [!NOTE]
> この例では、テストのため、Cloud Buildのデフォルトサービスアカウントのみを使用しています。本番環境またはステージング環境では、環境を保護するために、Cloud Build用のカスタムサービスアカウントを用意することをお勧めします。

### 4. Cloud Runサービスのデプロイ
環境変数を準備します。Database IDは先に書き留めたものを使用します。
```bash
export PROJECT_ID=<あなたのプロジェクトID>
export DATASTORE_ID=<あなたのデータストアID>
```
そして、アプリケーションに合わせて起動コメントを設定します。例えば、
```bash
export SUBJECT="Google Cloudセキュリティについて質問してください"
```
### オプション:
PDFやドキュメントなどのオブジェクトを配信する際の署名付きURLのセキュリティを考慮する場合は、[gcs-object-serving](https://github.com/shin5ok/gcs-object-serving)を使用できます。
```bash
export RETRIEVAL_FILE_URL=https://<ロードバランサ上のあなたのgcs-object-serving URL>
```
このオプションを使用すると、これらのオブジェクトはIAPによって保護されます。

デプロイします。
```bash
make deploy
```
デプロイが完了するまで数分待ちます。

> [!NOTE]
> セキュリティ上の理由から、このサービスはロードバランサとIAPを必要とするため、まだCloud Runサービスにアクセスできません。次の手順に進みます。

### 5. Identity Aware Proxy (IAP) の設定
インターネットからの不正アクセスを防ぐために、IAPを利用できます。

以下のリンクを参照してください。  
[https://cloud.google.com/iap/docs/enabling-cloud-run?hl=ja](https://cloud.google.com/iap/docs/enabling-cloud-run?hl=ja)  
マネージド証明書または証明書マネージャーから提供されるSSL証明書を使用できます。

> [!NOTE]
> IAPを採用する際は、ロードバランサでCDNを無効にする必要があります。

### 6. テスト
ブラウザで、ロードバランサに割り当てられた証明書のFQDNを開きます。テストしてみてください。


## オプション: データストアのデータ更新
検索データを更新したい場合は、`gs://[Cloud Storageバケット]/data` のようなデータストアのパスを覚えておいてください。例えば、
```bash
export PROJECT_ID=<あなたのプロジェクトID>
export DATASTORE_ID=<あなたのデータストアID>

poetry run python refresh_datastore.py gs://foo/data/*.pdf gs://bar/reports/*.pdf
```