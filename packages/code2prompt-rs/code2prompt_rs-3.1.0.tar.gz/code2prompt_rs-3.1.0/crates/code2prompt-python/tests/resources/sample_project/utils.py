"""Utility functions for the sample project."""

def double_values(values):
    """Double each value in the list."""
    return [x * 2 for x in values]

def capitalize_text(text):
    """Capitalize the first letter of each word."""
    return " ".join(word.capitalize() for word in text.split())