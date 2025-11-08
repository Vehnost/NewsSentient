"""
Sentient News Agent API Server
Implements Sentient Agent API standard with streaming support.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from contextlib import asynccontextmanager
import json
from loguru import logger

from agent import SentientNewsAgent
from models import AgentRequest, AgentResponse, AgentCapabilities
from config import settings


# Global agent instance
agent: SentientNewsAgent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    global agent
    
    # Startup
    logger.info("Starting Sentient News Agent...")
    agent = SentientNewsAgent()
    logger.info(f"Agent '{settings.agent_name}' initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Sentient News Agent...")
    if agent:
        await agent.close()
    logger.info("Agent closed")


# Create FastAPI application
app = FastAPI(
    title="Sentient News Agent",
    description="AI-powered news aggregator following Sentient API standards",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.agent_name,
        "description": settings.agent_description,
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "capabilities": "/capabilities",
            "chat": "/v1/chat (POST)",
            "chat_stream": "/v1/chat/stream (POST)",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": settings.agent_name,
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.get("/capabilities", response_model=AgentCapabilities)
async def get_capabilities():
    """
    Get agent capabilities.
    
    This endpoint describes what the agent can do.
    """
    return agent.get_capabilities()


@app.post("/v1/chat")
async def chat(request: AgentRequest):
    """
    Chat with agent (non-streaming).
    
    This is a fallback endpoint for clients that don't support streaming.
    For best UX, use /v1/chat/stream instead.
    """
    try:
        response = await agent.process_request(request)
        return {
            "message": response,
            "agent": settings.agent_name,
            "streaming": False
        }
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/chat/stream")
async def chat_stream(request: AgentRequest):
    """
    Chat with agent (streaming).
    
    This endpoint implements Sentient Agent API streaming standard.
    It sends Server-Sent Events (SSE) with intermediate thinking steps,
    progress updates, and the final response.
    
    Event format:
    - Each event is a JSON object with 'type' field
    - Types: 'thinking', 'content', 'data', 'complete', 'error'
    - Events are sent as SSE format: "data: {json}\\n\\n"
    """
    if not request.stream:
        # If streaming is disabled, redirect to non-streaming endpoint
        return await chat(request)
    
    async def event_generator():
        """Generate SSE events."""
        try:
            async for response in agent.process_request_stream(request):
                # Format as SSE
                event_data = response.model_dump_json(exclude_none=True)
                yield f"data: {event_data}\n\n"
                
        except Exception as e:
            logger.error(f"Error in stream: {e}")
            error_response = AgentResponse(
                type="error",
                content=f"Stream error: {str(e)}"
            )
            yield f"data: {error_response.model_dump_json()}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/v1/query/news")
async def query_news(
    keywords: list[str] = None,
    categories: list[str] = None,
    max_results: int = 10
):
    """
    Direct news query endpoint (non-conversational).
    
    This endpoint allows direct querying without chat context.
    """
    try:
        articles = await agent.aggregator.search_news(
            keywords=keywords or [],
            categories=categories or ["general"],
            max_results=max_results
        )
        
        return {
            "articles": [article.dict() for article in articles],
            "total": len(articles),
            "keywords": keywords,
            "categories": categories
        }
    except Exception as e:
        logger.error(f"Error in query_news: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/categories")
async def get_categories():
    """Get available news categories."""
    return {
        "categories": list(agent.aggregator.RSS_FEEDS.keys()),
        "description": "Available news categories for filtering"
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
