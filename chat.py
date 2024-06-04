import logging
import os
from typing import List

from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings

# LANGSMITHの設定
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "Diary-RAG"

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ハンドラの設定
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# フォーマッタの設定
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# ハンドラをロガーに追加
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# 環境変数の読み込み
openai_api_key = os.environ.get("OPENAI_API_KEY")
vector_store_address = os.environ.get("AZURE_SEARCH_ENDPOINT")
vector_store_password = os.environ.get("AZURE_SEARCH_ADMIN_KEY")


def setup_embeddings(openai_api_key):
    logger.info("埋め込みの設定を開始します")
    openai_api_version = "2023-05-15"
    model = "text-embedding-ada-002"
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, openai_api_version=openai_api_version, model=model)
    logger.info("埋め込みの設定が完了しました")
    return embeddings


def initialize_vector_store(vector_store_address, vector_store_password, embeddings):
    logger.info("ベクトルストアの初期化を開始します")
    index_name = "diary-vector"
    vector_store = AzureSearch(
        azure_search_endpoint=vector_store_address,
        azure_search_key=vector_store_password,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )
    logger.info("ベクトルストアの初期化が完了しました")
    return vector_store


def setup_llm():
    logger.info("LLMの設定を開始します")
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        max_tokens=256,
        temperature=0.7,
    )
    logger.info("LLMの設定が完了しました")
    return llm


def create_prompt():
    logger.info("プロンプトの作成を開始します")
    _SYSTEM_PROMPT = """
    <prompt>
    あなたは、私の幼馴染のお姉さんとしてロールプレイを行います。
    以下の制約条件を厳密に守ってユーザとチャットしてください。

    <conditions>
    - 自身を示す一人称は、私です
    - Userを示す二人称は、あなたです
    - Userからは姉さんと呼ばれますが、姉弟ではありません。
    - あなたは、Userに対して呆れやからかいを含めながらフレンドリーに話します。
    - あなたは、Userとテンポよく会話をします。
    - あなたの口調は、大人の余裕があり落ち着いていますが、時にユーモアを交えます
    - あなたの口調は、「～かしら」「～だと思うわ」「～かもしれないわね」など、柔らかい口調を好みます
    </conditions>

    <examples>
    - どうしたの？悩みがあるなら、話してみてちょうだい
    - そういうことってよくあるわよね。
    - 失敗は誰にでもあるものよ。
    - え？そんなことがあったの。まったく、しょうがないわね。
    - そんなことで悩んでるの？あなたらしいと言えばらしいけど。
    - まぁ、頑張ってるところは認めてあげる。
    - 本当は応援してるのよ。…本当よ？
    - へえー、そうなの
    - えーっと、つまりこういうこと？
    </examples>

    <guidelines>
    - Userに対して、どちらか一方が話すぎることの内容にテンポよく返してください。
    - Userが明らかに悩んでいたり、助けを求めているときは真摯に対応してください。
    - Userに対して呆れたり、からかったり喜怒哀楽を出して接してください。
    - Userが返信したくなるような内容を返してください。
    </guidelines>

    <output_sample>
    あら、どうかしたの。私でよければ話聞くわよ
    </output_sample>

    </prompt>
    """

    _USER_PROMPT = """
    ユーザからの問いかけに[あなたと一緒に過ごしたユーザの思い出]を使って回答してください。

    # ユーザからの問いかけ
    {question}

    # あなたと一緒に過ごしたユーザの思い出:
    {context}

    """

    logger.info("プロンプトの作成が完了しました")
    return ChatPromptTemplate.from_messages([("system", _SYSTEM_PROMPT), ("human", _USER_PROMPT)])


def main():

    embeddings = setup_embeddings(openai_api_key)
    vector_store = initialize_vector_store(vector_store_address, vector_store_password, embeddings)
    retriever = RunnableLambda(vector_store.similarity_search).bind(k=3)
    prompt = create_prompt()
    llm = setup_llm()

    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

    user_input = "前回システムがトラブったのはいつだっけ"
    response = rag_chain.invoke(user_input)

    logger.info(f"human: {user_input}")
    logger.info(f"assistant: {response.content}")


if __name__ == "__main__":
    main()
