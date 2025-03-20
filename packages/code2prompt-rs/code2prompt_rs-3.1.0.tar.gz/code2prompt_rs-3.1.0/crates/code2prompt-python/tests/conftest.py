"""Pytest fixtures for code2prompt tests."""
import os
import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture
def sample_project_path():
    """Return the path to the sample project."""
    current_dir = Path(__file__).parent
    return current_dir / "resources" / "sample_project"

@pytest.fixture
def temp_project_dir():
    """Create a temporary directory with sample project files."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Copy sample project to temp dir
        source_dir = Path(__file__).parent / "resources" / "sample_project"
        for item in source_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, temp_dir)
            else:
                shutil.copytree(item, Path(temp_dir) / item.name)
                
        yield temp_dir
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)