from pydantic import BaseModel
from typing import Dict, Any, Optional


class AgentPromptRequest(BaseModel):
    """
    Model representing a prompt request to an agent.

    Attributes:
        prompt (Dict[str, Any]): Dictionary containing the prompt data
    """

    prompt: Dict[str, Any]


class AgentRegisterRequest(BaseModel):
    cluster_name: str
    agent_name: str
    image: str
    image_pull_secret: str
    task_server_name: str
    checkpoint_db_name: str
    replicas: int
    iam_role_arn: Optional[str] = None
    vector_db_name: Optional[str] = None

class AgentUpdateRequest(BaseModel):
    image: Optional[str] = None
    image_pull_secret: Optional[str] = None
    task_server_name: Optional[str] = None
    checkpoint_db_name: Optional[str] = None
    replicas: Optional[int] = None
    iam_role_arn: Optional[str] = None
    vector_db_name: Optional[str] = None


class MemoryInsertRequest(BaseModel):
    """
    Model for inserting data into memory.
    Attributes:
        collection_name: Name of the collection to insert data into
        text: Text content to be embedded
        metadata: Additional metadata for the memory
    """
    collection_name: str
    text: str
    data: Dict[str, Any]


class MemoryUpdateRequest(BaseModel):
    """
    Model for updating data in memory.
    Attributes:
        collection_name: Name of the collection containing the data
        memory_id: ID of the document to update
        text: New text content to be embedded
        metadata: Updated metadata for the memory
    """
    collection_name: str
    memory_id: str
    text: str
    data: Dict[str, Any]


class MemoryDeleteRequest(BaseModel):
    """
    Model for deleting data from memory.
    Attributes:
        collection_name: Name of the collection containing the data
        memory_id: ID of the document to delete
    """
    collection_name: str
    memory_id: str