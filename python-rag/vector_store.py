"""
Vector Store for RAG System using ChromaDB
Handles document embeddings and semantic search
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Try to import chromadb and sentence-transformers, but make them optional
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logger.warning("ChromaDB not available. Vector store features will be disabled.")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("Sentence transformers not available. Embeddings will be disabled.")

class VectorStore:
    def __init__(self, persist_directory="./chroma_db"):
        """
        Initialize ChromaDB vector store with sentence transformer embeddings
        """
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB is not installed. Install it with: pip install chromadb")
        
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("Sentence transformers is not installed. Install it with: pip install sentence-transformers")
        
        try:
            self.client = chromadb.Client(Settings(
                persist_directory=persist_directory,
                anonymized_telemetry=False
            ))
            
            # Use all-MiniLM-L6-v2 for efficient sentence embeddings
            logger.info("Loading sentence transformer model...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="placement_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"Vector store initialized. Collection size: {self.collection.count()}")
            
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """
        Add documents to the vector store with embeddings
        
        Args:
            documents: List of text documents to add
            metadatas: List of metadata dicts for each document
            ids: List of unique IDs for each document
        """
        try:
            if not documents:
                logger.warning("No documents to add")
                return
            
            logger.info(f"Generating embeddings for {len(documents)} documents...")
            embeddings = self.embedding_model.encode(documents).tolist()
            
            logger.info(f"Adding {len(documents)} documents to collection...")
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Successfully added {len(documents)} documents. Total: {self.collection.count()}")
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def search(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        """
        Search for relevant documents using semantic similarity
        
        Args:
            query: Search query text
            n_results: Number of results to return
            
        Returns:
            Dictionary with 'documents', 'metadatas', 'distances', and 'ids'
        """
        try:
            logger.info(f"Searching for: '{query}' (top {n_results} results)")
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            # Log results
            if results['documents'] and results['documents'][0]:
                logger.info(f"Found {len(results['documents'][0])} relevant documents")
                for i, doc in enumerate(results['documents'][0]):
                    distance = results['distances'][0][i] if 'distances' in results else 0
                    logger.debug(f"  {i+1}. Distance: {distance:.3f}, Preview: {doc[:100]}...")
            else:
                logger.info("No documents found")
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {'documents': [[]], 'metadatas': [[]], 'distances': [[]], 'ids': [[]]}
    
    def clear_collection(self):
        """
        Clear all documents from the collection
        """
        try:
            self.client.delete_collection(name="placement_knowledge")
            self.collection = self.client.create_collection(
                name="placement_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Collection cleared successfully")
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store
        """
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'collection_name': 'placement_knowledge',
                'embedding_model': 'all-MiniLM-L6-v2',
                'embedding_dimension': 384
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {}

