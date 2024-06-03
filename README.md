# azure-ai-diary-rag

## プロジェクトの概要

azure-ai-diary-ragは、ユーザーの日記をベクトル化し、Azure Searchを使用して類似度検索を行うことで、ユーザーの思い出に基づいた対話型のチャットボットを実現するプロジェクトです。このプロジェクトでは、docxファイルをtxtファイルに変換し、txtファイルをベクトル化してAzure Searchにアップロードします。ユーザーの入力に基づいて関連する思い出を検索し、Gemini1.5 PROモデルを使用して対話的な応答を生成します。

## 主な機能

- docxファイルをtxtファイルに変換
- txtファイルをベクトル化し、Azure Searchにアップロード
- ユーザーの入力に基づいて、関連する思い出を検索
- 検索結果を使用して、GPT-3.5モデルによる対話的な応答を生成

## 使用技術

- Python
- Azure Search
- OpenAI API (embeddings)
- Gemini API (Gemini 1.5 PRO)
- langchain
- python-docx

## ディレクトリ構成とファイルの説明

- `azure-ai-diary-rag/`
  - `converter.py`: docxファイルをtxtファイルに変換するスクリプト
  - `diary/`: 日記のtxtファイルを格納するディレクトリ
  - `chat.py`: チャットボットの主要な機能を実装するメインスクリプト
  - `upload.py`: txtファイルをベクトル化し、Azure Searchにアップロードするスクリプト

## セットアップと使用方法

1. 必要な環境変数を設定します:
   - `OPENAI_API_KEY`: OpenAI APIキー
   - `AZURE_SEARCH_ENDPOINT`: Azure Searchのエンドポイント
   - `AZURE_SEARCH_ADMIN_KEY`: Azure Searchの管理者キー
   - `LANGCHAIN_API_KEY`: LangChain APIキー
   - `GOOGLE_API_KEY`: Google APIキー

2. 依存関係のインストール:

    ```bash
    poetry install
    ```

3. `diary`ディレクトリに日記のdocxファイルを配置します。

4. docxファイルをtxtファイルに変換します:

    ```bash
    python converter.py
    ```

5. txtファイルをベクトル化してAzure AI Searchにアップロードします:

    ```bash
    python upload.py
    ```

6. チャットボットを起動します:

    chat.pyに記載されているユーザプロンプトに対して日記を参照したうえで返答が生成され出力されます。

    ```bash
    python chat.py
    ```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、[LICENSE](LICENSE)ファイルを参照してください。

## 貢献

プルリクエストや改善案は歓迎します。バグ報告や機能リクエストがある場合は、Issueを作成してください。
