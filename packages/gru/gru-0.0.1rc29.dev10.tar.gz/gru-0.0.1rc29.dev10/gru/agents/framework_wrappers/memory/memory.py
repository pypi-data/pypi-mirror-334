from typing import Any, Dict, Optional
import uuid
import os

from gru.agents.framework_wrappers.memory.base import BaseMemory
from gru.agents.framework_wrappers.memory.collection_manager import CollectionManager
from gru.agents.tools.core.embeddings.embedding_factory import EmbeddingFactory, EmbeddingType
from datetime import datetime
from gru.agents.tools.core.vector_db.base import (
    AddToCollectionResponse,
    DeleteFromCollectionResponse,
    SimilaritySearchResponse,
    UpdateCollectionResponse
)
from gru.agents.tools.core.vector_db.vectordb_factory import VectorDBFactory, VectorDBType

class CansoMemory(BaseMemory):
    DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory_collections.yaml")


    def __init__(
        self,
        client: Any,
        embedding_type: EmbeddingType = EmbeddingType.OPENAI,
        vector_db_type: VectorDBType = VectorDBType.MILVUS,
        embedding_model: Optional[str] = None,
        config_path: Optional[str] = None,
    ):
        self.vdb_client = VectorDBFactory.get_vector_db_client(
            vector_db_type 
        )
        self.embedding_generator = EmbeddingFactory.get_embedding_generator(
            embedding_type=embedding_type,
            client=client,
            model=embedding_model
        )
        self.collection_schemas = {}

        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        
        self.collection_manager = CollectionManager(
            vector_db_client=self.vdb_client,
            embedding_dimension=self.embedding_generator.dimension,
            config_path=self.config_path
        )
        self.collection_manager.initialize_collections()

    async def store(self, data: Dict[str, Any], collection_name: str) -> AddToCollectionResponse:
        text = data.get("text", "")
        if not text:
            return AddToCollectionResponse(
                status="error",
                message="Text field is required for embedding generation",
                ids=[]
            )
        
        try:
            embedding = await self.embedding_generator.generate(text)
        except Exception as e:
            return AddToCollectionResponse(
                status="error",
                message=f"Failed to generate embedding: {str(e)}",
                ids=[]
            )
        
        
        document = data.get("data", {}).copy()
        document["text"] = text
        
        if "memory_id" not in document:
            document["memory_id"] = str(uuid.uuid4())
        
        if "created_at" not in document:
            document["created_at"] = datetime.now().isoformat()
        
        try:
            result = await self.vdb_client.add_to_collection(
                collection_name,
                embeddings=[embedding],
                data=[document]
            )
        except Exception as e:
            return AddToCollectionResponse(
                status="error",
                message=f"Failed to add document to collection: {str(e)}",
                ids=[]
            )
        
        return AddToCollectionResponse(
            status="success" if result.status != "error" else "error",
            message=result.message,
            ids=result.ids
        )

    async def retrieve(
            self, 
            query: str, 
            collection_name: str,
            top_k: int = 5
        ) -> SimilaritySearchResponse:
        try:
            query_embedding = await self.embedding_generator.generate(query)
            results = await self.vdb_client.similarity_search(
                collection_name=collection_name,
                query_vector=query_embedding,
                top_k=top_k,
            )
            return results
        except Exception as e:
            print(f"Error in retrieve: {str(e)}")
            return SimilaritySearchResponse(
                status="error",
                message=f"Failed to retrieve documents: {str(e)}",
                results=[]
            )

    async def update(
            self,
            doc_id: str,
            data: Dict[str, Any],
            collection_name: str
    ) -> UpdateCollectionResponse:
        """Update an existing memory entry in specified collection"""
        try:
            text = data.get("text")
            if text is None:
                raise ValueError("Text content is required for update")

            embedding = await self.embedding_generator.generate(text)

            # Prepare metadata with all necessary fields
            doc = {
                "text": text,
                "data": data.get("data", {}),
                "created_at": datetime.now().isoformat()
            }

            result = await self.vdb_client.update_collection(
                collection_name=collection_name,
                memory_id=doc_id,
                embedding=embedding,
                data=doc
            )

            return result
        except Exception as e:
            return UpdateCollectionResponse(
                status="error",
                message=f"Failed to update document: {str(e)}",
                id=doc_id,
                updated_count=None
            )

    async def delete(
            self, 
            doc_id: str,
            collection_name: str
        ) -> DeleteFromCollectionResponse:
        """Delete a memory entry from specified collection"""
        return await self.vdb_client.delete_from_collection(
            collection_name=collection_name,
            memory_id=doc_id
        )
        
