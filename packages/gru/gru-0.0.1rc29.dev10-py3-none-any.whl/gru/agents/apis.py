import json
import os
import uuid
from termcolor import colored
from websockets import Headers
import yaml
from websockets.sync.client import connect

from gru import DEFAULT_CANSO_API_CONFIG
from gru.agents.models import MemoryInsertRequest, MemoryUpdateRequest, MemoryDeleteRequest
from gru.agents.models import AgentPromptRequest, AgentRegisterRequest, AgentUpdateRequest
from gru.schema.api_request_handler import APIRequestHandler
from gru.schema.api_response_handler import APIResponseHandler
from gru.utils.config_reader import ConfigReader

from cookiecutter.main import cookiecutter

AGENT_CONFIG_FILE_NAME = "config.yaml"

AI_AGENT_TEMPLATE_URL = "https://github.com/Yugen-ai/canso-ai-agent-templates.git"


def ai_agent_templates_setup():
    """
    Run Cookiecutter with the specified template.
    """
    cookiecutter(AI_AGENT_TEMPLATE_URL)

def call_api(
        correlation_id:str, 
        auth_token:str, 
        base_url:str, endpoint:str, 
        method:str, 
        body: dict|None = None
    ):
    request_handler = APIRequestHandler(auth_token, base_url=base_url)
    request_handler.set_correlation_id(correlation_id)

    response = request_handler.send_request(method, endpoint, body)

    response_handler = APIResponseHandler(response)
    response_handler.check_for_errors()
    response_message = response_handler.get_message()

    return response_message


def register_agent(
        correlation_id:str, 
        auth_token: str, 
        agent_folder: str, 
        cluster_name: str, 
        image: str, 
        image_pull_secret: str
    ):
    config_file_path = os.path.join(agent_folder, AGENT_CONFIG_FILE_NAME)

    with open(config_file_path, "r") as config_file:
        config_dict = yaml.safe_load(config_file)

    agent_slug = config_dict["agent_name"].lower().replace(' ', '-') 
    
    agent_register_request = AgentRegisterRequest(
        cluster_name=cluster_name,
        agent_name=agent_slug,
        image=image,
        image_pull_secret=image_pull_secret,
        task_server_name=config_dict["task_server_name"],
        checkpoint_db_name=config_dict["checkpoint_db_name"],
        replicas=config_dict["replicas"],
        iam_role_arn=config_dict["iam_role_arn"],
        vector_db_name=config_dict["vector_db_name"],
    )

    body = agent_register_request.model_dump()

    configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
    response_message = call_api(
        correlation_id, auth_token, 
        configs.agents_service_url, configs.agent_register_endpoint, 
        "post", body
    )

    return response_message

def update_agent(
        correlation_id:str, 
        auth_token: str, 
        agent_folder:str, 
        image: str, 
        image_pull_secret: str
    ):
    config_file_path = os.path.join(agent_folder, AGENT_CONFIG_FILE_NAME)

    with open(config_file_path, "r") as config_file:
        config_dict = yaml.safe_load(config_file)

    agent_name = config_dict["agent_name"].lower().replace(' ', '-')
    
    agent_update_request = AgentUpdateRequest(
        image=image,
        image_pull_secret=image_pull_secret,
        task_server_name=config_dict["task_server_name"],
        checkpoint_db_name=config_dict["checkpoint_db_name"],
        replicas=config_dict["replicas"],
        iam_role_arn=config_dict["iam_role_arn"]
    )

    body = agent_update_request.model_dump()

    configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
    endpoint = configs.agent_update_endpoint.replace("{agent_name}", agent_name)

    response_message = call_api(
        correlation_id, auth_token, 
        configs.agents_service_url, endpoint,
        "patch", body
    )

    return response_message


def deploy_agent(correlation_id:str, auth_token:str, agent_name:str):

    configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
    endpoint = configs.agent_deploy_endpoint.replace("{agent_name}", agent_name)

    response_message = call_api(
        correlation_id, auth_token, 
        configs.agents_service_url, endpoint, "post"
    )

    return response_message

def delete_agent(correlation_id: str, auth_token: str, agent_name):

    configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
    endpoint = configs.agent_delete_endpoint.replace("{agent_name}", agent_name)

    response_message = call_api(
        correlation_id, auth_token, 
        configs.agents_service_url, endpoint, "delete"
    )

    return response_message


def prompt_agent(agent_name: str, prompt: dict, auth_token: str):
    """
    Send a prompt to a deployed agent.

    Args:
        agent_name (str): Name of the deployed agent
        prompt (dict): Dictionary containing the prompt data
        auth_token (str): Authentication token for API access

    Returns:
        AgentPromptResponse: Response containing the prompt ID

    Raises:
        ApiError: If the API request fails
        ValueError: If the request parameters are invalid
    """
    prompt_request = AgentPromptRequest(prompt=prompt)
    request_json = prompt_request.model_dump()

    configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
    request_handler = APIRequestHandler(auth_token, configs)

    endpoint = configs.agent_prompt_endpoint.replace("{agent_name}", agent_name)

    response = request_handler.send_request("post", endpoint, request_json)
    response_handler = APIResponseHandler(response)
    response_handler.check_for_errors()

    response_data = response_handler.get_success_data()
    return response_data


def read_prompt_file(prompt_file: str) -> dict:
    """
    Read and parse a JSON prompt file.

    Args:
        prompt_file (str): Path to the JSON file containing prompt data

    Returns:
        dict: Parsed prompt data

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(prompt_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in {prompt_file}: {str(e)}", e.doc, e.pos
        )


def converse_agent(
    auth_token: str, agent_name: str, conversation_id: str | None = None
):

    headers = Headers({"authorization": auth_token})

    if conversation_id is None:
        conversation_id = str(uuid.uuid4())[:8]

    configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
    uri = configs.agent_converse_endpoint.replace("{agent_name}", agent_name).replace(
        "{conversation_id}", conversation_id
    )

    with connect(uri, additional_headers=headers) as websocket:
        print(f"Conversation ID: {conversation_id}")
        while True:
            user_msg = input(colored("User: ", attrs=["bold"]))
            if user_msg == "STOP":
                break

            websocket.send(user_msg)
            response = websocket.recv()
            print(f"{colored('Agent: ', attrs=['bold'])}{response}")

    return "Conversation Stopped"


def memory_insert(
        correlation_id: str,
        auth_token: str,
        agent_name: str,
        file_path: str
) -> str:
    """
    Insert data into agent memory
    Args:
        correlation_id: Unique identifier for the request
        auth_token: Authentication token
        agent_name: Name of the agent
        file_path: Path to JSON file containing memory data
    Returns:
        API response message
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"

        try:
            with open(file_path, 'r') as f:
                memory_data = json.load(f)
        except json.JSONDecodeError as e:
            line_col = f"line {e.lineno}, column {e.colno}"
            return f"Error: Invalid JSON in {file_path} at {line_col}: {e.msg}"

        required_fields = ["collection_name", "text", "data"]
        missing_fields = [field for field in required_fields if field not in memory_data]
        if missing_fields:
            return f"Error: Missing required fields in JSON: {', '.join(missing_fields)}"

        try:
            memory_insert_request = MemoryInsertRequest(
                collection_name=memory_data["collection_name"],
                text=memory_data["text"],
                data=memory_data.get("data", {})
            )
        except Exception as e:
            return f"Error: Invalid request data: {str(e)}"

        body = memory_insert_request.model_dump()

        configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
        endpoint = configs.agent_memory_endpoint.replace("{agent_name}", agent_name)
        agent_url = f"{configs.agents_service_url}/agents/{agent_name}"

        request_handler = APIRequestHandler(auth_token, base_url=agent_url)
        request_handler.set_correlation_id(correlation_id)

        try:
            response = request_handler.send_request("post", endpoint, body)
            response_handler = APIResponseHandler(response)
            response_handler.check_for_errors()
            return response_handler.get_message()
        except Exception as e:
            if hasattr(e, 'status_code') and hasattr(e, 'message'):
                return f"API Error ({e.status_code}): {e.message}"
            else:
                return f"Error communicating with the API: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}. Correlation ID: {correlation_id}"


def memory_update(
        correlation_id: str,
        auth_token: str,
        agent_name: str,
        file_path: str
) -> str:
    """
    Update data in agent memory
    Args:
        correlation_id: Unique identifier for the request
        auth_token: Authentication token
        agent_name: Name of the agent
        file_path: Path to JSON file containing update data
    Returns:
        API response message
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"

        try:
            with open(file_path, 'r') as f:
                memory_data = json.load(f)
        except json.JSONDecodeError as e:
            line_col = f"line {e.lineno}, column {e.colno}"
            return f"Error: Invalid JSON in {file_path} at {line_col}: {e.msg}"

        required_fields = ["collection_name", "memory_id", "text", "data"]
        missing_fields = [field for field in required_fields if field not in memory_data]
        if missing_fields:
            return f"Error: Missing required fields in JSON: {', '.join(missing_fields)}"

        try:
            memory_update_request = MemoryUpdateRequest(
                collection_name=memory_data["collection_name"],
                memory_id=memory_data["memory_id"],
                text=memory_data["text"],
                data=memory_data.get("data", {})
            )
        except Exception as e:
            return f"Error: Invalid request data: {str(e)}"

        body = memory_update_request.model_dump()

        configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
        endpoint = configs.agent_memory_endpoint.replace("{agent_name}", agent_name)
        base_url = f"{configs.agents_service_url}/agents/{agent_name}"

        request_handler = APIRequestHandler(auth_token, base_url=base_url)
        request_handler.set_correlation_id(correlation_id)

        try:
            response = request_handler.send_request("patch", endpoint, body)
            response_handler = APIResponseHandler(response)
            response_handler.check_for_errors()
            return response_handler.get_message()
        except Exception as e:
            if hasattr(e, 'status_code') and hasattr(e, 'message'):
                return f"API Error ({e.status_code}): {e.message}"
            else:
                return f"Error communicating with the API: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}. Correlation ID: {correlation_id}"

def memory_delete(
        correlation_id: str,
        auth_token: str,
        agent_name: str,
        memory_id: str,
        collection: str
) -> str:
    """
    Delete data from agent memory
    Args:
        correlation_id: Unique identifier for the request
        auth_token: Authentication token
        agent_name: Name of the agent
        memory_id: ID of the memory to delete
        collection: Name of the collection
    Returns:
        API response message
    """
    try:
        if not memory_id:
            return "Error: memory_id is required and cannot be empty"

        if not collection:
            return "Error: collection name is required and cannot be empty"

        try:
            memory_delete_request = MemoryDeleteRequest(
                collection_name=collection,
                memory_id=memory_id
            )
        except Exception as e:
            return f"Error: Invalid request data: {str(e)}"


        body = memory_delete_request.model_dump()

        configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
        endpoint = configs.agent_memory_endpoint.replace("{agent_name}", agent_name)

        base_url = f"{configs.agents_service_url}/agents/{agent_name}"

        request_handler = APIRequestHandler(auth_token, base_url=base_url)
        request_handler.set_correlation_id(correlation_id)

        try:
            response = request_handler.send_request("delete", endpoint, body)
            response_handler = APIResponseHandler(response)
            response_handler.check_for_errors()
            return response_handler.get_message()
        except Exception as e:
            if hasattr(e, 'status_code') and hasattr(e, 'message'):
                return f"API Error ({e.status_code}): {e.message}"
            else:
                return f"Error communicating with the API: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}. Correlation ID: {correlation_id}"