"""Basic tests for code2prompt functionality."""
import pytest
from code2prompt_rs import Code2Prompt

def test_initialization(sample_project_path):
    """Test that Code2Prompt can be initialized."""
    prompt = Code2Prompt(path=str(sample_project_path))
    assert prompt is not None

def test_generate(sample_project_path):
    """Test prompt generation."""
    prompt = Code2Prompt(
        path=str(sample_project_path),
        include_patterns=["*.py"],
        line_numbers=True
    )
    
    # Generate prompt
    result = prompt.generate()
    
    # Basic assertions
    assert result is not None
    assert isinstance(result, str)
    assert "main.py" in result
    assert "utils.py" in result

def test_token_counting(sample_project_path):
    """Test token counting."""
    prompt = Code2Prompt(path=str(sample_project_path))
    
    # Create a session with token counting
    session = prompt._inner.with_token_encoding("cl100k")
    token_count = session.token_count()
    
    # The token count should be a positive integer
    assert isinstance(token_count, int)
    assert token_count > 0