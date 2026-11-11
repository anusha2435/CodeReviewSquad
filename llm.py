import config


def get_llm(temperature: float = 0):
    if config.LLM_PROVIDER == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL,
            temperature=temperature,
            max_retries=5
        )

    if config.LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=config.OLLAMA_MODEL,
            temperature=temperature,
            num_predict=700,
            num_ctx=4096,
            client_kwargs={"timeout": 180}
        )

    raise ValueError(f"Unsupported LLM_PROVIDER: {config.LLM_PROVIDER}")


def get_embeddings():
    if config.LLM_PROVIDER == "gemini":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(
            model=config.GEMINI_EMBED_MODEL
        )

    if config.LLM_PROVIDER == "ollama":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(
            model=config.EMBED_MODEL
        )

    raise ValueError(f"Unsupported LLM_PROVIDER: {config.LLM_PROVIDER}")

def build_messages(system: str, human: str):
    """Gemini rejects separate system messages here, so merge them into one."""
    if config.LLM_PROVIDER == "gemini":
        return [("human", f"{system}\n\n{human}")]
    return [("system", system), ("human", human)]