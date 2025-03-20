from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="web2markdown",
    version="0.1.0",
    author="Roger Koa",
    description="A Python library for crawling web pages and converting them to markdown format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roger_koa/web-to-markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "urllib3>=2.1.0",
        "markdown>=3.5.0",
        "trafilatura>=0.8.1",
    ],
    extras_require={
        'test': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'pytest-mock>=3.11.1',
        ],
    },
    test_suite='tests',
    entry_points={
        "console_scripts": [
            "web2markdown=web2markdown.cli:main",
        ],
    },
)
