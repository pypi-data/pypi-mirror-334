"""
MCP Aim Crawler
~~~~~~~~~~~~~~

A web crawler based on MCP protocol.
"""

from .crawler import WebCrawler
from .logger import logger

__version__ = '0.1.0'
__all__ = ['WebCrawler', 'logger'] 