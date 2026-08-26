"""Module for interfacing with IBM watsonx.ai LLMs."""

import logging

from llama_index.embeddings.ibm import WatsonxEmbeddings
from llama_index.llms.ibm import WatsonxLLM

import config

logger = logging.getLogger(__name__)


def create_watsonx_embedding() -> WatsonxEmbeddings:
    return WatsonxEmbeddings(
        model_id=config.EMBEDDING_MODEL_ID,
        url=config.WATSONX_URL,
        project_id=config.WATSONX_PROJECT_ID,
    )


def create_watsonx_llm(
    temperature: float = config.TEMPERATURE,
    max_new_tokens: int = config.MAX_NEW_TOKENS,
    decoding_method: str = "sample",
) -> WatsonxLLM:
    return WatsonxLLM(
        model_id=config.LLM_MODEL_ID,
        url=config.WATSONX_URL,
        project_id=config.WATSONX_PROJECT_ID,
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        additional_params={
            "decoding_method": decoding_method,
            "min_new_tokens": config.MIN_NEW_TOKENS,
            "top_k": config.TOP_K,
            "top_p": config.TOP_P,
        },
    )


def change_llm_model(new_model_id: str) -> None:
    config.LLM_MODEL_ID = new_model_id
