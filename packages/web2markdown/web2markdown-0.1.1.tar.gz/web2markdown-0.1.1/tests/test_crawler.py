import pytest
from unittest.mock import Mock, patch
from web2markdown.crawler import WebCrawler
from urllib.parse import urlparse

@pytest.fixture
def crawler():
    return WebCrawler("https://example.com/blog")

def test_init(crawler):
    assert crawler.base_url == "https://example.com/blog"
    assert crawler.max_depth == 3
    assert isinstance(crawler.visited_urls, set)
    assert isinstance(crawler.pages, dict)

def test_is_valid_url(crawler):
    # Valid URLs (same domain and path)
    assert crawler.is_valid_url("https://example.com/blog/post1")
    assert crawler.is_valid_url("https://example.com/blog/category/post2")
    
    # Invalid URLs (different domain or path)
    assert not crawler.is_valid_url("https://different.com/blog/post1")
    assert not crawler.is_valid_url("https://example.com/different/post1")
    assert not crawler.is_valid_url("invalid-url")

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.text = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Test Content</h1>
            <p>This is a test paragraph.</p>
            <a href="/blog/post1">Link 1</a>
            <a href="https://example.com/blog/post2">Link 2</a>
            <a href="https://different.com/post3">External Link</a>
        </body>
    </html>
    """
    return mock

@patch('trafilatura.fetch_url')
@patch('trafilatura.extract')
@patch('trafilatura.extract_metadata')
def test_get_page_content(mock_metadata, mock_extract, mock_fetch, crawler, mock_response):
    # Setup mocks
    mock_fetch.return_value = mock_response.text
    mock_extract.return_value = "# Test Content\n\nThis is a test paragraph."
    
    metadata = Mock()
    metadata.title = "Test Page"
    metadata.author = "Test Author"
    metadata.date = "2025-03-18"
    metadata.description = "Test Description"
    metadata.sitename = "Example Blog"
    metadata.categories = ["test"]
    mock_metadata.return_value = metadata

    # Test page content extraction
    content = crawler.get_page_content("https://example.com/blog/post1")
    
    assert content is not None
    assert content['title'] == "Test Page"
    assert "Test Content" in content['content']
    assert len(content['links']) == 2  # Only valid internal links
    assert all(link.startswith("https://example.com/blog/") for link in content['links'])
    assert content['metadata']['author'] == "Test Author"

@patch('web2markdown.crawler.WebCrawler.get_page_content')
def test_crawl(mock_get_content, crawler):
    # Setup mock content for multiple pages
    mock_content = {
        'title': 'Test Page',
        'content': '# Test Content',
        'links': ['https://example.com/blog/post2'],
        'metadata': {'author': 'Test Author'}
    }
    mock_get_content.return_value = mock_content

    # Test crawling
    pages = crawler.crawl()
    
    assert len(pages) > 0
    assert 'https://example.com/blog' in pages
    assert pages['https://example.com/blog'] == mock_content

def test_max_depth_limit(crawler):
    crawler.max_depth = 1
    with patch('web2markdown.crawler.WebCrawler.get_page_content') as mock_get_content:
        mock_content = {
            'title': 'Test Page',
            'content': '# Test Content',
            'links': ['https://example.com/blog/post2'],
            'metadata': {'author': 'Test Author'}
        }
        mock_get_content.return_value = mock_content
        
        pages = crawler.crawl()
        assert len(pages) == 1  # Only base URL should be crawled

def test_error_handling(crawler):
    with patch('trafilatura.fetch_url') as mock_fetch:
        mock_fetch.side_effect = Exception("Network error")
        content = crawler.get_page_content("https://example.com/blog/error")
        assert content is None
