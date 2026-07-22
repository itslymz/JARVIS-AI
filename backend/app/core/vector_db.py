"""Qdrant vector database management."""

from typing import Any, List, Optional

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from app.config import settings

vector_client: Optional[AsyncQdrantClient] = None


async def init_vector_db() -> None:
    """Initialize Qdrant vector database."""
    global vector_client
    try:
        vector_client = AsyncQdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None,
        )
        
        # Check if collection exists, if not create it
        collections = await vector_client.get_collections()
        collection_names = [c.name for c in collections.collections]
        
        if settings.QDRANT_COLLECTION_NAME not in collection_names:
            await vector_client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=settings.QDRANT_VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )
    except Exception as e:
        print(f"Qdrant initialization failed: {e}")


async def store_vector(
    collection_name: str,
    point_id: int,
    vector: List[float],
    payload: dict,
) -> bool:
    """Store vector in Qdrant."""
    if not vector_client:
        return False
    try:
        point = PointStruct(
            id=point_id,
            vector=vector,
            payload=payload,
        )
        await vector_client.upsert(
            collection_name=collection_name,
            points=[point],
        )
        return True
    except Exception as e:
        print(f"Vector store failed: {e}")
    return False


async def search_vectors(
    collection_name: str,
    vector: List[float],
    limit: int = 10,
) -> List[dict]:
    """Search vectors in Qdrant."""
    if not vector_client:
        return []
    try:
        results = await vector_client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit,
        )
        return [
            {
                "id": result.id,
                "score": result.score,
                "payload": result.payload,
            }
            for result in results
        ]
    except Exception as e:
        print(f"Vector search failed: {e}")
    return []
