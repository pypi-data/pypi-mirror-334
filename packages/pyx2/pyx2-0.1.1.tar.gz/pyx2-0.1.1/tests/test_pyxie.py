"""Test Pyxie class functionality."""

import pytest
import pytest_asyncio
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

from pyxie.pyxie import Pyxie
from pyxie.errors import PyxieError
from pyxie.types import ContentItem

# Test utilities
@dataclass
class TestContent:
    """Helper for creating test content."""
    content: str
    layout: str = "test"
    metadata: Dict[str, str] = None
    
    def write_to(self, path: Path) -> None:
        """Write content to a file."""
        content = "---\n"
        content += f"layout: {self.layout}\n"
        if self.metadata:
            for key, value in self.metadata.items():
                content += f"{key}: {value}\n"
        content += "status: published\n"  # Add status for filtering
        content += "---\n"
        content += self.content
        path.write_text(content)

# Fixtures
@pytest.fixture
def test_paths(tmp_path: Path) -> Dict[str, Path]:
    """Create test directory structure."""
    paths = {
        'layouts': tmp_path / "layouts",
        'content': tmp_path / "content",
        'cache': tmp_path / "cache"
    }
    for path in paths.values():
        path.mkdir()
    return paths

@pytest.fixture
def pyxie(test_paths: Dict[str, Path]) -> Pyxie:
    """Create a test Pyxie instance."""
    pyxie = Pyxie(
        content_dir=test_paths['content'],
        cache_dir=test_paths['cache']
    )
    return pyxie

# Test cases
def test_initialization(pyxie: Pyxie) -> None:
    """Test basic initialization."""
    assert pyxie.content_dir is not None
    assert pyxie._collections is not None

def test_add_collection(pyxie: Pyxie) -> None:
    """Test adding content collections."""
    # Add test collection
    pyxie.add_collection(
        name="test",
        path=pyxie.content_dir / "test",
        default_layout="default"
    )
    
    assert "test" in pyxie._collections
    assert pyxie._collections["test"].name == "test"
    assert pyxie._collections["test"].default_layout == "default"

def test_content_loading(pyxie: Pyxie) -> None:
    """Test loading content from collections."""
    # Create test collection
    test_dir = pyxie.content_dir / "test"
    test_dir.mkdir()
    
    # Add test content
    test_content = TestContent(
        content="# Test Content",
        metadata={"title": "Test Page"}
    )
    test_content.write_to(test_dir / "test.md")
    
    # Add collection and verify content
    pyxie.add_collection("test", test_dir)
    item, error = pyxie.get_item("test", collection="test")
    assert error is None
    assert item is not None
    assert item.metadata["title"] == "Test Page"

def test_error_handling(pyxie: Pyxie, monkeypatch) -> None:
    """Test error handling during content loading."""
    # Create a collection with invalid content
    test_dir = pyxie.content_dir / "error_test"
    test_dir.mkdir()
    
    # Create invalid markdown file
    invalid_file = test_dir / "invalid.md"
    invalid_file.write_text("---\nbroken yaml\n: :\n---\nContent")
    
    # This should log an error but not raise an exception
    pyxie.add_collection("error_test", test_dir)
    
    # Test nonexistent collection
    items = pyxie.get_items(collection="nonexistent")
    assert len(items) == 0

def test_collection_metadata(pyxie: Pyxie) -> None:
    """Test collection metadata handling."""
    # Add collection with metadata
    metadata = {"author": "Test Author", "category": "test"}
    pyxie.add_collection(
        name="test",
        path=pyxie.content_dir / "test",
        default_metadata=metadata
    )
    
    assert "author" in pyxie._collections["test"].default_metadata
    assert pyxie._collections["test"].default_metadata["author"] == "Test Author"

@pytest.mark.parametrize("has_cache", [True, False])
def test_query_items(pyxie: Pyxie, has_cache: bool, test_paths: Dict[str, Path]) -> None:
    """Test querying content items."""
    # Create test instance with or without cache
    if not has_cache:
        pyxie = Pyxie(content_dir=test_paths['content'])
    
    # Create test directory
    test_dir = pyxie.content_dir / "test"
    test_dir.mkdir()
    
    # Add test content with different tags
    for i in range(5):
        content = TestContent(
            content=f"# Test Content {i}",
            metadata={
                "title": f"Test Page {i}",
                "tags": f"tag{i}, common"
            }
        )
        content.write_to(test_dir / f"test{i}.md")
    
    # Add collection
    pyxie.add_collection("test", test_dir)
    
    # Test basic query
    all_items = pyxie.get_items()
    assert len(all_items) == 5
    
    # Test filtering
    filtered = pyxie.get_items(tags__contains=["tag1"])
    assert len(filtered) == 1
    
    common = pyxie.get_items(tags__contains=["common"])
    assert len(common) == 5 