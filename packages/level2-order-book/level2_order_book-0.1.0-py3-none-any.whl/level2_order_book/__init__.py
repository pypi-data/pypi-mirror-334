"""
L2Data Reader - A package for reading level 2 market data.
"""

__version__ = '0.1.0'

from .order_book import OrderBook, Order

__all__ = [
    'OrderBook',
    'Order'
]