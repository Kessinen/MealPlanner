"""Database connection management module.

This module provides a context manager for managing database connections and a function to test the connection.
"""

from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from settings import settings
from lib import logger


@contextmanager
def get_connection():
    """Context manager for database connections.

    Yields:
        psycopg.Cursor: A database cursor with dict_row factory.

    The connection is automatically committed on successful execution and rolled back on error.
    The cursor and connection are automatically closed when the context exits.
    """
    conn = None
    cur = None
    try:
        conn = psycopg.connect(settings.db_url)
        cur = conn.cursor(row_factory=dict_row)
        cur.execute("SELECT 1")  # Test the connection
        yield cur
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            try:
                conn.commit()
            except psycopg.Error as e:
                logger.error(f"Error committing transaction: {e}")
            if cur:
                cur.close()
            conn.close()


def test_connection() -> bool:
    """Test the database connection.

    Returns:
        bool: True if the connection test was successful, False otherwise.
    """
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        logger.debug("Database connection test successful")
        return True
    except psycopg.Error as e:
        logger.error(f"Database connection test failed: {e}")
        return False
