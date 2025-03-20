from typing import List, Dict, Any, Optional, Tuple
from gru.agents.tools.core.code_generator.models import RetrievalResult
from gru.agents.tools.core.vector_db.milvus import MilvusClient
from .base import ContextRetriever


class SQLContextRetriever(ContextRetriever):
    def __init__(
        self,
        vector_store: MilvusClient,
        system_prompt: Optional[str] = None,
        user_prompt_template: Optional[str] = None,
    ):
        super().__init__(vector_store, system_prompt, user_prompt_template)
        self.vector_store = vector_store

    async def get_relevant_datasources_and_schemas(
        self,
        query_embedding: List[float],
        top_k: int,
        embedding_field: str,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> Tuple[List[str], List[str]]:
        """
        Retrieves relevant data sources (tables) and their schemas.
        """
        if search_params is None:
            search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

        if output_fields is None:
            output_fields = ["table_name", "contents"]

        # Perform the similarity search
        search_response = await self.vector_store.similarity_search(
            collection_name="canso_table_metadata",
            query_vector=query_embedding,
            anns_field=embedding_field,
            top_k=top_k,
            search_params=search_params,
            output_fields=output_fields,
        )

        # Check if the search was successful
        if search_response.status != "success":
            raise ValueError(f"Search failed: {search_response.message}")

        # Extract the actual results from the search response
        data = search_response.results

        # Extract table names and schemas
        tables = [item.get("table_name", "") for item in data]
        schemas = [item.get("contents", "") for item in data]

        return tables, schemas

    async def get_similar_examples(
        self,
        query_embedding: List[float],
        top_k: int,
        embedding_field: str,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> List[str]:
        """Retrieves similar examples based on the query embedding."""
        if output_fields is None:
            output_fields = ["examples"]

        search_response = await self.vector_store.similarity_search(
            collection_name="canso_examples",
            query_vector=query_embedding,
            anns_field=embedding_field,
            top_k=top_k,
            search_params=search_params,
            output_fields=output_fields,
        )

        # Check if the search was successful
        if search_response.status != "success":
            raise ValueError(f"Search failed: {search_response.message}")

        # Extract the actual results from the search response
        data = search_response.results

        return [item.get("examples", "") for item in data]

    async def get_documentation(
        self,
        query_embedding: List[float],
        top_k: int,
        embedding_field: str,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> List[str]:
        """Retrieves relevant documentation based on the query embedding."""
        if output_fields is None:
            output_fields = ["documentation"]

        search_response = await self.vector_store.similarity_search(
            collection_name="canso_domain_knowledge",
            query_vector=query_embedding,
            anns_field=embedding_field,
            top_k=top_k,
            search_params=search_params,
            output_fields=output_fields,
        )

        # Check if the search was successful
        if search_response.status != "success":
            raise ValueError(f"Search failed: {search_response.message}")

        # Extract the actual results from the search response
        data = search_response.results

        return [item.get("documentation", "") for item in data]

    async def retrieve_context(
        self, query_embedding: List[float], top_k: int
    ) -> RetrievalResult:
        """Retrieves all relevant context for the query embedding."""
        tables, schemas = await self.get_relevant_datasources_and_schemas(
            query_embedding, top_k, "embedding"
        )
        examples = await self.get_similar_examples(
            query_embedding, top_k, "embeddings"
        )
        documentation = await self.get_documentation(
            query_embedding, top_k, "embeddings"
        )

        return RetrievalResult(
            tables=tables,
            schemas=schemas,
            documentation=documentation,
            examples=examples,
            low_cardinality_values=[],
            domain_knowledge=[],
            opt_rules=[],
        )
