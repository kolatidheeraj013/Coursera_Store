import logging
import time 
from typing import Any,Dict,Optional
import requests
import config

logger=logging.getLogger(__name__)

MOCK_PPROFILE_DATA={
    "full_name":"Leon Katsnelon",
    "headline":"Technology leader and software engineer",
    "summary":"Experienced technology professional with a background in software engineering and leadership.",
    "experiences":[
        {
            "title":"Technology Leader",
            "company":"Technology company",
            "description":"Leads software engineering teams and technology initiatives.",

        }
    ],
}
def extract_linked_profile(
        linked_profile_url:str,
        api_key:Optional[str]=None,
            
)