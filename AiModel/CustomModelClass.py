from typing import Any, List, Mapping, Optional

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
import requests

import os
import sys

#To make globals file available
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

import Globals 


class CustomLLM(LLM):

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        # if stop is not None:
        #     raise ValueError("stop kwargs are not permitted.")
        
        response = requests.post(
            Globals.MODEL_URL+"/generate/",

            json={
                "inputs": prompt,
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 256
                    }
                }
            ) 
        
        return response.json()["generated_text"]