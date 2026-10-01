"""Module for processing Linkedin profile data """

import json
import logging
from typing import Any,Dict,List,Optional

from llama_index.core import Documnet,VectorstoreIndex
from llama_index.core.node_parser import SentenceSpitter

import config 
from modules.llm_interface import create_watsonx_embedding

logger=logging.getLogger(__name__)


def split_profile_data(profile_data: Dict[str,Any]) -> List:
    try:
        document=Document(text=json.dumps(profile_data))
        nodes=SentencesSplitter(chunk_size=config.CHUNK_SIZE).get_nodes_from_documents(
            [document]
            )
        logger.info("Created %s nodes from profile data",len(nodes))
        return nodes
    except Exception as error:
        logger.error("Error in split_profile_data: %s",error)
        return []

def create_vector_database(nodes : list )-> Optional[VectorstoreIndex]
    try:
       return VectorstoreIndex(
           nodes=nodes,
           embed_model=create_watsonx_embedding(),
           show_progress=True,
       )
    except Exception as error:
        logger.error("Error in create_vector_database:%s",error)
        return None

def verify_embeddings(index : VectorStoreIndex) -> bool:
    try:
       vector_store = index._storage_context.vector_store
       for node_id in index.index_struct.nodes_dict:
           if vector_store.get(node_id) is None:
               return False
           return True
    except Exception as error:
        logger.error("Error in verify_embeddings:%s ",error)
        return False