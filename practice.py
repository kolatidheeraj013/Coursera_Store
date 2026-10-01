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
        linkedin_profile_url: str,
        api_key:Optional[str]=None,
        mock:bool=False,
) -> Dict[str,Any]:
    "Extract LinkedIn profile data."
    start_time=time.time()

    try:
        if mock:
            logger.info("Using mock data...")
            response=requests.get(
                config.MOCK_DATA_URL,
                timeout=30,

            )
        else:
            if not api_key:
                raise ValueError(
                    "API key is required when mock is false."
                )
            api_endpoint=(
                    "https://nubela.co/proxycurl/api/v2/linkedin"

            )
            headers={
                "Authorization":f"Bearer {api_key}"

            }
            params={
                "url":linkedin_profile_url,
                "fallback_to_cache":"on-error",
                "use_cache":"if-present",
                "skills":"include",
                "inferred_salary":"include",
                "personal_contact_number":"inlcude",

            }
            response=request.get(
                api_endpoint,
                headers=headers,
                paramas=params,
                timeout=10,
            )            
        logger.info(
            "response recieved after %.2f seconds",
            time.time() - start_time,
        )
        if response.status_code != 200:
            if mock :
                logger.warning(
                    "Mock data URl returned %s";using built-in mock data."
                    response.status_code,
                )
                return MOCK_PPROFILE_DATA
            logger.error(
                "Request failed with status code %s",
                response.status_code,
            )
            return{}
        data=response.json()

        data={
            key: value 
            for key,value in data.items() 
            if value not in ([],"",None) 
            and key not in [
                "people_also_viewed",
                "certifiations",
            ]
        }
        if data.get("groups"):
            for group in data["groups"]:
                group.pop("profile_pic_url",None)

        return data
    except Exception as error 
       logger.error(
           "error extracting profile data: %s",
           error
       )
       return {}