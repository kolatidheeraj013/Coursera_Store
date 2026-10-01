'""modules for querying indexing Linkedin profile data'""
import logging
from typing import Any
from llama_index.core import PromptTemplate , VectorStoreIndex
import config 
from modules.llm_interface import create_watsonx_llm

logger=logging.getLogger(__name__)

def generated_initial_facts(index:VectorStoreIndex)-> str:
    try:
        query_engine=index.as_query_engine(
        streaming=False,
        similarity_top_k=config.SIMILARITY_TOP_K,
        llm=create_watsonx_llm(
            tempearature=0.0,
            max_new_tokens=500,
            decoding_methods="sample",
        ),
        text_qa_template=PromptTemplate(
            template=config.INITIAL_FACTS_TEMPLATE
        ),
    )

    return query_engine.query(
        "Provide three interesting facts about this person's career or education."
    ).response

    except Exception as error:
        logger.error("Error in generate_initial_facts:%s",error)
        return "Failed ot generated initial facts"

def answer_user_query(index:VectorStoreIndex,user_query:str) ->Any:
    try:
        query_engine=index.as_query_engine(
            streaming=False,
            similarity_top_k=config.SIMILARITY_TOP_K,
            llm=create_watsonx_llm(
                temperature=0.0,
                max_new_tokens=250,
                decoding_methods="greddy",
            ),
            text_qa_template=PromptTemplate(
                template=config.USER_QUESTION_TEMPLATE 
            ),
        )
        return query_engine.query(user_query)
    except Exception as error:
        logger.error("Error in answer_user_qeury:%s",error)
        return "Failed to get an answer."
         
    