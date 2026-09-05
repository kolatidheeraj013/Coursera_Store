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
            streaming=Flase,
            
        )