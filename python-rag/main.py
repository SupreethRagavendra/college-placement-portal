"""
Main FastAPI Service for OpenRouter RAG System
Production-ready RAG service with dynamic knowledge sync
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import asyncio

# Import custom modules (will be created)
from openrouter_client import OpenRouterClient
from context_handler import ContextHandler
from response_formatter import ResponseFormatter
from knowledge_sync import KnowledgeSync
from vector_store import VectorStore
from response_cache import ResponseCache

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv('DEBUG', 'False').lower() == 'true' else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rag_service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="College Placement Portal RAG Service",
    description="OpenRouter AI powered RAG service with dynamic knowledge sync",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "https://college-placement-portal.onrender.com",
        "https://college-placement-portals.onrender.com",
        os.getenv("LARAVEL_APP_URL", "http://localhost:8000")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    openrouter_client = OpenRouterClient(
        api_key=os.getenv('OPENROUTER_API_KEY'),
        primary_model=os.getenv('OPENROUTER_PRIMARY_MODEL'),
        fallback_model=os.getenv('OPENROUTER_FALLBACK_MODEL'),
        api_url=os.getenv('OPENROUTER_API_URL')
    )
    
    # Initialize vector store for RAG (optional - will work without it)
    vector_store = None
    try:
        vector_store = VectorStore()
        logger.info("Vector store initialized successfully")
    except (ImportError, Exception) as ve:
        logger.warning(f"Vector store initialization failed: {ve}")
        logger.warning("RAG will operate without vector search - this is OK for deployment")
        vector_store = None
    
    context_handler = ContextHandler(
        openrouter_client=openrouter_client,
        vector_store=vector_store  # Pass vector store for RAG
    )
    response_formatter = ResponseFormatter()
    
    # Initialize response cache (5 minutes TTL)
    response_cache = ResponseCache(ttl_seconds=300)
    logger.info("Response cache initialized")
    
    knowledge_sync = KnowledgeSync(
        db_host=os.getenv('SUPABASE_DB_HOST'),
        db_port=os.getenv('SUPABASE_DB_PORT'),
        db_name=os.getenv('SUPABASE_DB_NAME'),
        db_user=os.getenv('SUPABASE_DB_USER'),
        db_password=os.getenv('SUPABASE_DB_PASSWORD')
    )
    
    logger.info("All services initialized successfully")
except Exception as e:
    logger.error(f"Service initialization failed: {e}")
    raise


# Pydantic Models
class ChatRequest(BaseModel):
    student_id: int = Field(..., description="Student ID")
    message: str = Field(..., min_length=1, max_length=500, description="Student's question")
    student_email: Optional[str] = Field(None, description="Student email")
    student_name: Optional[str] = Field(None, description="Student name")
    conversation_history: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Conversation history")


class ChatResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    actions: List[Dict[str, str]] = []
    follow_up_questions: List[str] = []
    timestamp: str
    model_used: Optional[str] = None
    query_type: Optional[str] = None


class SyncRequest(BaseModel):
    force: Optional[bool] = Field(False, description="Force full resync")


class SyncResponse(BaseModel):
    success: bool
    message: str
    stats: Dict[str, Any]
    timestamp: str


# Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "College Placement Portal RAG Service",
        "version": "1.0.0",
        "status": "running",
        "primary_model": os.getenv('OPENROUTER_PRIMARY_MODEL'),
        "fallback_model": os.getenv('OPENROUTER_FALLBACK_MODEL'),
        "provider": "OpenRouter AI"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        try:
            conn = knowledge_sync.get_postgres_connection()
            conn.close()
            db_status = "connected"
        except:
            db_status = "disconnected"
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "database": db_status,
            "primary_model": os.getenv('OPENROUTER_PRIMARY_MODEL'),
            "fallback_model": os.getenv('OPENROUTER_FALLBACK_MODEL')
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for student queries
    Processes queries with RAG and OpenRouter AI with comprehensive fallback chain
    """
    logger.info(f"Chat request from student {request.student_id}: {request.message}")
    
    try:
        # Check cache first (only for non-personalized queries)
        if response_cache.should_cache(request.message):
            cached = response_cache.get(request.message, request.student_id)
            if cached:
                logger.info(f"Returning cached response for student {request.student_id}")
                cached['from_cache'] = True
                cached['timestamp'] = datetime.utcnow().isoformat() + "Z"
                return cached
        
        # Get student-specific context from database
        try:
            student_context = knowledge_sync.get_student_context(request.student_id)
            logger.info(f"Retrieved context for student {request.student_id}")
        except Exception as db_error:
            logger.warning(f"Database context retrieval failed: {db_error}")
            # Continue with empty context if database fails
            student_context = {
                'available_assessments': [],
                'completed_assessments': [],
                'performance_summary': {}
            }
        
        # Process query with context handler (includes OpenRouter + fallback + RAG)
        message, data, query_type, model_used = context_handler.process_query(
            student_id=request.student_id,
            query=request.message,
            student_context=student_context,
            student_email=request.student_email,
            student_name=request.student_name,
            conversation_history=request.conversation_history  # Add conversation history for context
        )
        
        # Format response with status indicators
        response = response_formatter.format_response(
            message=message,
            data=data,
            query_type=query_type,
            student_id=request.student_id,
            model_used=model_used
        )
        
        # Cache response if appropriate (non-personalized queries)
        if response_cache.should_cache(request.message, query_type):
            response_cache.set(request.message, request.student_id, response)
            logger.info(f"Response cached for future requests")
        
        response['from_cache'] = False
        
        logger.info(f"Response generated successfully for student {request.student_id} using model {model_used}")
        return response
    
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        
        # Final fallback
        return ChatResponse(
            success=True,
            message="I'm experiencing technical difficulties right now. Please try again in a moment or contact support if the issue persists.",
            data={
                'service_status': 'error',
                'error': str(e)
            },
            actions=[],
            follow_up_questions=[],
            timestamp=datetime.utcnow().isoformat() + "Z",
            model_used='error',
            query_type='error'
        )


@app.post("/sync-knowledge", response_model=SyncResponse)
async def sync_knowledge(
    request: SyncRequest = SyncRequest(),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Trigger knowledge base sync from database
    Called by Laravel when admin updates assessments/questions
    """
    logger.info(f"Knowledge sync requested (force={request.force})")
    
    try:
        # Perform sync in background for non-blocking
        if request.force:
            stats = await asyncio.get_event_loop().run_in_executor(None, knowledge_sync.sync_all, True)
        else:
            # Quick incremental sync
            stats = await asyncio.get_event_loop().run_in_executor(None, knowledge_sync.sync_all, False)
        
        return {
            "success": True,
            "message": "Knowledge base synced successfully",
            "stats": stats,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        return {
            "success": False,
            "message": f"Sync failed: {str(e)}",
            "stats": {"errors": [str(e)]},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


@app.post("/init-student-context")
async def init_student_context(student_id: int):
    """
    Initialize or refresh student-specific context
    Can be called when student logs in
    """
    logger.info(f"Initializing context for student {student_id}")
    
    try:
        context = knowledge_sync.get_student_context(student_id)
        
        return {
            "success": True,
            "student_id": student_id,
            "context_summary": {
                "available_assessments": len(context.get('available_assessments', [])),
                "completed_assessments": len(context.get('completed_assessments', [])),
                "has_performance_data": bool(context.get('performance_summary'))
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    except Exception as e:
        logger.error(f"Context initialization failed for student {student_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models")
async def get_models():
    """Get available models"""
    return {
        "primary_model": os.getenv('OPENROUTER_PRIMARY_MODEL'),
        "fallback_model": os.getenv('OPENROUTER_FALLBACK_MODEL'),
        "api_url": os.getenv('OPENROUTER_API_URL')
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("=" * 60)
    logger.info("RAG Service Starting Up")
    logger.info("=" * 60)
    logger.info(f"Primary Model: {os.getenv('OPENROUTER_PRIMARY_MODEL')}")
    logger.info(f"Fallback Model: {os.getenv('OPENROUTER_FALLBACK_MODEL')}")
    logger.info(f"Database: {os.getenv('SUPABASE_DB_HOST')}")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("RAG Service shutting down...")


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Render uses PORT, local uses SERVICE_PORT
    port = int(os.getenv('PORT', os.getenv('SERVICE_PORT', 8001)))
    host = os.getenv('HOST', '0.0.0.0')
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv('DEBUG', 'False').lower() == 'true',
        log_level="info"
    )