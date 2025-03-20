import pytest
import os
from web2markdown.converter import MarkdownConverter

@pytest.fixture
def converter():
    return MarkdownConverter()

@pytest.fixture
def sample_pages():
    return {
        'https://example.com/blog/post1': {
            'title': 'Test Post 1',
            'content': '# Test Post 1\n\nThis is test content.',
            'metadata': {
                'author': 'Test Author',
                'date': '2025-03-18',
                'description': 'Test Description',
                'keywords': 'test, example',
                'sitename': 'Example Blog'
            }
        },
        'https://example.com/blog/post2': {
            'title': 'Test Post 2',
            'content': '# Test Post 2\n\nMore test content.',
            'metadata': {}  # Empty metadata
        }
    }

def test_convert_to_markdown(converter, sample_pages):
    markdown = converter.convert_to_markdown(sample_pages)
    
    # Check basic structure
    assert '---' in markdown
    assert '**Source**:' in markdown
    
    # Check content inclusion
    assert 'Test Post 1' in markdown
    assert 'Test Post 2' in markdown
    assert 'This is test content' in markdown
    assert 'More test content' in markdown
    
    # Check metadata handling
    assert '**Author**: Test Author' in markdown
    assert '**Published**: 2025-03-18' in markdown
    assert '**Description**: Test Description' in markdown
    assert '**Keywords**: test, example' in markdown

def test_convert_empty_pages(converter):
    markdown = converter.convert_to_markdown({})
    assert markdown.strip() == '---'

def test_convert_none_content(converter):
    pages = {'https://example.com': None}
    markdown = converter.convert_to_markdown(pages)
    assert markdown.strip() == '---'

def test_save_markdown(converter, tmp_path):
    content = "# Test Content\n\nThis is a test."
    output_file = tmp_path / "test_output.md"
    
    converter.save_markdown(content, str(output_file))
    
    assert output_file.exists()
    with open(output_file, 'r', encoding='utf-8') as f:
        saved_content = f.read()
    assert saved_content == content

def test_save_markdown_error_handling(converter, tmp_path):
    content = "# Test Content"
    invalid_path = str(tmp_path / "nonexistent" / "test.md")
    
    # Should not raise an exception
    converter.save_markdown(content, invalid_path)

def test_metadata_partial(converter):
    pages = {
        'https://example.com': {
            'title': 'Test',
            'content': '# Test\n\nContent',
            'metadata': {
                'author': 'Author',  # Only author provided
                'date': None,
                'description': None,
                'keywords': None
            }
        }
    }
    
    markdown = converter.convert_to_markdown(pages)
    assert '**Author**: Author' in markdown
    assert '**Published**:' not in markdown
    assert '**Description**:' not in markdown
    assert '**Keywords**:' not in markdown
