"""
Initialize Vector Database with Knowledge Base Documents
Loads markdown files from knowledge_base/ directory and populates ChromaDB
"""
from vector_store import VectorStore
import os
import glob
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_knowledge_base():
    """
    Load all markdown files from knowledge_base/ directory and add to vector store
    """
    try:
        logger.info("=" * 60)
        logger.info("Initializing Vector Database")
        logger.info("=" * 60)
        
        # Initialize vector store
        vector_store = VectorStore()
        
        # Get current stats
        stats = vector_store.get_stats()
        logger.info(f"Current collection size: {stats.get('total_documents', 0)} documents")
        
        # Load markdown files from knowledge_base/
        kb_path = "knowledge_base/*.md"
        files = glob.glob(kb_path)
        
        if not files:
            logger.warning(f"No markdown files found in knowledge_base/")
            logger.warning("Please create .md files in the knowledge_base/ directory")
            return
        
        logger.info(f"Found {len(files)} markdown files to process")
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, file_path in enumerate(files):
            logger.info(f"Processing {os.path.basename(file_path)}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Split into sections by ## headers (H2 level)
                sections = content.split('\n## ')
                
                # First section might contain the main title (# header)
                if sections[0].startswith('# '):
                    # Remove the main title and add rest as introduction
                    intro_parts = sections[0].split('\n', 1)
                    if len(intro_parts) > 1 and intro_parts[1].strip():
                        documents.append(intro_parts[1].strip())
                        metadatas.append({
                            'source': os.path.basename(file_path),
                            'type': 'knowledge_base',
                            'section': 'introduction'
                        })
                        ids.append(f"{os.path.basename(file_path)}_intro")
                    sections = sections[1:]  # Remove first section
                elif sections[0].strip():
                    # No title, treat as full section
                    documents.append(sections[0].strip())
                    metadatas.append({
                        'source': os.path.basename(file_path),
                        'type': 'knowledge_base',
                        'section': 'introduction'
                    })
                    ids.append(f"{os.path.basename(file_path)}_intro")
                    sections = sections[1:]
                
                # Process remaining sections
                for section_idx, section in enumerate(sections):
                    section_text = section.strip()
                    if section_text:
                        # Add back the ## prefix for proper header
                        section_text = "## " + section_text
                        
                        # Extract section title (first line)
                        section_lines = section_text.split('\n', 1)
                        section_title = section_lines[0].replace('## ', '').strip()
                        
                        documents.append(section_text)
                        metadatas.append({
                            'source': os.path.basename(file_path),
                            'type': 'knowledge_base',
                            'section': section_title
                        })
                        ids.append(f"{os.path.basename(file_path)}_{idx}_{section_idx}")
                        
                        logger.debug(f"  - Section: {section_title} ({len(section_text)} chars)")
        
        if not documents:
            logger.warning("No documents extracted from files")
            return
        
        logger.info(f"\nExtracted {len(documents)} sections from all files")
        logger.info("Adding documents to vector database...")
        
        # Add documents to vector store
        vector_store.add_documents(documents, metadatas, ids)
        
        # Get final stats
        final_stats = vector_store.get_stats()
        
        logger.info("=" * 60)
        logger.info("✓ Vector Database Initialized Successfully")
        logger.info("=" * 60)
        logger.info(f"Total documents: {final_stats.get('total_documents', 0)}")
        logger.info(f"Embedding model: {final_stats.get('embedding_model', 'unknown')}")
        logger.info(f"Embedding dimension: {final_stats.get('embedding_dimension', 'unknown')}")
        logger.info("=" * 60)
        
        # Test search
        logger.info("\nTesting search functionality...")
        test_queries = [
            "How do I start an assessment?",
            "Tips for aptitude improvement",
            "What is the passing criteria?"
        ]
        
        for query in test_queries:
            results = vector_store.search(query, n_results=2)
            if results['documents'] and results['documents'][0]:
                logger.info(f"\nQuery: '{query}'")
                logger.info(f"Found {len(results['documents'][0])} results")
                for i, doc in enumerate(results['documents'][0][:1]):  # Show first result
                    preview = doc[:150].replace('\n', ' ') + "..."
                    logger.info(f"  Result {i+1}: {preview}")
        
        logger.info("\n✓ Initialization complete! Vector database is ready.")
        
    except Exception as e:
        logger.error(f"Failed to initialize vector database: {e}")
        raise

if __name__ == "__main__":
    load_knowledge_base()

