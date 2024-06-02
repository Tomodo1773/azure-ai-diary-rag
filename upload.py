import os
import logging

from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 環境変数読み込み
openai_api_key: str = os.environ.get("OPENAI_API_KEY")
vector_store_address: str = os.environ.get("AZURE_SEARCH_ENDPOINT")
vector_store_password: str = os.environ.get("AZURE_SEARCH_ADMIN_KEY")
logger.info("環境変数が読み込まれました。")

# テキストをロード
directory_path = "./diary/2024"
loader = DirectoryLoader(directory_path, glob="*.txt", show_progress=True)
docs = loader.load()
logger.info(f"{len(docs)}件のドキュメントがロードされました。")

# テキストをベクトル化
openai_api_version: str = "2023-05-15"
model: str = "text-embedding-ada-002"
embeddings: OpenAIEmbeddings = OpenAIEmbeddings(
    openai_api_key=openai_api_key, openai_api_version=openai_api_version, model=model
)
logger.info("テキストのベクトル化が完了しました。")

# インデックスの設定
index_name: str = "diary-vector"
embedding_function = embeddings.embed_query
fields = [
    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True,
        filterable=True,
    ),
    SearchableField(name="content", type=SearchFieldDataType.String, searchable=True, analyzer_name="ja.microsoft"),
    SearchField(
        name="content_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=len(embedding_function("Text")),
        vector_search_profile_name="myHnswProfile",
    ),
    SearchableField(name="metadata", type=SearchFieldDataType.String, searchable=True, analyzer_name="ja.microsoft"),
]

# AzureSearchのインスタンスを初期化
vector_store = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
    fields=fields,
)

# AzureSearchのインスタンスにDocumentオブジェクトを追加
vector_store.add_documents(documents=docs)
logger.info(f"{len(docs)}件のドキュメントがAzureSearchインデックスに追加されました。")
