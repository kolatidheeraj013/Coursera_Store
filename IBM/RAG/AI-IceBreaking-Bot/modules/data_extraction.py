"""Module for extracting LinkedIn profile data."""

import logging
import time
from typing import Any, Dict, Optional

import requests

import config

logger = logging.getLogger(__name__)

MOCK_PROFILE_DATA = {
    "full_name": "Leon Katsnelson",
    "headline": "Technology leader and software engineer",
    "summary": "Experienced technology professional with a background in software engineering and leadership.",
    "experiences": [
        {
            "title": "Technology Leader",
            "company": "Technology Company",
            "description": "Leads software engineering teams and technology initiatives.",
        }
    ],
    "education": [
        {
            "school": "University",
            "degree_name": "Computer Science",
        }
    ],
}


def extract_linkedin_profile(
    linkedin_profile_url: str,
    api_key: Optional[str] = None,
    mock: bool = False,
) -> Dict[str, Any]:
    start_time = time.time()
    try:
        if mock:
            logger.info("Using mock data...")
            response = requests.get(config.MOCK_DATA_URL, timeout=30)
        else:
            if not api_key:
                raise ValueError("API key is required when mock is False.")
            response = requests.get(
                "https://nubela.co/proxycurl/api/v2/linkedin",
                headers={"Authorization": f"Bearer {api_key}"},
                params={
                    "url": linkedin_profile_url,
                    "fallback_to_cache": "on-error",
                    "use_cache": "if-present",
                    "skills": "include",
                    "inferred_salary": "include",
                    "personal_email": "include",
                    "personal_contact_number": "include",
                },
                timeout=10,
            )

        logger.info("Response received after %.2f seconds", time.time() - start_time)
        if response.status_code != 200:
            if mock:
                logger.warning(
                    "Mock data URL returned %s; using built-in mock data.",
                    response.status_code,
                )
                return MOCK_PROFILE_DATA
            logger.error("Request failed with status code %s", response.status_code)
            return {}

        data = response.json()
        data = {
            key: value
            for key, value in data.items()
            if value not in ([], "", None)
            and key not in ["people_also_viewed", "certifications"]
        }
        for group in data.get("groups", []):
            group.pop("profile_pic_url", None)
        return data
    except Exception as error:
        logger.error("Error extracting profile data: %s", error)
        return {}
