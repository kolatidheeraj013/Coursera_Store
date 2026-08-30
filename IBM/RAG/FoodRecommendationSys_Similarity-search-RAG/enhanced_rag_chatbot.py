from shared_functions import *
from typing import List, Dict, Any
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.foundation_models import ModelInference
import json

# Global variables
food_items = []

# IBM Watsonx.ai Configuration
my_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com"
}

model_id = 'ibm/granite-4-h-small'
gen_parms = {"max_new_tokens": 400}
project_id = "skills-network"  # <--- NOTE: specify "skills-network" as your project_id
space_id = None
verify = False

# Initialize the LLM model
model = ModelInference(
    model_id=model_id,
    credentials=my_credentials,
    params=gen_parms,
    project_id=project_id,
    space_id=space_id,
    verify=verify,
)
