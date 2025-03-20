import asyncio
import json
import logging
import os
import os.path
from contextlib import asynccontextmanager
from dataclasses import dataclass
from logging import INFO, basicConfig
from typing import Any, AsyncIterator, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(message)s",
)
# PARAMS
DATA_ROOT = os.environ.get("DATA_ROOT", os.path.join(os.path.dirname(__file__), "data"))
CHROMA_DB_FOLDER_NAME = os.environ.get("CHROMA_DB_FOLDER_NAME", "default")
SENTENCE_TRANSFORMER_PATH = os.environ.get(
    "SENTENCE_TRANSFORMER_PATH", "jinaai/jina-embeddings-v2-base-code"
)

# Ensure data directories exist
os.makedirs(DATA_ROOT, exist_ok=True)
CHROMA_DB_PATH = os.path.join(DATA_ROOT, CHROMA_DB_FOLDER_NAME)
SENTENCE_TRANSFORMER_CACHE_FOLDER = os.path.join(DATA_ROOT, "embedding_cache")


# Server lifespan context for ChromaDB initialization and project directory
@dataclass
class ServerContext:
    chroma_client: Optional[Any] = None
    code_collection: Optional[Any] = None
    embedding_model: str = ""
    is_initialized: bool = False
    initialization_error: Optional[str] = None


# Create a global context object
ctx = ServerContext(embedding_model=SENTENCE_TRANSFORMER_PATH)


async def initialize_resources():
    """Initialize ChromaDB and embedding model in background"""
    try:
        logging.info("Thanks for using WindCodeAssistant!")
        logging.info(f"Initializing ChromaDB at {CHROMA_DB_PATH} and embedding model...")

        # Ensure all data directories exist
        os.makedirs(CHROMA_DB_PATH, exist_ok=True)
        os.makedirs(SENTENCE_TRANSFORMER_CACHE_FOLDER, exist_ok=True)

        # Import ChromaDB here to allow for dependency installation
        import chromadb
        from chromadb.utils import embedding_functions

        chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=SENTENCE_TRANSFORMER_PATH,
            cache_folder=SENTENCE_TRANSFORMER_CACHE_FOLDER,
        )

        # Create or get the code collection
        try:
            code_collection = chroma_client.get_collection(
                name="code_collection", embedding_function=embedding_function
            )
            logging.info(
                f"Using existing code collection with {code_collection.count()} documents"
            )
        except Exception as e:
            logging.info(f"Collection not found, creating new one. Error: {str(e)}")
            code_collection = chroma_client.create_collection(
                name="code_collection", embedding_function=embedding_function
            )
            logging.info("Created new code collection")

        # Update global context
        ctx.chroma_client = chroma_client
        ctx.code_collection = code_collection
        ctx.is_initialized = True
        logging.info("Background initialization completed successfully")
    except Exception as e:
        error_msg = f"Initialization failed: {str(e)}"
        logging.error(error_msg)
        ctx.initialization_error = error_msg


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[ServerContext]:
    """Start initialization in background and continue server startup immediately"""
    # Start initialization in background
    init_task = asyncio.create_task(initialize_resources())

    try:
        # Return control immediately with the global context
        yield ctx
    finally:
        logging.info("Waiting for initialization task to complete before shutdown...")
        # Make sure the init task completes before server shuts down
        if not init_task.done():
            init_task.cancel()
            try:
                await init_task
            except asyncio.CancelledError:
                logging.info("Initialization task was cancelled")


mcp = FastMCP(
    "WindCodeAssistant",
    dependencies=["glob", "re", "json", "subprocess"],
    lifespan=server_lifespan,
)


def _get_directory_info(directory_path: str) -> List[Dict[str, Any]]:
    """
    Helper function to get information about directory contents

    Args:
        directory_path: Absolute path to the directory

    Returns:
        List of dictionaries containing information about each child in the directory
    """
    result = []

    # Check if directory exists and is a directory
    if not os.path.exists(directory_path):
        raise ValueError(f"Directory does not exist: {directory_path}")
    if not os.path.isdir(directory_path):
        raise ValueError(f"Path is not a directory: {directory_path}")

    # Get all entries in the directory
    for entry in os.listdir(directory_path):
        entry_path = os.path.join(directory_path, entry)
        relative_path = os.path.relpath(entry_path, directory_path)

        if os.path.isdir(entry_path):
            # For directories, count children recursively
            child_count = sum(len(files) for _, _, files in os.walk(entry_path))
            result.append(
                {"path": relative_path, "type": "directory", "child_count": child_count}
            )
        else:
            # For files, get size in bytes
            size = os.path.getsize(entry_path)
            result.append({"path": relative_path, "type": "file", "size": size})

    return result


@mcp.tool()
def list_dir(directory_path: str) -> str:
    """
    List the contents of a directory.

    Directory path must be an absolute path to a directory that exists.
    For each child in the directory, output will have:
    - relative path to the directory
    - whether it is a directory or file
    - size in bytes if file
    - number of children (recursive) if directory

    Args:
        directory_path: Path to list contents of, should be absolute path to a directory

    Returns:
        JSON string containing directory information
    """
    # We don't need ChromaDB or embeddings for this function, so it works regardless of initialization
    try:
        logging.info(f"Listing directory: {directory_path}")
        directory_info = _get_directory_info(directory_path)
        return json.dumps(directory_info, indent=2)
    except Exception as e:
        logging.error(f"Error listing directory {directory_path}: {str(e)}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_initialization_status() -> str:
    """
    Get the status of background initialization process

    Returns:
        JSON string with initialization status
    """
    status = {
        "is_initialized": ctx.is_initialized,
        "error": ctx.initialization_error
    }
    return json.dumps(status)