import os
import sys
import pytest
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.fibery_mcp_server.fibery_client import FiberyClient
from src.fibery_mcp_server.tools.create_entity import handle_create_entity
from src.fibery_mcp_server.tools.update_entity import handle_update_entity

pytestmark = pytest.mark.skipif(
    not os.environ.get("FIBERY_HOST") or not os.environ.get("FIBERY_API_TOKEN"),
    reason="FIBERY_HOST or FIBERY_API_TOKEN environment variables not set",
)
__fibery_host, __fibery_api_token = (
    os.environ.get("FIBERY_HOST"),
    os.environ.get("FIBERY_API_TOKEN"),
)


async def test_create_entity() -> None:
    """Test the create_entity function"""
    fibery_client = FiberyClient(__fibery_host, __fibery_api_token)
    creation_result = await handle_create_entity(
        fibery_client,
        {
            "database": "Product Management/Item",
            "entity": {
                "workflow/state": "To Do",
                "Product Management/Name": "Image Fourier Transform Understanding",
                "Product Management/Description": """A comprehensive summary of 2D Fourier Transform concepts for image processing, including:

- Basic principles of Fourier Transform
- Comparison between 1D (audio) and 2D (image) transforms
- Explanation of frequency domain representation
- Understanding of k and l frequency indices
- Visualization techniques for FFT output
- Edge effects and window functions
- Alignment of frequency patterns with image features
- Practical applications in image processing

This document includes explanations suitable for different audiences from beginners to technical specialists.""",
            },
        },
    )

    print(creation_result)


async def test_update_entity() -> None:
    """Test the create_entity function"""
    fibery_client = FiberyClient(__fibery_host, __fibery_api_token)
    update_result = await handle_update_entity(
        fibery_client,
        {
            "database": "Product Management/Item",
            "entity": {
                "fibery/id": "d3e27780-0ea9-11ef-ab49-df048edba921",
                "workflow/state": "Done",
                "Product Management/Name": "UPDATED 2!",
                "Product Management/Description": {"append": True, "content": " - Updated description"},
            },
        },
    )

    print(update_result)
