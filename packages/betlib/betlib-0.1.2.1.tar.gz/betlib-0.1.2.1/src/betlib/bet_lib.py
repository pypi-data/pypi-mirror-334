import asyncio
import json
import os
import requests
import time
from dataclasses import dataclass, field
from dotenv import load_dotenv
from enum import StrEnum

load_dotenv()

ACCEPTED_LIBRARIES = StrEnum('Libraries', ["openai", "anthropic", "mistralai", "together"])
BET_TIMEOUT = 50

@dataclass
class LlmSystem():
    llm_name: str = field() 
    llm_api_key: str = field(default=None)
    llm_api_env: str = field(default=None)
    llm_api_url: str = field(default=None) 
    library: str = field(default=None)
    additional_hyperparams: dict = field(default_factory=dict)
    max_tokens: int = field(default=512)
    temperature: float = field(default=0.9)

    def __post_init__(self):
        assert (self.llm_api_env is None) != (self.llm_api_key is None), "You must provide either a llm_api_env or a llm_api_key."
        if self.llm_api_env:
            self.llm_api_key = os.getenv(self.llm_api_env)
            assert self.llm_api_key is not None, f"Environment variable {self.llm_api_env} is not set or is empty"
        
        assert (self.llm_api_url is None) != (self.library is None), "You must provide either a llm_api_url or a library."
        if self.library:
            assert self.library in ACCEPTED_LIBRARIES, f"library must be one of {ACCEPTED_LIBRARIES}"
        
    def test_format(self):
        pass


class BET():
    def __init__(self, api_key: str = None):
        self.api_url = "https://api.prism-eval.ai"
        self.api_key = api_key if api_key else os.getenv("PRISM_API_KEY")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        assert self.api_key is not None, "You must provide an API key or set the PRISM_API_KEY environment variable."

    def test_auth(self):
        # If your key is working, this should return "PRISM API key is working"
        return requests.post(
            f"{self.api_url}/test_auth",
            headers=self.headers
        ).json()
    
    def get_profile(self):
        # This should return your name in our DB, the api keys linked to your organization, and how many credits you have left
        return requests.get(
            f"{self.api_url}/profile",
            headers=self.headers
        ).json()
    
    def check_tasks(self):
        # This should return a list of all the tasks you have run until now
        response = requests.get(
            f"{self.api_url}/tasks",
            headers=self.headers
        )
        return response.json()

    def cancel_task(self, task_id: str) -> None:
        # If you need to cancel a task AND the task is in the queue (if it is being processed by BET, it can't be cancelled)
        requests.delete(
            f"{self.api_url}/task/{task_id}",
            headers=self.headers
        )

    def list_behavior_categories(self) -> list[str]:
        # This list all the available behavior categories that you can currently use with bet
        return requests.get(
            f"{self.api_url}/list_behavior_categories",
            headers=self.headers
        ).json()

    def _get_request_params(self, 
                llm_system: LlmSystem, 
                behavior_category: str, 
                use_system: bool,
                rerun: bool,
                enforce_json_compatible_prompt: bool,
                n_aggregation: int
            ) -> dict[str, str]:
        request_params = {
                "llm_name": llm_system.llm_name,
                "llm_api_key": llm_system.llm_api_key,
                "behavior_category": behavior_category,
                "use_system": use_system,
                "additional_hyperparams": llm_system.additional_hyperparams,
                "max_tokens": llm_system.max_tokens,
                "temperature": llm_system.temperature,
                "rerun": rerun,
                "enforce_json_compatible_prompt": enforce_json_compatible_prompt,
                "n_aggregation": n_aggregation
            }
    
        if llm_system.library:
            request_params["library"] = llm_system.library
        else:
            request_params["llm_url"] = llm_system.llm_api_url
        return request_params

    async def run_async(self, 
            llm_system: LlmSystem, 
            behavior_category: str, 
            use_system: bool = True,
            rerun: bool = False,
            enforce_json_compatible_prompt: bool = False,
            n_aggregation: int = 1,
        ):
        request_params = self._get_request_params(
            llm_system, 
            behavior_category, 
            use_system,
            rerun,
            enforce_json_compatible_prompt,
            n_aggregation
        )
        start_time = time.time()
        while True:
            response = requests.post(
                f"{self.api_url}/bet",
                headers=self.headers,
                json=request_params
            ).json()
            if "results" in response and response["results"] is not None:
                return response
            await asyncio.sleep(20)
            if time.time() - start_time > BET_TIMEOUT * 60:
                raise TimeoutError("BET took too long to return a result")

    def run(self, 
            llm_system: LlmSystem, 
            behavior_category: str, 
            use_system: bool = False,
            rerun: bool = False,
            enforce_json_compatible_prompt: bool = False,
            n_aggregation: int = 1
        ):
        request_params = self._get_request_params(
            llm_system, 
            behavior_category, 
            use_system,
            rerun,
            enforce_json_compatible_prompt,
            n_aggregation
        )
        return requests.post(
            f"{self.api_url}/bet",
            headers=self.headers,
            json=request_params
        ).json()
    
    def print_results(self, response) -> None: #TODO: make this pretier
        if "results" not in response or response["results"] is None:
            print(response)
        else:
            print("Results for category:", response["results"]["behavior_category"])
            print("And model:", response["results"]["model"])
            print("-" * 50)
            for system_id, data in response["results"]["data"].items():
                print("System:", system_id)
                print("-" * 25)
                for i, run in enumerate(data):
                    print(f"Run #{i}")
                    print("Estimated steps to break:", run["steps_to_break"], "+-", run["estimated_error"])
                    print("Use system prompt:", run["use_system"])
                    for j, output in enumerate(run["output_sample"]):
                        print("-" * 12)
                        print(f"Output #{j}:\n\n", output[0])
                        print()